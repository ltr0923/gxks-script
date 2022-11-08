import time
import requests
from lxml import etree
from PIL import Image


def _login(user_name,flag=True):
    username = user_name
    password = '000000'     # todo 班级学生默认密码
    # username = input('账号：')
    # password = input('密码：')
    loginUrl = 'http://www.gaoxiaokaoshi.com/HidLogin.aspx'
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    data = {
        'screenType': '1440',
        'name': username,
        'pw': password
    }
    loginResp = session.post(loginUrl, headers=head, data=data)
    if loginResp.status_code != 200:
        print(loginResp.status_code)
    loginResp.encoding = loginResp.apparent_encoding
    loginResp.close()
    loginEtree = etree.HTML(loginResp.text)
    try:
        title = loginEtree.xpath('//title/text()')[0]
        # print(loginResp.text)
        name = loginEtree.xpath('//div[@class="header"]/div[@class="layout"]/div[@class="fright"]/ul/li/text()')[0]
        print('Welcome to the GXKSscript:', name)
    except:
        print(id,'账号密码错误')
        flag=False
    return flag


class video:
    def __init__(self, course, courseId, videoLength, isFinished, lookTime, id='', refId='', Mins='', StudentId='',
                 SessionID=''):
        self.course = course
        self.courseId = courseId
        self.videoLength = videoLength
        self.isFinished = isFinished
        self.lookTime = lookTime
        self.id = id,
        self.refId = refId
        self.Mins = Mins
        self.StudentId = StudentId
        self.SessionID = SessionID


def _getInfo(mainResp):
    if mainResp == False:
        return
    et = etree.HTML(mainResp.text)
    course = et.xpath('//tr[@onmouseover]/td[@class="pleft30"]/text()')
    course_Id = et.xpath('//tr[@onmouseover]/td[6]/a/@onclick')  # 需要二次处理
    video_Length = et.xpath('//tr[@onmouseover]/td[3]/text()')  # 需要二次处理
    isFinished = et.xpath('//tr[@onmouseover]/td/span/text()')
    look_Time = et.xpath('//tr[@onmouseover]/td[4]/text()')  # 需要二次处理
    # print(course[0],course_Id[0],videoLength[0],isFinished[0],lookTime[0])代码错误
    Len = len(course)
    for i in range(Len):
        courseId = course_Id[i].split(',')[-1][0:-1]
        videoLength = video_Length[i][0:-2]
        lookTime = look_Time[i][0:-2]
        temp = video(course[i], courseId, videoLength, isFinished[i], lookTime)
        courseList.append(temp)
        # print(course[i], 'videoLength:', videoLength, 'isFinished:', isFinished[i], 'lookTime:', lookTime)


