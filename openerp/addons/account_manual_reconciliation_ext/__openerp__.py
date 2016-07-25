# -*- coding: utf-8 -*-

{
    "name": "手动核销扩展",
    "description":
        """
2016-04-13 补丁更新说明：
    1) 手动核销界面中业务伙伴文本显示换为下拉选择
    2) 去掉原有的 退出 按钮功能
    3) 部分翻译修正

2016-07-25 补丁更新说明：
    1) 修正了反核销操作,res.partner的最后核销时间字段未修正导致下次无法在手动核销中找到该partner
    2) 添加手动核销界面中的下拉框中业务伙伴的序号
    3) 记录上次准备核销的业务伙伴,防止用户忘记上次操作的业务伙伴
        """,
    'author': "EricChang",
    'website': "",

    "category": "web",
    "version": "8.0.0.1",
    "depends": ['account'],
    "data": [
        'views/account_manual_reconciliation_ext_js.xml',
    ],
    "qweb": [
        "static/src/xml/*.xml",
    ],
    'installable': True,
    'application': False,
}
