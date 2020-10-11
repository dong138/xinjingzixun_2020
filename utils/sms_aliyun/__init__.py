#!/usr/bin/env python
# coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

client = AcsClient('LTAI4GJcCBqAEs63nNVNsJ63', 'hZXTnGJvkT54E6bqYH4jwAJO5Tc9Mx', 'cn-hangzhou')

request = CommonRequest()
request.set_accept_format('json')
request.set_domain('dysmsapi.aliyuncs.com')
request.set_method('POST')
request.set_protocol_type('https')  # https | http
request.set_version('2017-05-25')
request.set_action_name('SendSms')

request.add_query_param('RegionId', "cn-hangzhou")
request.add_query_param('PhoneNumbers', "13146060336")
request.add_query_param('SignName', "dong4716138")
request.add_query_param('TemplateCode', "SMS_167532197")
request.add_query_param('TemplateParam', "{\"code\":\"112233\"}")

response = client.do_action(request)
# python2:  print(response)
print(str(response, encoding='utf-8'))
