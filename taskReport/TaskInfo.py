#coding=utf-8
debug=0
import datetime
from TaskInfoUtil import TaskInfoUtil
class TaskInfo(object):
    '''
    统计一段时间一个任务的信息
    '''
    def __init__(self,taskId,startTime,endTime):
        self.taskId=taskId
        self.startTime=startTime
        self.endTime=endTime
        self.dateList=[]
        self.overallTaskInfo=TaskInfoUtil(taskId,startTime,endTime)
        tmpTime=datetime.time(0,0,0)
        incTime=datetime.timedelta(days=1)
        startDay=startTime.combine(startTime.date(),tmpTime)
        curDay=startDay+incTime
        if endTime-startTime<incTime:
            self.dateList.append((startTime,endTime))
        else:
            while True:
                tmp=(max(startDay,startTime),min(curDay,endTime))
                self.dateList.append(tmp)
                startDay+=incTime
                if debug:
                    print startDay
                curDay+=incTime
                if startDay>endTime:
                    break
        self.everyDayInfo=[]
        self.everyDayInfo=self.getEveryDayInfo()

    def getDayList(self):
        return self.dateList

    def getEveryDayInfo(self):
        if self.everyDayInfo!=[]:
            return self.everyDayInfo
        everyDayInfo=[]
        for day in self.dateList:
            taskInfoUtil=TaskInfoUtil(self.taskId,day[0],day[1])
            dayInfo={}
            dayInfo['timeInterval']=day
            dayInfo['totalRunTime']=taskInfoUtil.getTotalRunTime()
            tmp=taskInfoUtil.getFrequency()
            dayInfo['needRunCount']=tmp[0]
            dayInfo['successCount']=tmp[1]
            dayInfo['failCount']=tmp[2]
            dayInfo['failTaskInfoList']=taskInfoUtil.getFailTaskInfoList()
            dayInfo['averageRunTime']=taskInfoUtil.getAverageRunTime()
            dayInfo['maxRunTime']=taskInfoUtil.getMaxRunTime()
            dayInfo['minRunTime']=taskInfoUtil.getMinRunTime()
            dayInfo['waitTime']=taskInfoUtil.getWaitTime()
            dayInfo['averageWaitTime']=taskInfoUtil.getAverageWaitTime()
            dayInfo['abnormalTask']=taskInfoUtil.getAbnormalTask()
            dayInfo['runTimeVariance']=taskInfoUtil.getVarianceByRunTime()
            everyDayInfo.append(dayInfo)
        return everyDayInfo

    def getTotalRunTime(self):
        '''
        返回总的运行时间
        :return:
        '''
        return self.overallTaskInfo.getTotalRunTime()

    def getTotalFrequency(self):
        '''
        获得这段时间需要运行的次数，运行成功的次数，运行失败的次数
        :return:
        '''
        return self.overallTaskInfo.getFrequency()

    def getTotalFailTaskInfoList(self):
        '''
        返回所有失败的任务信息列表
        :return:
        '''
        return self.overallTaskInfo.getFailTaskInfoList()

    def getTotalAverageRunTime(self):
        '''
        获得这段时间任务每次花费的时间
        :return:
        '''
        return self.overallTaskInfo.getAverageRunTime()

    def getTotalMaxRunTime(self):
        '''
        返回这段时间最大的任务运行时间
        :return:
        '''
        return self.overallTaskInfo.getMaxRunTime()

    def getTotalMinRunTime(self):
        '''
        返回这段时间这个任务的最短运行时间
        :return:
        '''
        return self.overallTaskInfo.getMinRunTime()

    def getTotalWaitTime(self):
        '''
        返回这段时间这个任务的一共等待时间
        :return:
        '''
        return self.overallTaskInfo.getWaitTime()

    def getTotalAverageWaitTime(self):
        '''
        返回平均每次执行等待的时间
        :return:
        '''
        return self.overallTaskInfo.getAverageWaitTime()

    def getSpecialTaskListByRunTime(self,lowLine,highLine):
        '''
        返回运行时间低于 lowLine倍，或者高于平均值的highLine倍的执行任务列表
        :param lowLine:
        :param highLine:
        :return:
        '''
        return self.overallTaskInfo.getSpecialTaskListByRunTime(lowLine,highLine)

    def getTotalAbnormalTask(self):
        '''
        返回所有不正常的任务的信息列表
        :return:
        '''
        return self.overallTaskInfo.getAbnormalTask()

    def getSortedListBy(self,rule,rever=True):
        '''
        排序的通用函数
        :param rule:
        :param rever:
        :return:
        '''
        tmpDict={}
        for key in self.everyDayInfo:
            tmpDict[key['timeInterval']]=key[rule]
        sortedList=sorted(tmpDict.iteritems(),key=lambda d:d[1],reverse=rever)
        return sortedList

    def getSortedListByVariance(self):
        '''
        根据运行时间的方差排序
        :return:
        '''
        return self.getSortedListBy('runTimeVariance')

    @staticmethod
    def unitTest():
        taskInfo=TaskInfo(4079,datetime.datetime(2014,1,2,12,3,11),datetime.datetime(2014,2,2,12,3,11))
        dayList=taskInfo.getDayList()
        totalRunTime=taskInfo.getTotalRunTime()
        totalWaitTime=taskInfo.getTotalWaitTime()
        totalAvRunTime=taskInfo.getTotalAverageRunTime()
        totalAvWaitTime=taskInfo.getTotalAverageWaitTime()
        maxRunTime=taskInfo.getTotalMaxRunTime()
        minRunTime=taskInfo.getTotalMinRunTime()
        fre=taskInfo.getTotalFrequency()
        varianceList=taskInfo.getSortedListByVariance()
        dayInfo=taskInfo.getEveryDayInfo()
        specialTaskList=taskInfo.getSpecialTaskListByRunTime(0.99,1.01)
        print u'获得的时间列表为'
        for day in dayList:
            print day
        comStr=u'任务%d在时间%s到时间%s的'%(4079,datetime.datetime(2014,1,2,12,3,11),datetime.datetime(2014,2,2,12,3,11))
        print u'%s总运行时间是%s'%(comStr,totalRunTime)
        print u'%s总等待时间为%s'%(comStr,totalWaitTime)
        print u'%s平均运行时间是%s'%(comStr,totalAvRunTime)
        print u'%s平均等待时间是%s'%(comStr,totalAvWaitTime)
        print u'%s最长运行时间是%s'%(comStr,maxRunTime)
        print u'%s最短运行时间是%s'%(comStr,minRunTime)
        print u'%s的需要运行的次数是%d,运行成功的次数是%d,运行失败的次数是%d'%(comStr,fre[0],fre[1],fre[2])
        print u'暂时不显示失败的任务'
        print u'拿出一天的情况测试每天任务的执行情况,我们拿第一天的情况'
        for key in dayInfo[0]:
            if key in ['maxRunTime','minRunTime']:
                print u'属性%s的值为:对于未被kill的任务时间为%s,对于被kill掉的任务时间为%s'%(key,dayInfo[0][key][0],dayInfo[0][key][1])
                pass
            else:
                print u'属性%s的值为%s'%(key,dayInfo[0][key])
        for i in range(0,2):
            print u'方差第%d大的执行时间是%s到%s，方差为%d'%(i+1,varianceList[i][0][0],varianceList[i][0][1],varianceList[i][1])
        for x in specialTaskList:
            print u'id为%d的任务执行时间为平局值的%f倍'%(x[0],x[1])

if __name__=="__main__":
    if debug:
        print u'调用测试'
    TaskInfo.unitTest()