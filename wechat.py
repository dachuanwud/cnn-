# wechat
# by lishechuan
import itchat, time, requests, random
import re, json, urllib.request, urllib.parse
import base64
import os
import subprocess,threading
import pydub
from pydub import AudioSegment
from itchat.content import *
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from city import city
replied = []
picture = []
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
### 对传输的文字的处理


#itchat.send('Hello, filehelper', toUserName='filehelper')
@itchat.msg_register(TEXT)
def text_reply(msg):
    if '我爱你' in msg['Text'] and msg['FromUserName']:
        itchat.send('我也爱你，宝贝！', msg['FromUserName'])
        a = random.randint(1, 5000)
        itchat.send('@img@%s' % '%s.jpg' % a, msg['FromUserName'])
        sendGreeting(msg)

    if '天气' in msg['Text'] and msg['FromUserName']:
        citycode = city.get(msg['Text'][3:])
        if citycode:
            url = ('http://www.weather.com.cn/data/cityinfo/%s.html' % citycode)
            a = requests.get(url)
            itchat.send(a.content.decode('utf-8'), msg['FromUserName'])

    if '下载' in msg['Text'] and msg['FromUserName']:
        print(filename)
        itchat.send('@img@%s' % filename, msg['FromUserName'])
    if '全部' in msg['Text'] and msg['FromUserName']:
        for filename1 in picture:
            itchat.send('@img@%s' % filename1, msg['FromUserName'])

### 对传输的文字处理的结束

### 下载信息的函数，isGroupChat=Ture 是判断群聊
@itchat.msg_register([PICTURE, ATTACHMENT, VIDEO], isGroupChat=True)  # 上传信息
def download_files(msg):
    msg['Text'](msg['FileName'])
    print(msg['FileName'])
    filename = msg['FileName']
    picture.append(filename)
    # itchat.send('上传到服务器成功',msg['FromUserName'])
    # print({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'))


@itchat.msg_register([PICTURE, ATTACHMENT, VIDEO])
def groupchat_reply(msg):
    global filename
    global dataname
    msg['Text'](msg['FileName'])
    friend = itchat.search_friends(userName=msg['FromUserName'])
    dataname = friend['RemarkName']
    print(dataname)
    filename = msg['FileName']
    print(filename)
    save(filename)
    # picture.append(filename)
    # itchat.send('上传到服务器成功',msg['FromUserName'])
    # itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])
### 函数结束

### 语音处理模块
@itchat.msg_register(RECORDING)  # 语音处理
def yuyin(msg):
    msg['Text'](msg['FileName'])
    yuyinname = msg['FileName']
    print(yuyinname)
    word1 = yuyinshibie(yuyinname)
    if '家' in word1 or '家庭' in word1:
        itchat.send('请稍等，宝贝！', msg['FromUserName'])
    if '进行监控' in word1:
        subprocess.Popen('python3 /home/dachuan/PycharmProjects/untitled1/camera_reader.py', shell=True,
                         stdout=subprocess.PIPE)
    if '谁' in word1 or '房间' in word1:
        fp = open('warning.txt','r')
        a =fp.read()
        fp.close()
        itchat.send('%s'%a, msg['FromUserName'])
        #subprocess.Popen('python3 /home/dachuan/PycharmProjects/untitled1/camera_reader.py',shell=True,stdout=subprocess.PIPE)

    if '天气' in word1 or '天' in word1:
        citycode = city.get('桂林')
        if citycode:
            url = ('http://www.weather.com.cn/data/cityinfo/%s.html' % citycode)
            a = requests.get(url)
            itchat.send(a.content.decode('utf-8'), msg['FromUserName'])
    if '笑话' in word1 or '话' in word1 or '讲' in word1:
        itchat.send('请稍等，宝贝！', msg['FromUserName'])
        sendGreeting(msg)
    if '图片' in word1 or '美' in word1:
        a = random.randint(1, 5000)
        itchat.send('@img@%s' % '%s.jpg' % a, msg['FromUserName'])
    if '分析微信好友' in word1 or '分析' in word1 or '好友' in word1:
        friendList = itchat.get_friends(update=True)[1:]
        sexDict = {}
        total = len(friendList)
        print(friendList[0].keys())
        # print(friendList[0]['NickName'].encode('utf-8').decode())
        for friend in friendList:
            if not friend['Sex'] in sexDict:
                sexDict[friend['Sex']] = []
            sexDict[friend['Sex']].append(friend['NickName'] + ' ' + friend['DisplayName'])
            print(friend['PYInitial'])
        unkonw = len(sexDict[0])
        male = len(sexDict[1])
        female = len(sexDict[2])
        print('您共有%d位好友，其中未知性别好友%d,其中男性性别的好友%d位，女性性别的好友%d\n' % (total, unkonw, male, female))
        print('未知性别的好友是：\n')
        for name in sexDict[0]:
            print(name)
        print('男性的好友是：\n')
        for name in sexDict[1]:
            print(name)
        print('女性的好友是：\n')
        for name in sexDict[2]:
            print(name)

