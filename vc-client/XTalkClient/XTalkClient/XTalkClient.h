// XTalkClient.h : PROJECT_NAME Ӧ�ó������ͷ�ļ�
//

#pragma once

#ifndef __AFXWIN_H__
	#error "�ڰ������ļ�֮ǰ������stdafx.h�������� PCH �ļ�"
#endif

#include "resource.h"		// ������


// CXTalkClientApp:
// �йش����ʵ�֣������ XTalkClient.cpp
//

class CXTalkClientApp : public CWinApp
{
public:
	CXTalkClientApp();

// ��д
	public:
	virtual BOOL InitInstance();

// ʵ��

	DECLARE_MESSAGE_MAP()
};

extern CXTalkClientApp theApp;