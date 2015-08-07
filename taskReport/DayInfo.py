#coding=utf-8
import datetime
from ScheduleLogInfo import ScheduleLogInfo
from TaskInfoUtil import TaskInfoUtil

class DayInfo(object):
    '''
    一段时间内任务的整体情况，根据startTime，endTime初始化
    '''
    def __init__(self,startTime,endTime):
        '''
        startTime,endTime类型为dateTime.dateTime
        :param startTime:
        :param endTime:
        :return:
        '''
        self.startTime=startTime
        self.endTime=endTime
        self.catch={}
        self.catch=self.calculateCatch()

    def calculateCatch(self):
        '''
        初始化缓存，缓存中保存每一个任务的信息
        :return:
        '''
        catch={}
        for key in ScheduleLogInfo:
            taskInfoUtil=TaskInfoUtil(key,self.startTime,self.endTime)
            #代表taskInfoDict
            tIDict={}
            tIDict['runTime']=taskInfoUtil.getTotalRunTime()
            tmp=taskInfoUtil.getFrequency()
            tIDict['needRunCount']=tmp[0]
            tIDict['sucCount']=tmp[1]
            tIDict['failCount']=tmp[2]
            tIDict['aveRunTime']=taskInfoUtil.getAverageRunTime()
            tIDict['maxRunTime']=taskInfoUtil.getMaxRunTime()
            tIDict['minRunTime']=taskInfoUtil.getMinRunTime()
            tIDict['waitTime']=taskInfoUtil.getWaitTime()
            tIDict['aveWaitTime']=taskInfoUtil.getAverageWaitTime()
            tIDict['variance']=taskInfoUtil.getVarianceByRunTime()
            catch[key]=tIDict
        return catch

    def getRunTime(self):
        '''
        获得总的执行时间
        :return:
        '''
        runTime=datetime.timedelta()
        for key in self.catch:
            runTime+=self.catch[key]['runTime']
        return runTime

    def getWaitTime(self):
        '''
        获得总共的等待时间
        :return:
        '''
        waitTime=datetime.timedelta()
        for key in self.catch:
            waitTime+=self.catch[key]['waitTime']
        return waitTime

    def getTaskCount(self):
        '''
        返回需要执行的任务数量
        :return:
        '''
        taskCount=0
        for key in self.catch:
            taskCount+=self.catch[key]['needRunCount']
        return taskCount

    def getAveRunTime(self):
        '''
        返回平均的执行时间
        :return:
        '''
        aveRunTime=datetime.timedelta()
        runTime=self.getRunTime()
        taskCount=self.getTaskCount()
        if taskCount != 0:
            aveRunTime=runTime/taskCount
        else:
            print u'在DayInfo中的getAveRunTime中出现了执行次数为零的任务'
        return aveRunTime

    def getAveWaitTime(self):
        '''
        返回平均的等待时间
        :return:
        '''
        aveWaitTime=datetime.timedelta()
        wTime=self.getWaitTime()
        tCount=self.getTaskCount()
        if tCount!=0:
            aveWaitTime=wTime/tCount
        else:
            print u'在DayInfo的getAveWaitTime中有任务执行数量为零的任务'
        return aveWaitTime

    def getSortedListBy(self,rule,rever=True):
        '''
        通用的排序函数
        :param rule:
        :return:
        '''
        tmpDict={}
        for key in self.catch:
            tmpDict[key]=self.catch[key][rule]
        sortedList=sorted(tmpDict.iteritems(),key=lambda d:d[1],reverse=rever)
        return sortedList

    def getSortedListByVariance(self):
        '''
        返回方差从大到小排序的任务列表
        :return:
        '''
        return self.getSortedListBy('variance')

    def getSortedListByRunTime(self):
        '''
        返回根据运行时间从大到小排序的任务列表
        :return:
        '''
        return self.getSortedListBy('runTime')

    def getSortedListByWaitTime(self):
        '''
        返回根据任务的等待时间从大到小排序的任务列表
        :return:
        '''
        return self.getSortedListBy('waitTime')

    def getSortedListByAveRunTime(self):
        '''
        返回根据任务的平均运行时间从打到小排序的任务列表
        :return:
        '''
        return self.getSortedListBy('aveRunTime')

    def getSortedListByAveWaitTime(self):
        '''
        返回根据任务的平均等待时间从大到小排序的任务列表
        :return:
        '''
        return self.getSortedListBy('aveWaitTime')



    @staticmethod
    def unitTest():
        '''
        DayInfo的单元测试
        :return:
        '''
        dayInfo=DayInfo(datetime.datetime(2014,1,2,12,3,11),datetime.datetime(2014,2,2,12,3,11))
        waitTime=dayInfo.getWaitTime()
        print u'当前时间段内的总等待时间为%s'%waitTime
        taskCount=dayInfo.getTaskCount()
        print u'时间段内需要执行的任务总量为%d'%taskCount
        aveWaitTime=dayInfo.getAveWaitTime()
        print u'平均等待时间为%s'%aveWaitTime
        runTime=dayInfo.getRunTime()
        print u'总的执行时间是%s'%runTime
        aveRunTime=dayInfo.getAveRunTime()
        print u'平均每个任务的执行时间是%s'%aveRunTime
        sortedListByRunTime=dayInfo.getSortedListByRunTime()
        print u'获得执行时间最长的前十个task'
        for i in range(0,11):
            print u'执行时间第%d长的任务为%d,执行时间为%s'%(i+1,sortedListByRunTime[i][0],sortedListByRunTime[i][1])
        sortedListByWaitTime=dayInfo.getSortedListByWaitTime()
        print u'等待时间最长的前十个task'
        for i in range(0,11):
            print u'等待第%d长的任务为%d,执行时间为%s'%(i+1,sortedListByWaitTime[i][0],sortedListByWaitTime[i][1])
        sortedListByAveRunTime=dayInfo.getSortedListByAveRunTime()
        print u'平均执行时间最长的前十个task'
        for i in range(0,11):
            print u'平均执行时间第%d长的任务为%d,执行时间为%s'%(i+1,sortedListByAveRunTime[i][0],sortedListByAveRunTime[i][1])
        sortedListByAveWaitTime=dayInfo.getSortedListByAveWaitTime()
        print u'平均等待时间最长的前十个task'
        for i in range(0,11):
            print u'平均等待时间第%d长的任务为%d,执行时间为%s'%(i+1,sortedListByAveWaitTime[i][0],sortedListByAveWaitTime[i][1])
        sortedListByVariance=dayInfo.getSortedListByVariance()
        print u'方差最大的前十个task'
        for i in range(0,10):
            print u'方差第%d大的任务为%d,方差为%s'%(i+1,sortedListByVariance[i][0],sortedListByVariance[i][1])


if __name__=="__main__":
    DayInfo.unitTest()

