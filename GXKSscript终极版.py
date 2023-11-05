import time
import requests
from lxml import etree

session = requests.session()
login_status = False
courseList = set()
iiiii=0
fff=False

data_course = {
    'ddlClass': 25,
    '__EVENTTARGET': 'PageSplit1$ddlPage',
    '__VIEWSTATE': '',
    '__EVENTVALIDATION': '',
    '__VIEWSTATEGENERATOR': '',
    'PageSplit1$ddlPage': 0,
    'btnSearch':'搜索'

}
id_course_ddlClass = []
# todo login


def _login():
    # username = 'xxxxxxxx'
    # password = 'xxxxxxxx'
    username = input('账号：')
    password = input('密码：')
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
    name = loginEtree.xpath(
        '//div[@class="header"]/div[@class="layout"]/div[@class="fright"]/ul/li/text()')[0]
    data_course['__VIEWSTATE'] = loginEtree.xpath(
        '//*[@id="__VIEWSTATE"]/@value')[0]
    data_course['__EVENTVALIDATION'] = loginEtree.xpath(
        '//*[@id="__EVENTVALIDATION"]/@value')[0]
    data_course['__VIEWSTATEGENERATOR'] = loginEtree.xpath(
        '//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]
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
    def __init__(self, course, courseId, videoLength, isFinished, lookTime, iiiii,id='', refId='', Mins='', StudentId='',
                 SessionID=''):
        self.course = course
        self.courseId = courseId
        self.videoLength = videoLength
        self.isFinished = isFinished
        self.lookTime = lookTime
        self.iiiii=iiiii
        self.id = id
        self.refId = refId
        self.Mins = Mins
        self.StudentId = StudentId
        self.SessionID = SessionID

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.courseId == other.courseId
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.courseId)
    

def compare(self):
    return self.iiiii

# todo Account information
def _getInfo(mainResp,flag):
    if flag == False:
        return
    et = etree.HTML(mainResp.text)
    course = et.xpath('//tr[@onmouseover]/td[@class="pleft30"]/text()')
    course_Id = et.xpath('//tr[@onmouseover]/td[6]/a/@onclick')  # 需要二次处理
    video_Length = et.xpath('//tr[@onmouseover]/td[3]/text()')  # 需要二次处理
    isFinished = et.xpath('//tr[@onmouseover]/td/span/text()')
    look_Time = et.xpath('//tr[@onmouseover]/td[4]/text()')  # 需要二次处理
    data_course['__VIEWSTATE'] = et.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
    data_course['__EVENTVALIDATION'] = et.xpath(
        '//*[@id="__EVENTVALIDATION"]/@value')[0]
    # print(course[0],course_Id[0],videoLength[0],isFinished[0],lookTime[0])代码错误
    Len = len(course)
    global fff
    if not fff :
        fff=True
        return
    for i in range(Len):
        courseId = course_Id[i].split(',')[-1][0:-1]
        videoLength = video_Length[i][0:-2]
        lookTime = look_Time[i][0:-2]
        global iiiii
        temp = video(course[i], courseId, videoLength, isFinished[i], lookTime,iiiii)
        courseList.add(temp)
        iiiii+=1


# todo Gets information about the course
def _getCourse(page, index=0):
    mainUrl = 'http://www.gaoxiaokaoshi.com/Study/LibraryStudyList.aspx'
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    data_course['PageSplit1$ddlPage'] = page+1
    global login_status
    if page == 0 and not login_status:
        mainResp = session.get(mainUrl, headers=head)
        et = etree.HTML(mainResp.text)
        global id_course_ddlClass
        id_course_ddlClass = et.xpath('//*[@id="ddlClass"]/option/@value')
        if len(id_course_ddlClass) == 1 :
            global fff
            fff=True    
    else:
        data_course['ddlClass'] = id_course_ddlClass[index]
        mainResp = session.post(mainUrl, headers=head, data=data_course)
        mainResp.close()
    if mainResp.status_code != 200:
        return False,mainResp.text 
    mainResp.encoding = mainResp.apparent_encoding
    # print(mainResp.text)
    if not login_status:
        login_status = True
        return True,mainResp
    return None,mainResp

# todo Get all the forms of video information
def _getAllVideoInput(index=0):
    if courseList[index].isFinished == '已完成':
        return
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
        if i.isFinished == '已完成':
            continue
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
    print('**如果你想请作者喝一杯卡布奇诺的话，感谢大哥!好人一胎八个**')
    print('如果有使用问题的话，请联系作者邮箱kunkun317@qq.com')
    print('刷课继续...')


if __name__ == '__main__':
    _disclaimer()  # 免责声明
    _login()  # 登录
    for index in range(100000):
        if(index!=0):
            if(index>=len(id_course_ddlClass)):
                break
        # 获取课程信息
        for i in range(1000):
            flag,resp = _getCourse(i,index)
            if flag == False:
                break
            _getInfo(resp,flag)
    # 获取需要多长的时间刷课
    courseList=(list(courseList))
    courseList.sort(key=compare)
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
    print("刷课初始化中...")
    # Get all the forms of video information
    length = len(courseList)
    for i in range(length):
        _getAllVideoInput(i)
    print('每分钟自动上报一下刷课进度，请耐心等待。')
    _notice()
    time.sleep(60)
    for i in range(countTime):
        _WatchAllVideos(i)
        print('刷课时长累计', i + 1, '分钟，ok!!!')
        time.sleep(60)
    print('所有视频刷课完成，谢谢您的使用！')
    time.sleep(180)
