#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/4/10
'''

import datetime
import time
from dateutil import rrule,relativedelta
from dateutil.parser import parse

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"
DATE_FORMAT_ABBR = "%Y%m%d"
TIME_FORMAT = "%H:%M:%S"
YEARLY=0; MONTHLY=1; WEEKLY=2; DAILY=3; HOURLY=4; MINUTELY=5; SECONDLY=6

#返回当前日期，格式为2020-04-14，不能通过参数指定格式化样式
#返回数据类型为<class 'datetime.date'>
def curDatetime2(format = DATETIME_FORMAT):
    today = datetime.datetime.now()
    dt = today.strftime(format)
    dt = datetime.datetime.strptime(dt, format).date()
    return dt

# 当前毫秒数
def curMilis():
    return int(time.time() * 1000)

# 当前秒数
def curSeconds():
    return int(time.time())

# 当前日期 格式%Y-%m-%d %H:%M:%S
# 返回字符串类型
def curDatetime(format = DATETIME_FORMAT):
    return datetime.datetime.strftime(datetime.datetime.now(), format)

# 当前日期 格式%Y-%m-%d
#返回日期类型
def curDate():
    return datetime.date.today()

# 当前时间 格式%Y-%m-%d
# 返回字符串类型
def curTime(format = TIME_FORMAT):
    return time.strftime(format)

# 当前年
def curYear():
    return datetime.datetime.now().year

# 当前月
def curMonth():
    return datetime.datetime.now().month

# 当前日
def curDay():
    return datetime.datetime.now().day

# 当前时
def curHour():
    return datetime.datetime.now().hour

# 当前分
def curMinute():
    return datetime.datetime.now().minute

# 当前秒
def curSecond():
    return datetime.datetime.now().second

# 当前星期几
def curWeek():
    return datetime.datetime.now().weekday()

####################################################################################################################
####################################################################################################################

# 几天前的时间
# 返回日期字符串
def nowDaysAgo(days, format = DATETIME_FORMAT):
    daysAgoTime = datetime.datetime.now() - datetime.timedelta(days=days)
    return time.strftime(format, daysAgoTime.timetuple())

# 几天后的时间
# 返回日期字符串
def nowDaysAfter(days, format = DATETIME_FORMAT):
    daysAfterTime = datetime.datetime.now() + datetime.timedelta(days=days)
    return time.strftime(format, daysAfterTime.timetuple())

# 某个日期几天前的时间
def dtimeDaysAgo(dtimestr, days, format = DATETIME_FORMAT):
    daysAgoTime = datetime.datetime.strptime(dtimestr, format) - datetime.timedelta(days=days)
    return time.strftime(format, daysAgoTime.timetuple())

# 某个日期几天前的时间
def dtimeDaysAfter(dtimestr, days, format = DATETIME_FORMAT):
    daysAfterTime = datetime.datetime.strptime(dtimestr, format) + datetime.timedelta(days=days)
    return time.strftime(format, daysAfterTime.timetuple())

# 输入日期判断是哪一年的第几周，周几
# 返回格式：(年,第几周,周几),比如：(2016, 52, 7)
def getYearWeek(strdate=curDatetime(DATE_FORMAT)):
    date = datetime.datetime.strptime(strdate, '%Y-%m-%d')
    YearWeek = date.isocalendar()
    return YearWeek


# 当前日期是哪一年的第几周，周几
# 返回格式：(年,第几周,周几),比如：(2016, 52, 7)
def getNowYearWeek():
    timenow = datetime.datetime.now()
    NowYearWeek = timenow.isocalendar()
    return NowYearWeek


# 日期所在周的周一日期
# 返回格式：2020-04-06
def getDayInweekMonday(dateobj=datetime.datetime.now()):
    week_num = dateobj.weekday()
    Monday = dateobj + datetime.timedelta(days=-week_num)
    Monday = str(Monday)[0:10]
    return Monday


# 获取上一周的周一和周日的时间
def getDayLastWeekMondayAndSunday(dateobj=datetime.datetime.now()):
    week_num = dateobj.weekday()

    Monday = dateobj - datetime.timedelta(days=7) + datetime.timedelta(days=-week_num)
    Monday = Monday.strftime('%Y-%m-%d 00:00:00')
    Monday = str(Monday)[0:10]

    Sunday = dateobj - datetime.timedelta(days=1) + datetime.timedelta(days=-week_num)
    Sunday = Sunday.strftime('%Y-%m-%d 23:59:59')
    Sunday = str(Sunday)[0:10]
    # print str(Sunday)[0:10]

    return Monday, Sunday

# weekflag格式为"2016#53"（即2016年第53周的开始时间）
def getWeekFirstday(weekflag):
    year_str = weekflag[0:4]  # 取到年份
    week_str = weekflag[5:]  # 取到周
    if int(week_str) >= 53:
        Monday = "Error,Week Num greater than 53!"
    else:
        yearstart_str = year_str + '0101'  # 当年第一天
        yearstart = datetime.datetime.strptime(yearstart_str, '%Y%m%d')  # 格式化为日期格式
        yearstartcalendarmsg = yearstart.isocalendar()  # 当年第一天的周信息
        yearstartweekday = yearstartcalendarmsg[2]
        yearstartyear = yearstartcalendarmsg[0]
        if yearstartyear < int(year_str):
            daydelat = (8 - int(yearstartweekday)) + (int(week_str) - 1) * 7
        else:
            daydelat = (8 - int(yearstartweekday)) + (int(week_str) - 2) * 7
        Monday = (yearstart + datetime.timedelta(days=daydelat)).date()
    return Monday

# 计算两个时间之差，单位有unit参数指定，可以是 YEARLY, MONTHLY, WEEKLY,DAILY, HOURLY, MINUTELY, SECONDLY。即年月日周时分秒
# 返回差值
def diffrentPeriod(freq, startDate, endDate):
    return  rrule.rrule(freq, dtstart=parse(startDate),  until=parse(endDate)).count()

# 计算两个日期之间的年
def diff(start,end):
    diff = relativedelta.relativedelta(end, start)
    #print(diff.months) #只计算相对月数
    #print(diff.days)   #只计算相对天数
    return diff.years

# 计算两个日期之间的天数
def diffrentDay(start,end):
    #today = datetime.date.today()
    #my_birthday = datetime.date(year=1992, month=3, day=17)
    #print('我已经出生' + str((today - my_birthday).days) + '天')
    return str((end - start).days)

#给定日期时间的后一周期，比如下一天，下一月，下一分钟
def nextDateTime():
    pass
####################################################################################################################
####################################################################################################################
# 秒转日期
# 返回字符串类型
def secondsToDatetime(seconds, format = DATETIME_FORMAT):
    return time.strftime(format, time.localtime(seconds))

# 秒转日期, 东八区时间处理
# 返回字符串类型
def secondsToDatetime2(seconds, format = DATETIME_FORMAT):
    utc_time = datetime.datetime.utcfromtimestamp(seconds)
    return (utc_time + datetime.timedelta(hours=8)).strftime(format)

# 毫秒转日期
# 返回字符串类型
def milisToDatetime(milix, format = DATETIME_FORMAT):
    return time.strftime(format, time.localtime(milix // 1000))

# 日期转毫秒，传入日期字符串参数
def datetimeToMilis(datetimestr, format = DATETIME_FORMAT):
    strf = time.strptime(datetimestr, format)
    return int(time.mktime(strf)) * 1000

# 日期转秒，传入日期字符串参数
def datetimeToSeconds(datetimestr, format = DATETIME_FORMAT):
    strf = time.strptime(datetimestr, format)
    return int(time.mktime(strf))

# 日期时间对象转字符串
def datetime2str(datetime, format = DATETIME_FORMAT):
    #return time.strftime(datetime, format).date()
    return datetime.datetime.strftime(datetime, format)

# 日期时间对象转字符串
# format参数待调试，有问题
def datetime2str2(datetime, format = None):
    if format is None:
        return str(datetime)
    else:
        #return time.strftime(datetime, format).date()
        return str(datetime.datetime.strftime(datetime, format))

# 日期对象转字符串
def date2str(date):
    return str(date)

# 日期字符串转换为日期对象类型
#返回类型：<class 'datetime.date'>
def str2date(datetimestr, format = DATE_FORMAT):
    return datetime.datetime.strptime(datetimestr, format).date()

# 日期时间字符串转换为日期时间对象类型
def str2datetime2(datetimestr, format = DATETIME_FORMAT):
    #datetimestr = datetime.now().isoformat().split('.')[0]
    print(datetime.datetime.strptime(datetimestr, format))

# 日期时间字符串转换为日期时间对象类型
# 传入的日期时间字符串格式支持：-、/、,、紧挨型、英文等格式，详见https://www.jianshu.com/p/f29dddce3a9a
# 返回格式：2020-04-14 00:00:00
def str2datetime(datetimestr):
    return parse(datetimestr)

# 日期时间对象格式化，返回日期或时间
def formateDateTime(datetime,format):
    pass

def time2str(time):
    pass

def str2time(str):
    pass

#返回后一分钟时间字符串
#输入格式为："%H:%M:%S"
#返回值：字符串"%H:%M:%S"
def nextmin(str):
    arr = time.split(':')
    timeobj = datetime.date(hour=arr[0], minute=arr[1], second=arr[2])

#当前时间戳转换为指定格式的日期
def test1():
    # 使用time
    timeStamp = time.time()  # 1559286774.2953627
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print(otherStyleTime)  # 2019-05-31 15:12:54
    # 使用datetime
    timeStamp = time.time()  # 1559286774.2953627
    dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
    otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
    print(otherStyleTime)  # 2019-05-31 07:12:54

#把字符串类型的日期转换为时间戳
def test2():
    # 字符类型的时间1
    tss1 = '2019-05-31 15:12:54'
    # 转为时间数组
    timeArray = time.strptime(tss1, "%Y-%m-%d %H:%M:%S")
    print(timeArray)
    # timeArray可以调用tm_year等
    print(timeArray.tm_year)  # 2019
    # 字符类型的时间2
    tss2 = "Fri Jun 21 13:22:37 +0800 2019"
    timeArray = time.strptime(tss2, "%a %b %d %H:%M:%S %z %Y")
    # timeArray可以调用tm_year等
    print(timeArray.tm_year)  # 2019
    # 转为时间戳
    timeStamp = int(time.mktime(timeArray))
    print(timeStamp)  # 1559286774

#更改str类型日期的显示格式
def test3():
    tss2 = "2019-05-31 15:12:54"
    # 转为数组
    timeArray = time.strptime(tss2, "%Y-%m-%d %H:%M:%S")
    # 转为其它显示格式
    otherStyleTime = time.strftime("%Y/%m/%d %H:%M:%S", timeArray)
    print(otherStyleTime)  # 2019/05/31 15:12:54

    tss3 = "2019/05/31 15:12:54"
    timeArray = time.strptime(tss3, "%Y/%m/%d %H:%M:%S")
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print(otherStyleTime)  # 2019-05-31 15:12:54

    tss4 = "2019/05/31 15:12:54"
    otherStyleTime = datetime.datetime.strptime(tss4, "%Y/%m/%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
    print(otherStyleTime)  # 2019-05-31 15:12:54

#日期的加减
def test4():
    d1 = datetime.datetime.strptime('2019-05-31 15:12:54', '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime('2019-05-22 15:12:54', '%Y-%m-%d %H:%M:%S')
    delta = d1 - d2
    print(delta.days)  # 9  间隔9天

#股票交易时间转序列号，时间从9:31--11:30,13:00--15:00,每分钟一档，共计240档，序列从0--239
def stockTradeTime2Index(time):
    arr = time.split(':')
    index = -1
    hour = int(arr[0])
    min = int(arr[1])
    switch = {
        9: lambda m: m -31 if m > 30 else -1,
        10: lambda m: 29 + m,
        11: lambda m: 89 + m,
        13: lambda m: 119 + m,
        14: lambda m: 179 + m,
        15: lambda m: 239 if m == 0 else -1
    }
    return switch[hour](min)

#股票交易序列号转时间，序列号从0--239，对应时间从9:31--11:30,13:00--15:00,每分钟一档，共计240档
def stockTradeIndex2Time(index):
    if index < 0 or index > 239: return -1
    BASE = 60
    time_format = "{0:02d}:{1:02d}:00"
    if index < 29:
        return time_format.format(9,index +31)
    elif index < 120:
        index = index -30
        switch = {0: 10, 1: 11}
    else:
        index = index -120
        switch = {0: 13, 1: 14, 2: 15}
    phase = (index + 1) // BASE
    model = (index + 1) % BASE

    return time_format.format(switch[phase],model)


#time.strftime 方法来格式化日期
#time.strptime() 函数根据指定的格式把一个时间字符串解析为时间元组
#datetime.datetime.strptime() 由字符串格式转化为日期格式
#datetime.datetime.strftime() 由日期格式转化为字符串格式
def test_get_now():
    dat1 = time.localtime()  # <class 'time.struct_time'>
    print(dat1)
    print(type(dat1))
    dat2 = time.strftime(DATE_FORMAT, dat1)  # <class 'str'>
    print(dat2)
    print(type(dat2))
    dat3 = time.strptime(dat2,DATE_FORMAT)  # <class 'time.struct_time'>
    print(dat3)
    print(type(dat3))
    dat32 = datetime.datetime.strptime(dat2,DATE_FORMAT)  #<class 'datetime.datetime'>
    print(dat32)
    print(type(dat32))
    dat33 = parse(dat2)                 # <class 'datetime.datetime'>
    print(dat33)
    print(type(dat33))

    dat4 = datetime.date.today()  # <class 'datetime.date'>
    print(dat4)
    print(type(dat4))
    dat5 = datetime.datetime.strftime(dat4, DATETIME_FORMAT)  # <class 'str'>
    print(dat5)
    print(type(dat5))
    dat6 = datetime.datetime.strptime(dat5, DATETIME_FORMAT)  # <class 'datetime.datetime'>
    print(dat6)
    print(type(dat6))

    dat7 = datetime.datetime.now()  # <class 'datetime.datetime'>
    print(dat7)
    print(type(dat7))
    dat8 = datetime.datetime.strftime(dat7,DATE_FORMAT)  #<class 'str'>
    print(dat8)
    print(type(dat8))
    dat9 = datetime.datetime.strptime(dat8, DATE_FORMAT)  # <class 'datetime.datetime'>
    print(dat9)
    print(type(dat9))

if __name__ == '__main__':
    sec = 1586498316
    time_stamp = 1537846361
    milisec = 1586498344522
    date_time = "2016-03-20 11:45:39"
    date_str = "2020-04-14"
    strdate = '2017-01-01'
    date_str_abbr = "20200414"
    dateobj = datetime.date(year=1992, month=3, day=17)
    todayobj = datetime.date.today()
    '''DATE_FORMAT_ABBR, DATE_FORMAT, DATETIME_FORMAT, TIME_FORMAT'''
    #print(datetime2str(todayobj,DATE_FORMAT))
    #print(type(datetime2str(datetime.date.today(),DATE_FORMAT)))
    #print(diffrentPeriod(YEARLY,'2018-3-15','2018-11-10'))
    #print(secondsToDatetime2(time_stamp, DATE_FORMAT_ABBR))
    #str2datatime2(date_str,DATE_FORMAT)
    #print(diff(datetime.date(year=1992, month=3, day=17),datetime.date(year=2020, month=3, day=17)))

    #print(getYearWeek())
    #print(getNowYearWeek())
    #print(getDayInweekMonday(dateobj))
    #print(getDayLastWeekMondayAndSunday(dateobj))
    # 输出2014年第35周的开始时间
    #print(getWeekFirstday('2014#35'))

    #test_get_now()
    #print(datetime2str2(dateobj))
    #print(type(datetime2str2(dateobj)))

    timestr = '09:31:00'
    print(timestr, '--', stockTradeTime2Index(timestr) , '--', stockTradeIndex2Time(stockTradeTime2Index(timestr)))
    #for i in range(240):
        #print(i,'--',stockTradeIndex2Time(i))
    #now = datetime.datetime.now()
    #timeobj = datetime.time(hour=9, minute=30, second=17)
    #for i in range(60):
    #    timeobj = (timeobj + datetime.timedelta(minutes=1)).strftime("%H:%M:%S")
    #    print(timeobj)


