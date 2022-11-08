import time
import requests
from lxml import etree
from PIL import Image

session = requests.session()
courseList = []


# todo login
def _login():
    # username = ''
    # password = ''
    username=input('账号：')
    password=input('密码：')
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
    title = loginEtree.xpath('//title/text()')[0]
    # print(loginResp.text)
    name = loginEtree.xpath('//div[@class="header"]/div[@class="layout"]/div[@class="fright"]/ul/li/text()')[0]
    print('Welcome to the GXKSscript:', name)


# todo 免责声明
def _disclaimer():
    print('免责声明：请您认真阅读下面文字：')
    print('今后由该脚本引起的纠纷和造成的一切后果，其责任概由其使用者承担，与本作者无关。')
    print('你可现在直接退出本脚本，无任何影响，继续使用本脚本将自动视为同意上述声明，并承担其可能造成的后果。如果有人篡改该脚本，其承担所有后果。望其周知！！！')
    input('按任意键以继续...')
    print('欢迎使用高校考试网 www.gaoxiaokaoshi.com 自动刷课脚本')
    print('此脚本不参与任何交易，如果侵权的话，请联系我删库跑路。')
    print('项目地址https://github.com/AlwaysLazy21/GXKSscript')
    print('如果你感觉此脚本对你有帮助的话，可以给我一个★star')


# todo class video存储视频相关信息
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


# todo Account information
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
        print(course[i], 'videoLength:', videoLength, 'isFinished:', isFinished[i], 'lookTime:', lookTime)


# todo Gets information about the course
def _getCourse(page=0):
    mainUrl = 'http://www.gaoxiaokaoshi.com/Study/LibraryStudyList.aspx'
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    data_course = {
        '__VIEWSTATE': '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',
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


# todo Watch all the videos at the same time
def _WatchAllVideos(count):
    for i in courseList:
        if i.isFinished == '已完成': continue
        frameUrl = f"http://www.gaoxiaokaoshi.com/Study/LibraryStudy.aspx?tmp=1&Id={i.courseId}&PlanId=11"
        domainURl = 'http://www.gaoxiaokaoshi.com/Study/updateTime.ashx?'
        head = {
            'Host': 'www.gaoxiaokaoshi.com',
            'Referer': frameUrl,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        param_from = {
            'Id': i.id,
            'pTime': 60 * (count + 1),
            'Mins': i.Mins,
            'refId': i.refId,
            'StudentId': i.StudentId,
            'StydyTime': 0,
            'SessionId': i.SessionID
        }
        domainResp = session.get(domainURl, headers=head, params=param_from)
        # print('666')


def _notice():
    print('Notice:理论上该脚本可适用于所有学校。')
    print('工作原理：获取所有未完成的视频数据，伪造请求欺骗服务器，以达到刷课目的。')
    print('考试：只有三次机会，风险有点大。刷课考试：拦截提交的数据包，更换身份id重新发送即可。')
    print('如果你感觉同时刷所有视频风险太大的话，可使用上一版本。')
    print('**如果你想请作者喝一杯卡布奇诺的话，感谢大哥!好人一胎八个**')
    select = input('是否支持作者?(Y/n)')
    if select == 'Y':
        im = Image.open('支付宝.jpg')
        im.show()
        print('支付宝用户名为：L*星芒（**坤），切勿上当！！！')
    print('如果有使用问题的话，请联系作者邮箱kunkun317@qq.com')
    print('刷课继续...')


if __name__ == '__main__':
    _disclaimer()  # 免责声明
    _login()  # 登录
    # 获取课程信息
    for i in range(1000):
        resp = _getCourse(i)
        if resp == False:
            break
        _getInfo(resp)
    # 获取需要多长的时间刷课
    countTime = -1
    for i in courseList:
        if i.isFinished == '已完成':
            continue
        tempTime = (int)(i.videoLength) - (int)(i.lookTime)
        countTime = max(countTime, tempTime)
    if countTime == -1:
        print("您的所有任务已完成！一分钟后自动退出。")
        time.sleep(60)
    print("本次刷课一共需要耗时", countTime, '分钟，',
          '刷课期间请保持网络通畅，脚本可在后台默默运行，可放心去进行您的其他工作。')
    # Get all the forms of video information
    length = len(courseList)
    for i in range(length):
        _getAllVideoInput(i)
    print('每六十分钟自动上报一下刷课进度，请耐心等待。')
    _notice()
    time.sleep(60)
    for i in range(countTime):
        _WatchAllVideos(i)
        print('刷课时长累计', i + 1, '分钟，ok!!!')
        time.sleep(60)
    print('所有视频刷课完成，谢谢您的使用！')
    time.sleep(180)
