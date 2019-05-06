from bs4 import BeautifulSoup
import requests
import random
import re
import time
import hashlib
# 教务系统首页121.251.136.100
session = requests.session()
cookieValue = ''
hostUrl = 'http://121.251.136.100/jwxt'
host = '121.251.136.100'
code = '13995'
origin = 'http://121.251.136.100'


def _md5(src):
    """
    md5加密方法
    """
    md = hashlib.md5()
    md.update(src.encode(encoding='utf-8'))
    return md.hexdigest()


def saveImgae(name,data):
    """
    保存图片，考虑到图片大小不一致，需要睡眠的时间长短不一，若抓取不成功，可能为网络原因
    :param name: 保存图片的名称
    :param data: 图片数据
    :return:
    """
    with open(name + '.jpg', 'wb') as fp:
        fp.write(data)
    time.sleep(10)


def getCode(url, cookie):
    """
    保存验证码
    :param url: 验证码获取地址
    :param cookie: cookie信息
    :return:
    """
    cookieValue = 'ASP.NET_SessionId='+str(cookie)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        'Cookie': cookieValue,
        'Referer': hostUrl + '/_data/login_new.aspx',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Host': host,
    }
    response = requests.get(url=url, headers=headers)
    saveImgae("yzm", response.content)

def getCookie(response):
    """
    根据响应数据获取cookie
    :param response:
    :return:
    """
    cookieJar = response.cookies
    cookieDict = requests.utils.dict_from_cookiejar(cookieJar)
    return cookieDict['ASP.NET_SessionId']


