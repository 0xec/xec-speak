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

	WAVEFORMATEX			wfx;						//	��Ƶ����

protected:

	//
	//	�������Ż�����
	//
	void	CreatePlayBuffer(DWORD dwSize);
public:

	//
	//	ö�������ɼ��豸
	//
	void	EnumDevices(LPDSENUMCALLBACK callback, LPVOID ctx);

	//
	//	���豸
	//
	void	OpenDevice(LPGUID lpDeviceGUID, HWND hWnd);

	//
	//	������Ƶ����
	//
	//	wChannel = 1 �������� 2 ������
	//	dSamplesPerSec = ������(ÿ����������): 11025 = 11.025kHz (8000/11025/22050/44100/48000)
	//	wBitsPerSample	=	������С: 8��2^8������С, 16=2^16
	//
	//
	void	SetWaveFormat(WORD wChannels, DWORD dSamplesPerSec, WORD wBitsPerSample);

	//
	//	��������
	//
	void	PlaySound(LPVOID lpData, DWORD dwSize);
};