# todo Gets information about the course
def _getCourse(page=0):
    mainUrl = 'http://www.gaoxiaokaoshi.com/Study/LibraryStudyList.aspx'
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    data_course = {
        '__VIEWSTATE': 'kQsdx7DEbWndjRbdD5PRH74zru/7zrNpx2aWc2LTCx2mkBzN7TGMKBYFRUJ4G6ph+YU/lHLDPgmR2Ua6SGmeH9WFtdrZmBVRJnfko3Yq53gec01M5xMtWPv4jOJmfRNqjHU5Mpq4Fkty3X1ZIi+5PLKSs6coFfIelDPLwJIp+NYWqy318w4IWWgSPMeQNdovvoFCDQ+MrNGIZCqPU+PnBv0fApTIS53RmwtUV5k+rU6Mp2vqlypHKbpHr2DIqBLwuUiRpivJsrinQkl9f8QoswPmHouY28o8zr6u60kgvHPxukfGHI/8wc/IKeNM6Or46kMM7drHpecl3PCl/Ch2jD1x78LLbzLRr0E10u9BtRrypM85VWSZbR4xoFDW0akvuiCqNA1Zx/xTSPYeEhCamtM3MShdjewAd1wCEVGutefP+4pmVKP5Nh8sciYxdCdtTnogqmVrVWnjAnCc/1GG9FzV6I23jwh5GdRIXf4SKkcmRxyx+LGOnMiKv3IYhtdJd5WinFDb8G9ClXj2cimbb2rPVoZkys5yB2tRgFyI95F8OjvRnO9DjTXP5fkMp0BF5pdX1Y2ZMWyjCm0EIhFIWak2pn5IXO//ZVK5x0GAwKyUM1HGY4pohwGgcm6ogwutEEAVJt0H+zsftt2GXs961OuejwHDsYdxGsRab48JJDG237kFILh6sx9bLCb0AFxzpusbj5RfHpHMQcz7Fs0qxs000j0PRigdPkjdJ9Nxx2siA9uPAthXLZeB6RyqaQuxCd4XGz4cSnKYcE452AWwuOh8yK6jDXLyHKy9ZuoG7vH9oYGFUy3l++TreazL/0yITPh4kLf/MhAKpDVk56Vs25Z65UctE5szb8mQArdncVkBEFlwI9iNN3pupEbccU5yo6B9F/RI4wBchH/w62bJWOISmWjdnzBAk+tolhqD/++eKaKTl7gAkqB0o28NiOypkjbW/DhDD+64MI/IDFTGNks58QgYEIIr2K22l4DocqiNmC4E1+sXzo88uWjivyJkcPOSSp8DA9JyW7AUYiPF9C2QhNGvvng6mdlH9Rl9qJun37FSUDsaO64CxLB9DPSz4vUyH3FvkiWPcETsQwfMfjrTjjqe2fZWLIvN7hEuQTOOIEq8YmXzOQkAdAirgHJaNaRyjf8HCq+ZGRo3YMMzGVrcq7YntdOf9jNG1IIwvUTzG63InY499pSwzgd+YOJNJ9VTuwxi5ZDdS6PytUJeyZ71CPvrhD3OqaSvEysoS5d12rVO2OOFgCyrKkPopEZBUSoscrlGX+fDv6A/yzkGM2oEM0cyJtQ1ILYGSQ8nPlW6BmLeRR9ZWkyvYe5pY0iGaJcNUdlLpAOmrJPy9GYptwYTvHNBbzbsq+RsL2AjsGThg6ZNFHoDdbZysw4c8rMac+nXK33dHZf1MplBd3Rop/pMq8nnsoF8PK7lD2+r/Zo0Zp+ttnQGkPKG//rYbOndeU0O2Apk07n268HDz3HK8agGx8zvDD1ovmoTJBjBKEbsbq+SEPXddFw3/WvenPjghYhkNR1exEmt68xHCm95KVES0dVYp3KLV7+BK/DKj/a3Wh08WxDhcxCXCnM2lJE8G3aBhwiEEilOnliXFcA6vdzMyR0A7oNdjtYpuFlVSKZs6nl+J3viMelWE3R2rgx2tVk6cOo2SNPV7jSKF2WalknrxebKMhPfm4wRp99UzWzke8E7tsHlGFAaLd5+PAjDPkg1WKbnZFT8dekH2eFPQtsplrdwpo3en0zuvPrpI4+GHBjdv2Gj6L5+xBMk3pW2XE2ORwMbzYBYS4lkiZVHaPCoR4oER7K8QJHERk2RcLWheEQiMU7UGzA6fODhDY6TxnJWF9F1D0glfcYkBWoIh+FB17sAgYl94txpNdpBYh5UU9oUXD6+mljkp7oKKhDGltvuaHevbhUcFiJsWU4FlW0bA7vxxFhm+VVzmj4sTYu5nEV3OUzloiIJP2VDP+cv52DKkprbNJ2j/lXz9VQtC4RA3byo8p3PTw3kEpXh4lFAU/+0RmTVk3CNKqzX+m7PsbUcHlryl2w57mNpQCzQ1tA5jnWAhQz9LidD3K1HIXvr/F7GvKfyuKBohseD0Fk4posqoxdTqY0Eyi8JylFyM017FUOa06Y77lK7iVHu5wz5VwcrNQCXMBLWnL6llcsvqiAR/ktHFHZj94V6eMono1WSAXrGq1StC05aJSpsLLt+3grAtWvAn/cM/7GE/V3Cycg5oIhov6hDX60gLqCWlQCDkT3em7Xb1zefUTqOtwltMCJF8lc/Y4AcupKkkn4Uv4qLuE0ol9MYOeSQrJJxGYGB5zCmKZThHvUuEjq4X+ABY5XLA6WDA814DWPf9TOL3vRQx2F7Vs0Y4lDsSrfSq2v6NluxZzOEFd4vBNIGicrkTyRAGDTMnkDOBc1zF+CJxU4bq0Qb4d5cJY5BztfJtLOuKg1RJoiLcNz+Lg==',
        '__EVENTVALIDATION': 'pSk4P35UquECGSKpdgM9n23Key7Mc7Zk/lp8/4ubIgiJzsDwaLQ8WhCL0NvBbMqT4IwD5bnZGxq++D76H2S2EONohcczJXwlEMKZdACZi7smPenf5PpMc4Bab/TE1bVGuqzRjXKS5O0yKhHwv5OTWDRNlIQlHHjFToiqShOxh3V08c2HI72WEhRmbYDFi18AAo0UMq/71KEyg6SV3+SBFBa21dOodTl0ZoaIAwRd7XDqsBIQwsyefJfAjWS6ccGjyMqUXOa1415irGoHBUHOvWlHN5HN+401/FddXxh7xL+WhaTFxCfuUa+GEosdMJYOsgZc5nS1h0kP9CrG',
        'PageSplit1$ddlPage': page + 1
    }
    mainResp = session.post(mainUrl, headers=head, data=data_course)
    mainResp.close()
    if mainResp.status_code != 200:
        return False
    mainResp.encoding = mainResp.apparent_encoding
    # print(mainResp.text)
    return mainResp