def login(username,password):
    """
    登录方法 主要为了获取session
    :return:
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }
    response = requests.get(url=hostUrl, headers=headers) #访问主页获取cookie
    cookie = getCookie(response)
    # 访问登录地址的headers 获取登录的额外参数
    _login_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        'Cookie': str(cookie),
        'Referer': hostUrl + '/_data/login_new.aspx',
    }
    login_home_url = hostUrl + "/_data/login_new.aspx"
    _login_response = requests.get(url=login_home_url, headers=_login_headers)
    VIEWSTATE = re.search(r'<input type="hidden" name="__VIEWSTATE" value="(.*)"', _login_response.text).group(1)
    # 根据cookie信息获取验证码，并保存
    code_url = hostUrl+"/sys/ValidateCode.aspx?t=" + str(random.randint(0, 999))
    getCode(url=code_url, cookie=str(cookie))
   
    yzm = str(input("请输入验证码："))
    password_encode = _md5((username + _md5(password)[0:30].upper() + code))[0:30].upper()
    code_encode = _md5((_md5(yzm.upper())[0:30].upper() + code))[0:30].upper()
    global cookieValue
    cookieValue = 'ASP.NET_SessionId=' + str(cookie)
    viewstate = VIEWSTATE
    login_data = {
        '__VIEWSTATE': viewstate,
        'pcInfo': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36undefined5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36 SN:NULL',
        'typeName': 'ѧ��',
        'dsdsdsdsdxcxdfgfg': password_encode,
        'fgfggfdgtyuuyyuuckjg': code_encode,
        'Sel_Type': 'STU',
        'txt_asmcdefsddsd': username,
        'txt_pewerwedsdfsdff': '',
        'txt_sdertfgsadscxcadsads': '',
    }
    login_headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        'Cookie': cookieValue,
        'Referer': hostUrl + '/_data/login_new.aspx',
        'Origin': origin,
        'host': host,
        'Connection': 'keep-live',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }
    global session
    login_url = hostUrl + "/_data/login_new.aspx"
    response = session.post(url=login_url, data=login_data, headers=login_headers)


def getScore():
    """
    获取成绩列表
    :return:
    """
    xnxq = input("成绩：请输入学期学年（如20160表示2016-2017学年第一学期）：")
    type = input("请选择成绩类型：（0为原始成绩，1为有效成绩）:")
    # 按照教务系统处理的方式 先出处理请求页面 再进行图片页面的请求
    _score_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': cookieValue,
        'Host': host,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Origin': origin,
        'Referer': hostUrl + '/xscj/Stu_MyScore_rpt.aspx',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    }
    score_data = {
        'sel_xn': xnxq[0:4],
        'sel_xq': xnxq[4:],
        'SJ': type,
        'btn_search': "检索".encode(),
        'SelXNXQ': '2',
        'zfx_flag': '0',
        'zxf': '0'
    }
    _score_url = hostUrl + "/xscj/Stu_MyScore_rpt.aspx"
    _score_response = session.post(url=_score_url, data=score_data,headers=_score_headers)
    # 获取请求回来的内容，进行数据的拆分，获取图片地址进行重新请求
    html = BeautifulSoup(_score_response.content, 'html.parser')
    score_url = hostUrl +"/xscj/" + html.find_all('img')[0].attrs['src']
    score_headers = {
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': cookieValue,
        'Host': host,
        'Connection': 'keep-alive',
        'Referer': hostUrl + '/xscj/Stu_MyScore_rpt.aspx',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    }
    score_response = session.get(url=score_url,headers=score_headers)
    saveImgae("score-"+xnxq+"-"+type,score_response.content)

def getCourse():
    """
    获取课程表
    :return:
    """
    xnxq = input("课表：请输入学年学期（20160表示2016-2016学年第一学期：）")
    _str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    s = "".join(random.sample(_str, 15))
    hidsjyzm = _md5(code + xnxq + s).upper()
    _course_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': cookieValue,
        'Host': host,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Origin': origin,
        'Referer': hostUrl + '/frame/menu.aspx',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    }
    _course_response = session.get(hostUrl + "/znpk/Pri_StuSel.aspx", headers=_course_headers)
    hidyzm = BeautifulSoup(_course_response.content, 'html.parser').find('input', {'name': {'hidyzm'}}).attrs['value']
    _course_data = {
        'Sel_XNXQ': xnxq,
        'rad': '0',
        'px': '0',
        'txt_yzm': '',
        'hidyzm': hidyzm,
        'hidsjyzm': hidsjyzm,
    }
    _course_url = hostUrl + '/znpk/Pri_StuSel_rpt.aspx?m=' + s
    _cs_header = {
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Length': '115',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookieValue,
        'Host': host,
        'Origin': origin,
        'Connection': 'keep-alive',
        'Referer': hostUrl + '/znpk/Pri_StuSel.aspx',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    }
    resp = session.post(url=_course_url, data=_course_data, headers=_cs_header)
    html = BeautifulSoup(resp.content, 'html.parser')
    course_url = hostUrl + "/znpk/" + html.find_all('img')[0].attrs['src']
    course_header = {
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': cookieValue,
        'Host': host,
        'Connection': 'keep-alive',
        'Referer': hostUrl + '/znpk/Pri_StuSel_rpt.aspx?m=' + s,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    }
    course_response = session.get(
        url=course_url,
        headers=course_header)
    saveImgae("kb-"+xnxq , course_response.content)


def getExam():
    xnxq = input("考试安排：请输入学期学年（如20160表示2016-2017学年第一学期）：")
    _ks_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': cookieValue,
        'Host': host,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Origin': 'http://121.251.136.100',
        'Referer': hostUrl + '/KSSW/stu_ksap.aspx',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    }
    _ks_data = {
        'sel_xnxq': xnxq,
        'sel_lcxz': '',
        'sel_lc': '',
        'btn_search': "检索".encode(),
    }
    _ks_url = hostUrl + "/KSSW/stu_ksap_rpt.aspx"
    _ks_resp = session.post(url=_ks_url, headers=_ks_headers, data=_ks_data);
    html = BeautifulSoup(_ks_resp.content, 'html.parser')
    url = hostUrl + "/KSSW/" + html.find_all('img')[0].attrs['src']
    ks_headers = {
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': cookieValue,
        'Host': host,
        'Connection': 'keep-alive',
        'Referer': hostUrl + '/KSSW/stu_ksap_rpt.aspx',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    }
    ks_resp = session.get(
        url=url,
        headers=ks_headers)
    saveImgae("ks-"+xnxq, ks_resp.content)


if __name__=='__main__':
    username = '学号'
    password = '密码'
    login(username,password)
    getScore()
    getCourse()
    getExam()
