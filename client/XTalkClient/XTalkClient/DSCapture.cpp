#include "StdAfx.h"
#include "DSCapture.h"

CDSCapture::CDSCapture(void)
{
	::CoInitialize(NULL);

	//	֪ͨ�¼�
	m_hNotificationEvent	= CreateEvent(NULL, FALSE, FALSE, NULL);
	m_hExitEvent			= CreateEvent(NULL, TRUE, FALSE, NULL);

	m_lpSoundCapture		= NULL;
	m_lpDSCB				= NULL;
	m_lpNotifyProc			= NULL;
	m_lpFrame				= NULL;
	m_dwNotifySize			= 0;

	memset(&wfx, 0, sizeof(WAVEFORMATEX));
}

CDSCapture::~CDSCapture(void)
{
	if (m_lpDSCB)
		m_lpDSCB->Release();

	if (m_lpSoundCapture)
		m_lpSoundCapture->Release();
}

void CDSCapture::EnumDevices(LPDSENUMCALLBACK callback, LPVOID ctx)
{
	//	ö���豸
	DirectSoundCaptureEnumerate(callback, ctx);
}

void CDSCapture::OpenDevice(LPGUID lpDeviceGUID, NOTIFYPROC callproc, LPVOID frame)
{
	if (m_lpDSCB)
		m_lpDSCB->Release();

	if (m_lpSoundCapture)
		m_lpSoundCapture->Release();

	DirectSoundCaptureCreate(lpDeviceGUID, &m_lpSoundCapture, NULL);

	m_lpNotifyProc	= callproc;
	m_lpFrame		= frame;
}

void CDSCapture::SetWaveFormat(WORD wChannels, DWORD dSamplesPerSec, WORD wBitsPerSample)
{
	DSCBUFFERDESC			dscBufferDesc;
	LPDIRECTSOUNDNOTIFY		lpDSNotify = NULL;
	DSBPOSITIONNOTIFY		dsPosNotify[NUM_REC_NOTIFICATIONS + 1]; 

	//
	//	���ò������
	//
	wfx.wFormatTag				= WAVE_FORMAT_PCM;									//	Ĭ��PCM��ʽ
	wfx.nChannels				= wChannels;										//	��������
	wfx.nSamplesPerSec			= dSamplesPerSec;									//	������ 11025=11.025kHz
	wfx.nAvgBytesPerSec			= wChannels * dSamplesPerSec * wBitsPerSample / 8;	//	ÿ��������
	wfx.nBlockAlign				= wBitsPerSample * wChannels / 8;					//	�ֽڶ���
	wfx.wBitsPerSample			= wBitsPerSample;
	wfx.cbSize					= 0;

	//
	//	����������
	//
	dscBufferDesc.dwSize		= sizeof(DSCBUFFERDESC);
	dscBufferDesc.dwFlags		= 0;
	dscBufferDesc.dwBufferBytes	= wfx.nAvgBytesPerSec * 2;		//	��������С������Ϊ1s����Ĵ�С
	dscBufferDesc.dwReserved	= 0;
	dscBufferDesc.lpwfxFormat	= &wfx; //����¼���õ�wave��ʽ
	dscBufferDesc.dwFXCount		= 0;
	dscBufferDesc.lpDSCFXDesc	= NULL;

	m_dwBufferSize				= dscBufferDesc.dwBufferBytes;

	//
	//	�������񻺳���
	//
	m_lpSoundCapture->CreateCaptureBuffer(&dscBufferDesc, &m_lpDSCB, NULL);

	//
	//	����֪ͨ��
	//
	m_dwNotifySize = m_dwBufferSize / NUM_REC_NOTIFICATIONS;			//	����֪ͨ��С

	m_lpDSCB->QueryInterface(IID_IDirectSoundNotify, (LPVOID*)&lpDSNotify);		//	��ȡ֪ͨ�����

	for( INT i = 0; i < NUM_REC_NOTIFICATIONS; i++ ) {

		//	����ÿ��֪ͨ��λ��
		dsPosNotify[i].dwOffset = m_dwNotifySize * i + m_dwNotifySize - 1;
		dsPosNotify[i].hEventNotify = m_hNotificationEvent;             
	}

	lpDSNotify->SetNotificationPositions(NUM_REC_NOTIFICATIONS, dsPosNotify);
}

DWORD WINAPI CDSCapture::_threadRecvData(LPVOID lParameter)
{
	CDSCapture* lpThis = static_cast<CDSCapture*>(lParameter);
	DWORD dwWaitFlags = 0;

	while(true)
	{
		dwWaitFlags = WaitForSingleObject(lpThis->m_hExitEvent, 0);
		if (WAIT_OBJECT_0 == dwWaitFlags)
			return 0;

		dwWaitFlags = WaitForSingleObject(lpThis->m_hNotificationEvent, 100);

		if (dwWaitFlags == WAIT_TIMEOUT)
			continue;

		lpThis->RecordCapturedData();
	}
}

void CDSCapture::RecordCapturedData()
{
	HRESULT hr;
	VOID*   pbCaptureData    = NULL;
	DWORD   dwCaptureLength;
	VOID*   pbCaptureData2   = NULL;
	DWORD   dwCaptureLength2;
	DWORD   dwReadPos;
	DWORD   dwCapturePos;
	long	tLockSize = 0;
	static DWORD m_dwNextCaptureOffset = 0;

	if( NULL == m_lpDSCB )
		return;

	if( FAILED( hr = m_lpDSCB->GetCurrentPosition( &dwCapturePos, &dwReadPos ) ) )
		return;

	tLockSize = dwReadPos - m_dwNextCaptureOffset;
	if( tLockSize < 0 )
		tLockSize += m_dwBufferSize;

	// Block align lock size so that we are always write on a boundary
	tLockSize -= (tLockSize % m_dwNotifySize);

	if( tLockSize == 0 )
		return;

	// Lock the capture buffer down
	if( FAILED( hr = m_lpDSCB->Lock( m_dwNextCaptureOffset, tLockSize, 
		&pbCaptureData, &dwCaptureLength, 
		&pbCaptureData2, &dwCaptureLength2, 0L ) ) )
		return;// DXTRACE_ERR_MSGBOX( TEXT("Lock"), hr );

	// Write the data into the wav file
	m_lpNotifyProc(m_lpFrame, pbCaptureData, dwCaptureLength);

	// Move the capture offset along
	m_dwNextCaptureOffset += dwCaptureLength; 
	m_dwNextCaptureOffset %= m_dwBufferSize; // Circular buffer

	if( pbCaptureData2 != NULL )
	{
		// Write the data into the wav file
		m_lpNotifyProc(m_lpFrame, pbCaptureData2, dwCaptureLength2);

			// Move the capture offset along
		m_dwNextCaptureOffset += dwCaptureLength2; 
		m_dwNextCaptureOffset %= m_dwBufferSize; // Circular buffer
	}

	// Unlock the capture buffer
	m_lpDSCB->Unlock( pbCaptureData,  dwCaptureLength, 
		pbCaptureData2, dwCaptureLength2 );
}

void CDSCapture::StartCapture()
{
	ResetEvent(m_hExitEvent);

	m_hThread = CreateThread(NULL, 0, _threadRecvData, this, 0, NULL);

	m_lpDSCB->Start(DSCBSTART_LOOPING);
}

void CDSCapture::StopCapture()
{
	m_lpDSCB->Stop();

	SetEvent(m_hExitEvent);

	if (WAIT_OBJECT_0 != WaitForSingleObject(m_hThread, 1000))
		TerminateThread(m_hThread, 0);
}