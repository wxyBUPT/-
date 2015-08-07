#coding=utf-8
#把bdms中schedule_log 字段的内容存到一个变量中
debug=0
if debug:
    print u'ScheduleLogInfo启用了调试'
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","settings")
import sys
sys.path.append("..")
from ide.models import Schedule_Log
#key 位task_id value为列表 列表中的内容为每一次执行的字典，字典中包括每一次执行的信息
ScheduleLogInfo={}
def calScheduleLogInfo():
    scheduleList = Schedule_Log.objects.all()
    for schedule in scheduleList:
        index=schedule.task_id
        try:
            ScheduleLogInfo[index]
        except:
            ScheduleLogInfo[index]=[]
        schDict={}
        schDict['query_name']=schedule.query_name
        schDict['id']=schedule.id
        schDict['result']=schedule.result
        schDict['exe_date']=schedule.exe_date
        schDict['ready_time']=schedule.ready_time
        schDict['running_time']=schedule.running_time
        schDict['leave_time']=schedule.leave_time
        schDict['kill_time']=schedule.kill_time
        ScheduleLogInfo[index].append(schDict)
    def unitTest():
        print u'task的数量是%d'%len(ScheduleLogInfo)
        count=2
        for i in ScheduleLogInfo:
            print i
            print i,u':',ScheduleLogInfo[i][1]
            print type(ScheduleLogInfo[i][1]['id'])
            print type(ScheduleLogInfo[i][1]['ready_time'])
            print '\n\n'
            count=count-1
            if count<0:
                break
    if debug:
        unitTest()

calScheduleLogInfo()
if debug:
    print len(ScheduleLogInfo)