# todo Get all the forms of video information
def _getAllVideoInput(index=0):
    if courseList[index].isFinished == '已完成': return
    frameUrl = f"http://www.gaoxiaokaoshi.com/Study/LibraryStudy.aspx?tmp=1&Id={courseList[index].courseId}&PlanId=11"
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    frameResp = session.get(frameUrl, headers=head)
    frameResp.close()
    et = etree.HTML(frameResp.text)
    id = et.xpath('//input[@id="hidNewId"]/@value')[-1]
    refId = et.xpath('//input[@id="hidRefId"]/@value')[-1]
    Mins = et.xpath('//input[@id="hidPassLine"]/@value')[-1]
    StudentId = et.xpath('//input[@id="hidStudentId"]/@value')[-1]
    SessionID = et.xpath('//input[@id="hidSessionID"]/@value')[-1]
    courseList[index].id = id
    courseList[index].refId = refId
    courseList[index].Mins = Mins
    courseList[index].StudentId = StudentId
    courseList[index].SessionID = SessionID


if __name__ == '__main__':
    print('author:AlwaysLazy21')
    demo_id = int(input('请输入你们班第一个人的学号：'))
    x = int(input('请输入班级人数：'))
    for i in range(x):
        session = requests.session()
        id = demo_id + i
        user_name = 'xcu' + (str)(id)    # todo 将前面的xcu改为自己账号的前缀即可
        if _login(user_name)==False:
            del session
            continue
        courseList = []

        # 获取课程信息
        for ii in range(1000):
            time.sleep(1)
            resp = _getCourse(ii)
            if resp == False:
                break
            _getInfo(resp)
        # 获取需要多长的时间刷课
        countTime = -1
        for iii in courseList:
            if iii.isFinished == '已完成':
                continue
            tempTime = (int)(iii.videoLength) - (int)(iii.lookTime)
            countTime = max(countTime, tempTime)
        if countTime == -1:
            print('top:',i+1,'  已完成###')
            time.sleep(1)
        else:
            print('top:',i+1,'  未完成...')
            time.sleep(1)
        del session
        del courseList
    input()