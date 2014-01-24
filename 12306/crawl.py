# -*- coding: utf-8 -*- 
# Author: luxuan@github.com

from urllib.request import urlopen
import json
import time
import sys

def get_url(train_date, from_station, to_station, is_student=False):
    param = {
        'train_date': train_date,
        'from_station': from_station,
        'to_station': to_station,
        'purpose_codes': is_student and '0X00' or 'ADULT'
    }
    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=%(train_date)s&leftTicketDTO.from_station=%(from_station)s&leftTicketDTO.to_station=%(to_station)s&purpose_codes=%(purpose_codes)s' % param
    return url

def get_html(url, data_key='data'):
    html = urlopen(url).read()
    html = html.decode()
    return json.loads(html)[data_key]

def check_ticket(url, should_sit=False):
    for line in get_html(url):
        train = line['queryLeftNewDTO']
        rw = train['rw_num']  # ruan wo
        yw = train['yw_num']  # ying wo
        rz = train['rz_num']  # wu zuo
        yz = train['yz_num']  # ying zuo
        wz = train['wz_num']  # wu zuo
        #print('wz', wz, not should_sit and wz not in no_ticket_tag)
        no_ticket_tag = ('无', '--')
        if rw not in no_ticket_tag or yw not in no_ticket_tag \
        or rz not in no_ticket_tag or yz not in no_ticket_tag \
        or not should_sit and wz not in no_ticket_tag:
            return True

def main(trains):
    while True:
        for train in  trains:
            is_student = 'is_student' in train and train['is_student'] or False
            should_sit = 'should_sit' in train and train['should_sit'] or False
            url = get_url(train['date'], train['from'], train['to'], is_student)
            if check_ticket(url, should_sit):
                print()
                print('got ticket', train, time.strftime('%X %m-%d', time.localtime()), '\x07')
            else:
                #print(time.strftime('%X %m-%d', time.localtime()))
                print('.', end='')
                sys.stdout.flush()
        time.sleep(1)

if __name__ == '__main__':
    train_tasks = [
        #{'date': '2014-02-09', 'from': 'SYQ', 'to': 'GZQ' },
        {'date': '2014-02-09', 'from': 'SYQ', 'to': 'HZH', 'is_student': True, 'should_sit': True }
    ]
    main(train_tasks)