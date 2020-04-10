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

# 星期几
def curWeek():
    return datetime.datetime.now().weekday()

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

# 日期时间对象转字符串
# 该方法有问题
def datetime2str(datetime, format = DATETIME_FORMAT):
    print(datetime)
    #return time.strftime(datetime, format).date()
    return time.strptime(datetime, format).date()


# 输入日期判断是哪一年的第几周，周几
# 返回格式：(年,第几周,周几),比如：(2016, 52, 7)
def getYearWeek(strdate):
    date = datetime.datetime.strptime(strdate, '%Y-%m-%d')
    YearWeek = date.isocalendar()
    return YearWeek


# 当前时间是哪一年的第几周，周几
def getNowYearWeek():
    timenow = datetime.datetime.now()
    NowYearWeek = timenow.isocalendar()
    return NowYearWeek


# 当前时间所在周的周一时间
def getDayInweekMonday():
    week_num = datetime.datetime.now().weekday()
    Monday = datetime.datetime.now() + datetime.timedelta(days=-week_num)
    Monday = str(Monday)[0:10]
    return Monday


# 获取上一周的周一和周日的时间
def getDayLastWeekMondayAndSunday():
    week_num = datetime.datetime.now().weekday()

    Monday = datetime.datetime.now() - datetime.timedelta(days=7) + datetime.timedelta(days=-week_num)
    Monday = Monday.strftime('%Y-%m-%d 00:00:00')
    Monday = str(Monday)[0:10]

    Sunday = datetime.datetime.now() - datetime.timedelta(days=1) + datetime.timedelta(days=-week_num)
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

# 日期时间字符串转换为日期时间对象类型
def str2datatime2(datetimestr, format = DATETIME_FORMAT):
    #datetimestr = datetime.now().isoformat().split('.')[0]
    print(datetime.datetime.strptime(datetimestr, format))

# 日期时间字符串转换为日期时间对象类型
# 传入的日期时间字符串格式支持：-、/、,、紧挨型、英文等格式，详见https://www.jianshu.com/p/f29dddce3a9a
# 返回格式：2020-04-14 00:00:00
def str2datetime(datetimestr):
    return parse(datetimestr)

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

if __name__ == '__main__':
    sec = 1586498316
    time_stamp = 1537846361
    milisec = 1586498344522
    date_str = "2020-04-14"
    date_str_abbr = "20200414"
    '''DATE_FORMAT_ABBR, DATE_FORMAT, DATETIME_FORMAT, TIME_FORMAT'''
    #print(datetime2str(datetime.date.today(),DATE_FORMAT))
    #print(type(datetime2str(datetime.date.today(),DATE_FORMAT)))
    #print(diffrentPeriod(YEARLY,'2018-3-15','2018-11-10'))
    #print(secondsToDatetime2(time_stamp, DATE_FORMAT_ABBR))
    #str2datatime2(date_str,DATE_FORMAT)
    print(diff(datetime.date(year=1992, month=3, day=17),datetime.date(year=2020, month=3, day=17)))
    strdate = '2017-01-01'
    #print(getYearWeek(strdate))
    #print(getNowYearWeek())
    #print(getDayInweekMonday())
    #print(getDayLastWeekMondayAndSunday())
    # 输出2014年第35周的开始时间
    #print(getWeekFirstday('2014#35'))