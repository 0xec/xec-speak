// XTalkClientDlg.h : ͷ�ļ�
//

#pragma once
#include "afxcmn.h"

#include "DSCapture.h"
#include "DSSound.h"

// CXTalkClientDlg �Ի���
class CXTalkClientDlg : public CDialog
{
// ����
public:
	CXTalkClientDlg(CWnd* pParent = NULL);	// ��׼���캯��

// �Ի�������
	enum { IDD = IDD_XTALKCLIENT_DIALOG };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV ֧��

	void InitializeUI();

	static BOOL CALLBACK DSEnumCallback(LPGUID lpGuid, LPCTSTR lpcstrDescription, LPCSTR lpcstrModule, LPVOID lpContext);

// ʵ��
protected:
	HICON m_hIcon;

	// ���ɵ���Ϣӳ�亯��
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()
public:
	CDSCapture	m_dsCapture;
	CDSSound	m_dsSound;
};
