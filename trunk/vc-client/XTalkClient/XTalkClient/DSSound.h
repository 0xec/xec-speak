#pragma once

#include <mmsystem.h>
#include <dsound.h>

#pragma comment(lib, "dsound.lib")
#pragma comment(lib, "dxguid.lib")

class CDSSound
{
public:
	CDSSound(void);
	~CDSSound(void);

protected:
	LPDIRECTSOUNDBUFFER		m_lpDSB;
	LPDIRECTSOUND			m_lpDirectSound;

	WAVEFORMATEX			wfx;						//	音频参数

protected:

	//
	//	创建播放缓冲区
	//
	void	CreatePlayBuffer(DWORD dwSize);
public:

	//
	//	枚举声音采集设备
	//
	void	EnumDevices(LPDSENUMCALLBACK callback, LPVOID ctx);

	//
	//	打开设备
	//
	void	OpenDevice(LPGUID lpDeviceGUID, HWND hWnd);

	//
	//	设置音频参数
	//
	//	wChannel = 1 单声道， 2 立体声
	//	dSamplesPerSec = 采样率(每秒样本数量): 11025 = 11.025kHz (8000/11025/22050/44100/48000)
	//	wBitsPerSample	=	采样大小: 8即2^8采样大小, 16=2^16
	//
	//
	void	SetWaveFormat(WORD wChannels, DWORD dSamplesPerSec, WORD wBitsPerSample);

	//
	//	播放声音
	//
	void	PlaySound(LPVOID lpData, DWORD dwSize);
};

