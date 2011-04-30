#include "StdAfx.h"
#include "DSSound.h"


CDSSound::CDSSound(void)
{
	CoInitialize(NULL);
	m_lpDirectSound = NULL;
	m_lpDSB			= NULL;
}


CDSSound::~CDSSound(void)
{
}

void CDSSound::EnumDevices(LPDSENUMCALLBACK callback, LPVOID ctx)
{
	//	枚举设备
	DirectSoundEnumerate(callback, ctx);
}

void CDSSound::OpenDevice(LPGUID lpDeviceGUID, HWND hWnd)
{
	HRESULT hr = DirectSoundCreate(lpDeviceGUID, &m_lpDirectSound, NULL);
	m_lpDirectSound->SetCooperativeLevel(hWnd, DSSCL_NORMAL);
}

void CDSSound::SetWaveFormat(WORD wChannels, DWORD dSamplesPerSec, WORD wBitsPerSample)
{
	//
	//	设置捕获参数
	//
	wfx.wFormatTag		= WAVE_FORMAT_PCM;									//	默认PCM格式
	wfx.nChannels		= wChannels;										//	声道数量
	wfx.nSamplesPerSec	= dSamplesPerSec;									//	采样率 11025=11.025kHz
	wfx.nAvgBytesPerSec	= wChannels * dSamplesPerSec * wBitsPerSample / 8;	//	每秒样本数
	wfx.nBlockAlign		= wBitsPerSample * wChannels / 8;					//	字节对齐
	wfx.wBitsPerSample	= wBitsPerSample;
	wfx.cbSize			= 0;
}

void CDSSound::CreatePlayBuffer(DWORD dwSize)
{
	DSBUFFERDESC	dscBufferDesc;

	//
	//	缓冲区描述
	//
	dscBufferDesc.dwSize		= sizeof(DSBUFFERDESC);
	dscBufferDesc.dwFlags		= DSBCAPS_STATIC | DSBCAPS_STICKYFOCUS | DSBCAPS_GLOBALFOCUS;
	dscBufferDesc.dwBufferBytes	= dwSize;		//	缓冲区大小，设置为1s所需的大小
	dscBufferDesc.dwReserved	= 0;
	dscBufferDesc.lpwfxFormat	= &wfx;						//	设置录音用的wave格式

	HRESULT hr = m_lpDirectSound->CreateSoundBuffer(&dscBufferDesc, &m_lpDSB, 0);
	m_lpDSB->SetVolume(DSBVOLUME_MAX);
}

void CDSSound::PlaySound(LPVOID lpData, DWORD dwSize)
{
	if (!lpData || dwSize <= 0)
		return;

	CreatePlayBuffer(dwSize);

	LPVOID lpvPtr1;
	DWORD dwBytes1;
	
	HRESULT hr = m_lpDSB->Lock(0, 0, &lpvPtr1, &dwBytes1, 0, 0, DSBLOCK_ENTIREBUFFER);    
	if(DSERR_BUFFERLOST == hr) {
		m_lpDSB->Restore();
		hr = m_lpDSB->Lock(0, 0, &lpvPtr1, &dwBytes1, 0, 0, DSBLOCK_ENTIREBUFFER);
	}
	if(DS_OK == hr) {
		
		::CopyMemory(lpvPtr1, lpData, dwBytes1);
		m_lpDSB->Unlock(lpvPtr1, dwBytes1, 0, 0);
	}

	m_lpDSB->SetCurrentPosition(0);
	m_lpDSB->Play(0, 0, 0);
}