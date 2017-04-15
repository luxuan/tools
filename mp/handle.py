# -*- coding: utf-8 -*-
# filename: handle.py

import sys
import hashlib

import web

import reply
import receive

import tuling
import baidu

# fix file redict: UnicodeEncodeError: 'ascii' codec can't encode ...
reload(sys)
sys.setdefaultencoding("utf-8")

class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "xxxx" # your backend set

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument



    def POST(self):
        try:
            webData = web.data()
            #print "Handle Post webdata is ", webData   #后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if recMsg.MsgType == 'text' or recMsg.MsgType == 'voice':
                    try:
                        content = tuling.get_response(recMsg.Content)
                        #print 'reply: %s' % content
                        replyMsg = reply.TextMsg(toUser, fromUser, content)
                        return replyMsg.send()
                    except Exception, e:
                        print e
                if recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    return replyMsg.send()
                else:
                    return reply.Msg().send()
            else:
                print "暂且不处理"
                print recMsg
                return reply.Msg().send()
        except Exception, Argment:
            return Argment

