# -*- coding: utf-8 -*-

{
    "name": "报销单上直接选择付款方式",
    "description":
        """
                                人力资源费用报销单上直接选择付款方式
        """,
    'author': "jacky@osbzr.com,jason@osbzr.com",
    'website': "http://",

    "category": "osbzr",
    "version": "8.0.0.1",
    "depends": [
                'hr_expense','base'
                ],
    "data" : [
              'osbzr_expense.xml'
        ],
    'installable': True,
    'application': False,
}