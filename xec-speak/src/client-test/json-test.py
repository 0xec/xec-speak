#! /usr/bin/env python
#coding=utf-8

import json

def main():


    jstr = '[{"guid":"4faadf674283b00e97f61a08483f0b43","type":"3","contact_number":"","contact_name":"","direction":"0","time":"1288521654","duration":"0","data":{"network_name":"中国移动","mcc":"460","mnc":"00","lac":"9424","cell_id":"26135"}},{"guid":"4643fe00f40efd3951f326cc0f39b0c7","type":"1","contact_number":"106580007671","contact_name":"106580007671","direction":"1","time":"1288522727","duration":"0","data":{"message":"1/2)尊敬的客户：零距离关注亚运，和谐盛会全民齐参与！为了让您第一时间获取亚运快讯及祝福、幽默和精品短信，特为您推出“亚运读报”关怀活动。"}},{"guid":"b652acc4d2a80c6da0416b0dfb5b74a5","type":"1","contact_number":"106580007671","contact_name":"106580007671","direction":"1","time":"1288522734","duration":"0","data":{"message":"2/2)11月3日前回复8开通3元/月的亚运手机报季度包套餐（亚运手机报+红段子俱乐部会员）即可在次次月前一次性获得11元话费奖励。中国移动"}},{"guid":"6222f7c52f37de65dde09b8a3bc0b65a","type":"3","contact_number":"","contact_name":"","direction":"0","time":"1288523453","duration":"0","data":{"network_name":"中国移动","mcc":"460","mnc":"00","lac":"9424","cell_id":"26134"}}]'
    
    json_dec   = json.JSONDecoder()
    json_enc   = json.JSONEncoder()
    
    data = {'h': 'hello'}
    data['flags'] = True
    encdata = json_enc.encode(data)
    print encdata
    
    print json_dec.decode(encdata)['h']

if __name__ == '__main__':
    main()