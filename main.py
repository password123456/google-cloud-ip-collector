__author__ = 'https://github.com/password123456/'

import os
import sys
import importlib
import json
import requests
import csv
from datetime import datetime

importlib.reload(sys)

_today_ = datetime.today().strftime('%Y-%m-%d')
_ctime_ = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

_home_path_ = 'F:/code/pythonProject/collect_cloud_ips'
_db_ = '%s/db/%s-cloud_ipinfo.csv' % (_home_path_, _today_)

_headers_ = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) \
             Chrome/49.0.2623.112 Safari/537.36', 'Content-Type': 'application/json; charset=utf-8'}


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def collect_google_cloud_ips():

    _url = 'https://www.gstatic.com/ipranges/cloud.json'
    _google_file = '%s/google.json' % _home_path_
    _name_ = 'GOOGLE'

    if os.path.exists(_google_file):
        create_time = os.stat(_google_file).st_ctime
        google_file_datetime = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d')
        today = datetime.now().date()

        if str(google_file_datetime) == str(today):
            get_google_cloud = True
        else:
            get_google_cloud = False
    else:
        print('%s[+] Download New %s Cloud File%s' % (Bcolors.OKGREEN, _name_, Bcolors.ENDC))
        r = requests.get(_url, headers=_headers_, verify=True)
        if r.status_code == 200:
            body = r.text
            with open(_google_file, 'w') as f:
                f.write(body)
            f.close()
            get_google_cloud = True
        else:
            res_status = r.status_code
            message = '**%s_Cloud Collector**\n▶ Connection Error: http %s\n' % (_name_, res_status)
            print(message)
            sys.exit(1)

    if not get_google_cloud:
        print('%s[+] Downloaded %s Cloud File Found.%s' % (Bcolors.OKGREEN, _name_, Bcolors.ENDC))
        r = requests.get(_url, headers=_headers_, verify=True)
        if r.status_code == 200:
            body = r.text
            with open(_google_file, 'w') as f:
                f.write(body)
            f.close()
        else:
            res_status = r.status_code
            message = '**%s_Cloud Collector**\n▶ Connection Error: http %s\n' % (_name_, res_status)
            print(message)
            sys.exit(1)
        r.close()

    with open(_google_file, 'r') as google_file:
        if os.path.exists(_db_):
            mode = 'a'
            header = True
        else:
            mode = 'w'
            header = False

        fa = open(_db_, mode)
        writer = csv.writer(fa, delimiter=',', lineterminator='\n')

        if not header:
            writer.writerow(['datetime', 'platform', 'create_time', 'region', 'ip_prefix', 'service'])

        y = json.load(google_file)
        n = 0

        create_time = datetime.strptime(y['creationTime'], '%Y-%m-%dT%H:%M:%S.%f')
        print('%s[+] Collect Google Cloud IP Prefixes.%s' % (Bcolors.OKGREEN, Bcolors.ENDC))

        for item in y['prefixes']:
            if 'ipv4Prefix' in item:
                n = n + 1
                ip_prefix = item['ipv4Prefix']
                service = item['service']
                region = item['scope']
                try:
                    writer.writerow([_ctime_, 'google', create_time, region, ip_prefix, service])
                    sys.stdout.write('\r ----> Processing... %d lines' % n)
                    sys.stdout.flush()
                except KeyboardInterrupt:
                    sys.exit(0)
                except Exception as e:
                    print('%s- Exception::%s%s' % (Bcolors.WARNING, e, Bcolors.ENDC))
        fa.close()
    google_file.close()
    print('\n')


def main():
    collect_google_cloud_ips()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print('%s- Exception::%s%s' % (Bcolors.WARNING, e, Bcolors.ENDC))
