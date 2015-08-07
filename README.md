# -
Django-Python项目。
主要的功能需求是根据实习公司的线上执行的任务提供一个全局的报表功能。
线上任务在数据库中有如下字段：
class Schedule_Log(models.Model):

    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task)
    result = models.IntegerField(choices=Schedule_Status.result_choice)
    desc = models.CharField(null=True,max_length=256）
    exe_date = models.DateTimeField(）
    ready_time = models.DateTimeField(null=True,default='0000-00-00 00:00:00')
    running_time = models.DateTimeField(null=True,default='0000-00-00 00:00:00')
    leave_time = models.DateTimeField(null=True,default='0000-00-00 00:00:00')
    kill_time = models.DateTimeField(null=True,blank=True)
    query_name = models.CharField(max_length=128)

代码的主要有两个功能
（1）输入参数为任务外键task，其实时间startTime，结束时间endTime 均为datetime.datetime格式
     功能是：（1）返回这段时间整体的任务运行情况 （2）返回每天这个任务的运行情况
     运行情况包括：总的运行时间，总的等待时间，平均运行时间，平均等待时间，最长运行时间，最短运行时间，需要运行的次数
     运行成功的次数，运行失败的次数，每天或者这段时间内的运行时间方差由大到小排列的任务列表
     以及低于或者超过运行时间平均值多少倍的异常任务列表
（2）输入参数为起始时间startTime，结束时间endTime，均为datetime.datetime格式
     功能是：（1）返回这段时间的整体 运行情况  （2）返回这段时间每天的运行情况
     运行情况包括，运行的时间区间数组，平均每个任务的执行时间，所有任务的总执行时间，总等待时间，
     这段时间之内执行的任务总量，这段时间内任务的等待时间，这段是时间执行的任务方差最大的十个任务，
     每天的任务情况包运行时间区间，所有任务的等待时间，运行的任务数，运行的平均时间，平均等待时间，
     运行时间最长的前十个任务，等待时间最长的 前十个任务，方差最大前十个任务