# 传入 picture ID写入文件
def save(data):
    # 组装为 json 格式
    dic = {}
    dic['%s' % dataname] = data

    repost_data_str = json.dumps(dic)
    with open('shujuku.txt', 'a+') as f:
        f.write('\n')
        f.write(repost_data_str)
    print('successly save')


def yuyinshibie(M):  # 语音识别模块
    # 设置应用信息
    baidu_server = "https://openapi.baidu.com/oauth/2.0/token?"
    grant_type = "client_credentials"
    client_id = "j9GxSBiT7haIAqv8kvWsn9Xp"  # 填写API Key
    client_secret = "3f0f1cbd27e5e6d5849ff4a4cacebf4b"  # 填写Secret Key
    # 合成请求token的URL
    url = baidu_server + "grant_type=" + grant_type + "&client_id=" + client_id + "&client_secret=" + client_secret
    # 获取token
    res = urllib.request.urlopen(url).read().decode('UTF-8')
    # print(res)
    # print(type(res))
    data = json.loads(res)
    token = data["access_token"]
    # print (token)
    # MP3 --WAV
    song = AudioSegment.from_mp3(M)
    a = song.export("mashup.wav", format="wav")
    # print(type(a))
    # 设置音频属性，根据百度的要求，采样率必须为8000，压缩格式支持pcm（不压缩）、wav、opus、speex、amr
    VOICE_RATE = 8000
    WAVE_FILE = "mashup.wav"  # 音频文件的路径
    USER_ID = "hail_hydra"  # 用于标识的ID，可以随意设置
    WAVE_TYPE = "wav"
    # 打开音频文件，并进行编码
    f = open(WAVE_FILE, "rb")
    speech = base64.b64encode(f.read()).decode('UTF-8')
    # print(type(speech))
    size = os.path.getsize(WAVE_FILE)
    update = json.dumps(
        {"format": WAVE_TYPE, "rate": VOICE_RATE, 'channel': 1, 'cuid': USER_ID, 'token': token, 'speech': speech,
         'len': size})
    headers = {'Content-Type': 'application/json'}
    url = "http://vop.baidu.com/server_api"
    # print(type(url))
    req = urllib.request.Request(url, update.encode('UTF-8'), headers)
    r = urllib.request.urlopen(req)
    t = r.read().decode('UTF-8')
    result = json.loads(t)
    # print (result)
    if result['err_msg'] == 'success.':
        word = result['result'][0]
        if word != '':
            if word[len(word) - 3:len(word)] == '，':
                print(word[0:len(word) - 3])
            else:
                print(word)
        else:
            print("音频文件不存在或格式错误")
    else:
        print("错误")
    return word


def sendGreeting(msg):
    global replied
    friend = itchat.search_friends(userName=msg['FromUserName'])
    itchat.send((friend['RemarkName'] + '这是给你准备的笑话，愿你开心每一天！！！     笑话：' + getRandomGreeting()), msg['FromUserName'])
    replied.append(msg['FromUserName'])

def getRandomGreeting():
    jokePage = requests.get('http://www.jokeji.cn/list.htm')
    jokeList = re.findall('/jokehtml/[\w]+/[0-9]+.htm', jokePage.text)  # 使用正则表达式找到所有笑话页面的链接
    jokePage.encoding = 'gbk'
    for jokeLink in jokeList:
        jokeContent = requests.get('http://www.jokeji.cn/' + jokeLink)  # 访问第一个链接
        jokeContent.encoding = 'gbk'
        jokes = re.findall('<P>[0-9].*</P>', jokeContent.text)
    random.shuffle(jokes)
    return jokes[1][5:-1]
def saysafe():
    print('li')
    with open('warning.txt', 'r') as f:
        a = f.read()
        if a == 'chuan':
            itchat.send('you wai ren !')
    global t
    t = threading.Timer(15.0, saysafe)
    t.start()

### 自动加好友
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text'])  # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])
### 自动加好友模块结束



itchat.auto_login(hotReload=True)
t = threading.Timer(15.0, saysafe)
t.start()

itchat.run()
