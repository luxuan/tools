#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import random
import time
import threading

import itchat
import tuling
import baidu

# fix file redict: UnicodeEncodeError: 'ascii' codec can't encode ...
reload(sys)
sys.setdefaultencoding("utf-8")

# TODO why print not work
logger = logging.getLogger('itchat')

def log(txt):
    now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    logger.info('[%s] %s' % (now, txt))


def filter_reply(text):
    if text == '我通过了你的朋友验证请求，现在我们可以开始聊天了':
        return [
            '@img@attachment/hi.gif',
            '很高兴认识你，么么哒~',
            '你可以用语音和我聊天哦'
        ]
    elif text == '刘斌' or text.find('刘斌') >= 0 and \
        (text.find('谁') >= 0 or text.find('吗') >= 0 or text.find('认识') >= 0):
        ws = [
            '哈哈哈，你猜刘斌是谁，我不告诉你',
            '刘斌是我酷帅酷帅的主人啦',
            '笨蛋，大名鼎鼎的刘斌都不知道，他是主人，哈哈'
        ]
        i = random.randint(0, 2)
        return ws[i]
    return None

def send_msg(texts, username):
    if type(texts) != type([]):
        texts = [texts]
    for text in texts:
        log('\treply: %s' % text.replace('\n', '\\n'))
        itchat.send(text, toUserName=username)

@itchat.msg_register(itchat.content.TEXT)
@itchat.msg_register(itchat.content.RECORDING)
def text_reply(msg):
    text = msg['Text']
    if msg['Type'] == itchat.content.RECORDING:
        mp3_name = "download/" + msg['FileName']
        msg['Text'](mp3_name)
        txts = baidu.get_response(mp3_name)
        log('recognized len: %d' % len(txts))
        text = txts[0]

    peer = msg['User']

    title = ''
    if msg['ToUserName'] == 'filehelper':
        title += 'Self'
    else:
        if peer['UserName'] == msg['ToUserName']:
            title += 'Send to >'
        # Uin, Sex, MsgId, CreateTime
        if peer['RemarkName']:
            title += '%(RemarkName)s(%(Province)s %(City)s)' % peer
        else:
            title += '%(NickName)s(%(Province)s %(City)s)' % peer
    log('%s: %s' % (title, text))

    if peer['UserName'] != msg['ToUserName'] or msg['ToUserName'] == 'filehelper':
        reply = filter_reply(text)
        if reply == None:
            reply = tuling.get_response(text)
        touser = msg['FromUserName']
        if msg['ToUserName'] == 'filehelper':
            touser = 'filehelper'
        send_msg(reply, touser)
        return


@itchat.msg_register(itchat.content.PICTURE)
def image_reply(msg):
    peer = msg['User']
    if peer['UserName'] != msg['ToUserName'] or msg['ToUserName'] == 'filehelper':
        touser = msg['FromUserName']
        if msg['ToUserName'] == 'filehelper':
            touser = 'filehelper'
        ws = [
            '哈哈哈~',
            '么么哒~~~~',
            '哥笑而不语'
        ]
        emotion = [
            '[憨笑]',
            '[偷笑]',
            '[微笑]'
        ]
        iw = random.randint(0, 2)
        ie = random.randint(0, 2)
        ne = random.randint(0, 5)
        reply = ws[iw] + (emotion[ie] * ne)
        send_msg(reply, touser)


@itchat.msg_register(itchat.content.SYSTEM)
def system_log(msg):
    pass
    #logger.info('system message:')
    #for k, v in msg.items():
    #    logger.info('%s: %s' % (k, v))

def heartbeat():
    text = 'heartbeat'
    while True:
        i = 0
        while i < 1800:
            log('wait for heartbeat')
            time.sleep(60)
            i += 60
        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        send_msg('[%s] %s' % (now, text), 'filehelper')


itchat.auto_login(enableCmdQR=2, hotReload=True)

t1 = threading.Thread(target=heartbeat)
t1.setDaemon(True)
t1.start()

itchat.run()
log('exit')
