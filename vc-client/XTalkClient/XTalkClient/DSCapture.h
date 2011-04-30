#pragma once

#include <mmsystem.h>
#include <dsound.h>

#pragma comment(lib, "dsound.lib")
#pragma comment(lib, "dxguid.lib")

#define				NUM_REC_NOTIFICATIONS			3		//	���û�����֪ͨ�Ĵ���

typedef VOID (CALLBACK *NOTIFYPROC)(LPVOID lpFrame, LPVOID lpData, DWORD dwSize);

class CDSCapture
{
public:
	CDSCapture(void);
	~CDSCapture(void);

protected:
	HANDLE						m_hNotificationEvent;		//	֪ͨ�¼�
	LPDIRECTSOUNDCAPTURE		m_lpSoundCapture;			//	�������
	LPDIRECTSOUNDCAPTUREBUFFER	m_lpDSCB;					//	���񻺳���

	NOTIFYPROC					m_lpNotifyProc;				//	�ص�֪ͨ
	LPVOID						m_lpFrame;

	DWORD						m_dwBufferSize;				//	��������С
	DWORD						m_dwNotifySize;

	HANDLE						m_hExitEvent;
	HANDLE						m_hThread;

public:
	WAVEFORMATEX				wfx;						//	��Ƶ����

protected:
	//
	//	����֪ͨ���߳�
	//
	static	DWORD	WINAPI	_threadRecvData(LPVOID lParameter);

public:
	//
	//	ö�������ɼ��豸
	//
	void	EnumDevices(LPDSENUMCALLBACK callback, LPVOID ctx);

	//
	//	���豸
	//
	void	OpenDevice(LPGUID lpDeviceGUID, NOTIFYPROC callproc, LPVOID frame);

	//
	//	���ò������
	//
	//	wChannel = 1 �������� 2 ������
	//	dSamplesPerSec = ������(ÿ����������): 11025 = 11.025kHz (8000/11025/22050/44100/48000)
	//	wBitsPerSample	=	������С: 8��2^8������С, 16=2^16
	//
	//
	void	SetWaveFormat(WORD wChannels, DWORD dSamplesPerSec, WORD wBitsPerSample);

	//
	//	֪ͨ�㴥������ȡ����
	//
	void	RecordCapturedData();

	//
	//	��ʼ����
	//
	void	StartCapture();

	//
	//	ֹͣ����
	//
	void	StopCapture();
};
