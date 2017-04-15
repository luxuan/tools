#coding=utf8
import sys, os
import base64
import requests, json

try:
    with open(os.path.join('config', 'baidu.json')) as f: token = json.loads(f.read())['token']
except:
    token = ''

def recognize(en_msg, size):
    url = 'http://vop.baidu.com/server_api'
    payloads = {
        'channel': 1,
        'rate': 8000,
        'format': 'wav',
        'cuid': '192.168.0.100',
        'lan': 'zh',
        'token': token,
        'speech': en_msg,
        'len': size
    }
    # print payloads
    headers = {"Content-Type": "application/json" }
    try:
        # CARE:should 'json=', not 'data='
        #r = json.loads(requests.post(url, json = payloads, headers = headers).text)
        r = json.loads(requests.post(url, json = payloads).text)
        # print r
        if r['err_no'] != 0:
            print >> sys.stderr, r['err_msg']
            return None
        # result contains 1-5 recognized text
        return r['result']
    except Exception as e:
        print e
        return

def recognize_by_wav(wav_name):
    with open(wav_name, 'rb') as f: audio = f.read()
    # CARE: replace \n, http://yuyin.baidu.com/bbs/q/2132
    en_audio = base64.encodestring(audio).replace('\n', '')
    # en_audio = base64.urlsafe_b64encode(audio)
    # print 'encode', en_text
    text = recognize(en_audio, len(audio))
    return text


def get_response(mp3_name):
    wav_name = mp3_name + ".wav"
    # convert to wav
    # http://blog.csdn.net/lw_power/article/details/51771267
    # http://blog.sina.com.cn/s/blog_613aa3c30100wu4x.html
    # cmd = 'lame --decode %s %s' % (mp3_name, wav_name)
    cmd = 'sox %s -r 8000 -c1 %s' % (mp3_name, wav_name)
    os.system(cmd)

    return recognize_by_wav(wav_name)


if __name__ == '__main__':
    while True:
        a = raw_input('>').decode(sys.stdin.encoding).encode('utf8')
        print(get_response(a, 'ItChat'))
