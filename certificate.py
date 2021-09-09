#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author: shaoqiang

# 此脚本用来获取https证书过期时间，需要先执行pip3 install pyopenssl

from urllib3.contrib import pyopenssl as reqs
from datetime import datetime
import sys
import getopt


# 公网验证
def get_notafter(url):
    # 输出结果
    try:
        cert = reqs.OpenSSL.crypto.load_certificate(
            reqs.OpenSSL.crypto.FILETYPE_PEM,
            reqs.ssl.get_server_certificate((url, 443))
        )

        notafter = datetime.strptime(cert.get_notAfter().decode()[0:-1], '%Y%m%d%H%M%S')
        remain_days = notafter - datetime.now()
        print(remain_days.days)
    except Exception as e:
        print("出现错误，请检查域名是否正确或者可达性，{}".format(e))


def get_domain_list():
    import json
    domain = {
        "data": [
            {"{#DOMAIN}": "www.baidu.com"},
        ]
    }
    print(json.dumps(domain, sort_keys=True, indent=2))


def useage():
    print("%s -w\t#检查domain" % sys.argv[0])
    print("%s -d\t#输出域名列表" % sys.argv[0])
    print("%s -h\t#帮助文档" % sys.argv[0])


def main():
    if len(sys.argv) == 1:
        useage()
        sys.exit(1)
    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            "w:hd"
        )
    except getopt.GetoptError:
        print("%s -h" % sys.argv[0])
        sys.exit(1)
    command_dict = dict(options)
    command_data = dict()
    # 帮助
    if '-h' in command_dict:
        useage()
        sys.exit(1)
    # 获取监控项数据
    elif "-w" in command_dict:
        command_data['url'] = command_dict.get('-w')
        get_notafter(**command_data)
    elif "-d" in command_dict:
        get_domain_list()
    else:
        useage()
        sys.exit(1)


if __name__ == '__main__':
    main()
