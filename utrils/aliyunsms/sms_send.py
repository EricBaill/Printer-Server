import uuid
import json
from aliyunsdkcore.client import AcsClient


# 注意：不要更改
from utrils.aliyunsms.aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest

REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"


#阿里大鱼相关配置
ACCESS_KEY_ID = 'LTAItcQwAaf9Lgou'
ACCESS_KEY_SECRET = 'JYNuR0JEYzK9FRB4W0dGeXlZwWY206'
SING_NAME = "上海蒹信网络科技"
TEMPLATE_CODE = "SMS_121910923"

acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
# region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


def send_sms(phone_numbers, template_param=None):
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(TEMPLATE_CODE)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    business_id = uuid.uuid1()
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(SING_NAME)

    # 数据提交方式
    # smsRequest.set_method(MT.POST)

    # 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    # TODO 业务处理

    return smsResponse


if __name__ == '__main__':

    # print(__business_id)
    params = {
        'code': 1234
    }
    # params = u'{"name":"wqb","code":"12345678","address":"bz","phone":"13000000000"}'
    print(send_sms("13xxxxxxxxx", json.dumps(params)))