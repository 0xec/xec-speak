// XTalkClientDlg.h : 头文件
//

#pragma once
#include "afxcmn.h"

#include "DSCapture.h"
#include "DSSound.h"

// CXTalkClientDlg 对话框
class CXTalkClientDlg : public CDialog
{
// 构造
public:
	CXTalkClientDlg(CWnd* pParent = NULL);	// 标准构造函数

// 对话框数据
	enum { IDD = IDD_XTALKCLIENT_DIALOG };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV 支持

	void InitializeUI();

	static BOOL CALLBACK DSEnumCallback(LPGUID lpGuid, LPCTSTR lpcstrDescription, LPCSTR lpcstrModule, LPVOID lpContext);

// 实现
protected:
	HICON m_hIcon;

	// 生成的消息映射函数
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()
public:
	CDSCapture	m_dsCapture;
	CDSSound	m_dsSound;
};
