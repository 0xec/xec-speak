#pragma once

#include <mmsystem.h>
#include <dsound.h>

#pragma comment(lib, "dsound.lib")
#pragma comment(lib, "dxguid.lib")

#define				NUM_REC_NOTIFICATIONS			3		//	设置缓冲区通知的次数

typedef VOID (CALLBACK *NOTIFYPROC)(LPVOID lpFrame, LPVOID lpData, DWORD dwSize);

class CDSCapture
{
public:
	CDSCapture(void);
	~CDSCapture(void);

protected:
	HANDLE						m_hNotificationEvent;		//	通知事件
	LPDIRECTSOUNDCAPTURE		m_lpSoundCapture;			//	捕获对象
	LPDIRECTSOUNDCAPTUREBUFFER	m_lpDSCB;					//	捕获缓冲区

	NOTIFYPROC					m_lpNotifyProc;				//	回调通知
	LPVOID						m_lpFrame;

	DWORD						m_dwBufferSize;				//	缓冲区大小
	DWORD						m_dwNotifySize;

	HANDLE						m_hExitEvent;
	HANDLE						m_hThread;

public:
	WAVEFORMATEX				wfx;						//	音频参数

protected:
	//
	//	接收通知点线程
	//
	static	DWORD	WINAPI	_threadRecvData(LPVOID lParameter);

public:
	//
	//	枚举声音采集设备
	//
	void	EnumDevices(LPDSENUMCALLBACK callback, LPVOID ctx);

	//
	//	打开设备
	//
	void	OpenDevice(LPGUID lpDeviceGUID, NOTIFYPROC callproc, LPVOID frame);

	//
	//	设置捕获参数
	//
	//	wChannel = 1 单声道， 2 立体声
	//	dSamplesPerSec = 采样率(每秒样本数量): 11025 = 11.025kHz (8000/11025/22050/44100/48000)
	//	wBitsPerSample	=	采样大小: 8即2^8采样大小, 16=2^16
	//
	//
	void	SetWaveFormat(WORD wChannels, DWORD dSamplesPerSec, WORD wBitsPerSample);

	//
	//	通知点触发，读取数据
	//
	void	RecordCapturedData();

	//
	//	开始捕获
	//
	void	StartCapture();

	//
	//	停止捕获
	//
	void	StopCapture();
};
