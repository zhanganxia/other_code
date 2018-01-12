# coding:utf-8

# 图片验证码在redis中保存的有效期 单位：秒
IMAGE_CODE_REDIS_EXPIRES = 300

# 短信验证码在redis中保存的有效期 单位：秒
SMS_CODE_REDIS_EXPIRES = 300

# 验证码短信模板编号
SMS_CODE_TEMPLATE = 1

# 两次发送短信验证码的时间间隔，单位：秒
SEND_SMS_CODE_INTERVAL = 60