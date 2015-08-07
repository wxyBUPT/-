#coding=utf-8
from ScheduleLogInfo import ScheduleLogInfo
import datetime
import copy
class TaskError(Exception):
    def __init__(self,value):
        self.value=value
    def __str__(self):
        return repr(self.value)
class TaskInfoUtil(object):
    '''
    组件的工具类
    '''
    def __init__(self,taskId,startTime,endTime):
        '''
        taskId，类型为long，
        startTime,endTime类型均为datetime.datetime
        返回startTime 到 endTime时间段内的任务信息
        self.info 中的任务比较重要，即异常的任务
        :param taskId:
        :param startTime:
        :param endTime:
        :return:
        '''
        self.taskId=taskId
        self.startTime=startTime
        self.endTime=endTime
        try:
            ScheduleLogInfo[taskId]
        except:
            raise TaskError(u"ScheduleLogInfo中没有taskId=%d的信息"%taskId)
        #在下面的发现异常的字典里面，key 异常名 value：id组成的一个列表
        info={}
        info['noRun']=[]
        info['noEnd']=[]
        info['noReady']=[]
        self.info=info
        self.runList=copy.deepcopy(ScheduleLogInfo[self.taskId])
        #以下循环确保列表中的数据合法且符合规律
        for run in self.runList:
            if run['exe_date']<startTime or run['exe_date']>=endTime:
                self.runList.remove(run)
                continue
            if run['ready_time']==None:
                self.info['noReady'].append(run['id'])
                try:
                    self.runList.remove(run)
                except:
                    pass
            if run['running_time']==None:
                self.info['noRun'].append(run['id'])
                try:
                    self.runList.remove(run)
                except:
                    pass
            if run['leave_time']==None and run['kill_time']==None:
                self.info['noEnd'].append(run['id'])
                try:
                    self.runList.remove(run)
                except:
                    pass

    def getTotalRunTime(self):
        '''
        获得这段时间总共的运行时间.
        datetim.timedelta()形式的
        :return:
        '''
        totleRunTime=datetime.timedelta()
        for run in self.runList:
            if run['leave_time']!=None:
                totleRunTime=totleRunTime+run['leave_time']-run['running_time']
            elif run['kill_time']!=None:
                totleRunTime=totleRunTime+run['kill_time']-run['running_time']
            else:
                print u'来自getTotalRunTime的错误：TaskInfoUtil未能去除无效的数据'
        return totleRunTime

    def getFrequency(self):
        '''
        获得这段时间这个任务各种情况的次数
        分别返回任务本身需要执行的次数，任务自己执行成功的次数，任务被kill的次数
        :return:
        '''
        class FreInfo(object):
            '''
            内部数据结构，包含三种参数信息
        :return:
        '''
            def __init__(self):
                self.needRunTime=0
                self.successTime=0
                self.failTime=0
        freInfo=FreInfo()
        for run in self.runList:
            freInfo.needRunTime+=1
            if run['leave_time']!=None:
                freInfo.successTime+=1
            elif run['kill_time']!=None:
                freInfo.failTime+=1
            else:
                print u'在TaskInfoUtil中的FreInfo中有任务信息不完整'
        return freInfo.needRunTime,freInfo.successTime,freInfo.failTime

    def getFailTaskInfoList(self):
        '''
        获得被手动
        获取失败的任务的时间列表
        info以id query_name ready_time 排序
        :return:
        '''
        faileList=[]
        for run in self.runList:
            if run['leave_time']==None:
                faileInfo=[run['id'],run['query_name'],run['ready_time']]
                faileList.append(faileInfo)
            else:
                pass
        return faileList

    def getAverageRunTime(self):
        '''
        获得任务平均的运行时间，运行时间是指为用户分配了资源的时间
        返回datetime.timedelat 形式的时间
        :return:
        '''
        totalRunTime=self.getTotalRunTime()
        totalFrequency=self.getFrequency()[0]
        if totalFrequency!=0:
            return totalRunTime/totalFrequency
        else:
            return datetime.timedelta()

    def getMaxRunTime(self):
        '''
        获得任务执行的最长时间，分别返回正常执行结束以及手动kill掉的任务的时间
        返回datetime.timedelat 形式的时间
        :return:
        '''
        #正常执行结束的任务的最大时间
        maxTime=datetime.timedelta()
        #手动kill的任务最大时间
        maxKillTaskTime=datetime.timedelta()
        for run in self.runList:
            if run['leave_time']!=None:
                curTime=(run['leave_time']-run['running_time'])
                maxTime=curTime if (curTime>maxTime) else maxTime
            elif run['kill_time']!=None:
                curTime=run['kill_time']-run['running_time']
                maxKillTaskTime=curTime if curTime>maxKillTaskTime else maxKillTaskTime
            else:
                print u'在TaskInfoUtil中的getMaxRunTime出现了问题'
        return maxTime,maxKillTaskTime

    def getMinRunTime(self):
        '''
        获得任务最短的执行时间，分别返回正常结束和kill掉的任务的最短时间
        返回datetime.timedelta形式
        :return:
        '''
        minTime=datetime.timedelta()
        minKillTaskTime=datetime.timedelta()
        for run in self.runList:
            if run['leave_time']!=None:
                minTime=run['leave_time']-run['running_time']
                break
        for run in self.runList:
            if run['kill_time']!=None:
                minKillTaskTime=run['kill_time']-run['running_time']
                break
        for run in self.runList:
            if run['leave_time']!=None:
                curTime=run['leave_time']-run['running_time']
                minTime=curTime if curTime<minTime else minTime
            elif run['kill_time']!=None:
                curTime=run['kill_time']-run['running_time']
                minKillTaskTime=curTime if curTime<minKillTaskTime else minKillTaskTime
            else:
                print u'在taskinfoutil中的getminruntime出行了问题'
        return minTime,minKillTaskTime

    def getWaitTime(self):
        '''
        返回任务的等待时间，返回的是总时间
        返回的是datetime.timedelate
        :return:
        '''
        waitTime=datetime.timedelta()
        for run in self.runList:
            waitTime=waitTime+run['running_time']-run['ready_time']
        return waitTime

    def getAverageWaitTime(self):
        '''
        返回这段时间内这个任务的平均等待时间
        :return:
        '''
        totalWaitTime=self.getWaitTime()
        runFrequency=self.getFrequency()[0]
        if runFrequency!=0:
            return totalWaitTime/runFrequency
        else:
            return datetime.timedelta()

    def getAbnormalTask(self):
        '''
        获得异常的任务
        :return:
        '''
        return self.info

    def getVarianceByRunTime(self):
        '''
        返回任务执行时间的方差
        :return:
        '''
        aveRunTime=self.getAverageRunTime().total_seconds()
        variance=0
        for run in self.runList:
            if run['leave_time']!=None:
                runTime=run['leave_time']-run['running_time']
            elif run['kill_time']!=None:
                runTime=run['kill_time']-run['running_time']
            else:
                print u'在TaskInfoUtil中的getVarianceByRunTime函数中找到非法的数据库项'
                continue
            runTime=runTime.total_seconds()
            variance+=(runTime-aveRunTime)**2
        return variance

    def getSpecialTaskListByRunTime(self,lowLine,highLine):
        '''
        返回低于平均值 lowLine倍，或者高于平均值的highLine倍的执行任务的列表
        :return:
        '''
        specialList=[]
        if lowLine <0 or highLine <0:
            return specialList
        aveRunTime=self.getAverageRunTime().total_seconds()
        if aveRunTime==0:
            return specialList
        for run in self.runList:
            if run['leave_time']!=None:
                runTime=run['leave_time']-run['running_time']
            elif run['kill_time']!=None:
                runTime=run['kill_time']-run['running_time']
            else:
                print u'在TaskInfoUtil中的getVarianceByRunTime函数中找到非法的数据库项'
                continue
            runTime=runTime.total_seconds()
            rTiDivATi=runTime/aveRunTime
            if rTiDivATi<lowLine or rTiDivATi>highLine:
                specialList.append([run['id'],rTiDivATi])
        return specialList


    @staticmethod
    def unitTest():
        '''
        单元测试
        :return:
        '''
        taskInfoUtil=TaskInfoUtil(4079,datetime.datetime(2014,1,2),datetime.datetime(2015,9,1))
        totalRunTime=taskInfoUtil.getTotalRunTime()
        print u'任务4079的总运行时间是%s'%totalRunTime
        frequency=taskInfoUtil.getFrequency()
        print u'任务需要跑的次数为：%d,任务成功的次数为:%d,任务被kill掉的次数为:%d'%(frequency[0],frequency[1],frequency[2])
        abnormalTask=taskInfoUtil.getAbnormalTask()
        print u'输出出现异常的任务'
        print u'未准备好的任务Id列表'
        print abnormalTask['noReady']
        print u'未能开始执行的任务ID列表：'
        print abnormalTask['noRun']
        print u'未能停止执行的任务Id列表:'
        print abnormalTask['noEnd']

        (maxTime,maxKillTaskTime)=taskInfoUtil.getMaxRunTime()
        print u'未被杀死的任务执行的最长时间是%d,被杀死任务执行最长时间是%d'%(maxTime.total_seconds(),maxKillTaskTime.total_seconds())
        (minTime,minKillTaskTime)=taskInfoUtil.getMinRunTime()
        print u'未被杀死的任务执行的最短时间是%d,被杀死的任务执行的最短时间是%d'%(minTime.total_seconds(),minKillTaskTime.total_seconds())
        waitWaitTime=taskInfoUtil.getWaitTime()
        print u'任务的总等待时间是%d'%waitWaitTime.total_seconds()
        averageWaitTime=taskInfoUtil.getAverageWaitTime()
        print u'任务的平均等待时间是%d'%averageWaitTime.total_seconds()
        failTask=taskInfoUtil.getFailTaskInfoList()
        print u'执行失败的任务有'
        for i in failTask:
            print i
        runTimeVariance=taskInfoUtil.getVarianceByRunTime()
        print u'任务4079运行时间的方差是%d'%runTimeVariance
        specilaList=taskInfoUtil.getSpecialTaskListByRunTime(0.8,1)
        for x in specilaList:
            print u'id为%d的任务执行时间为平均时间的%f倍'%(x[0],x[1])

if __name__=='__main__':
    TaskInfoUtil.unitTest()