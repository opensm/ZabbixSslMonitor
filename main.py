# coding: utf-8
from urllib3.contrib import pyopenssl as reqs
from datetime import datetime
import sys
import getopt


def get_expire_time(url):
    cert = reqs.OpenSSL.crypto.load_certificate(
        reqs.OpenSSL.crypto.FILETYPE_PEM,
        reqs.ssl.get_server_certificate((url, 443))
    )

    notafter = datetime.strptime(cert.get_notAfter().decode()[0:-1], '%Y%m%d%H%M%S')  # 获取到的时间戳格式是ans.1的，需要转换
    remain_days = notafter - datetime.now()  # 用证书到期时间减去当前时间
    print(remain_days.days)  # 获取剩余天数


def useage():
    print("%s -f\t#检查domain" % sys.argv[0])
    print("%s -h\t#帮助文档" % sys.argv[0])


def main():
    if len(sys.argv) == 1:
        useage()
        sys.exit(1)
    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            "f:h"
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
    elif "-f" in command_dict:
        command_data['url'] = command_dict.get('-f')
        get_expire_time(**command_data)
    else:
        useage()
        sys.exit(1)


if __name__ == '__main__':
    main()
