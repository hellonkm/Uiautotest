#!/usr/bin/python
# -*- coding=utf-8 -*-
import logging
from os import sys
sys.path.append("..")
from imp import reload
reload(sys)
from testplatform.common.basicLib import basicLib
from testplatform.webUi.testWeb import testWeb
from testplatform.webUi.webCase import webCase
import json,threading
import os,time,datetime

'''执行批量用例任务'''
class TESTExecute(object):

    def __init__(self,id,operatorId):
        self.id = id 
        self.operatorId =operatorId

    def testExe(self,data,reportTd):
        caseId = data["caseId"]
        createdTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = webCase().getDataByCaseId(caseId)
        for indexSec in range(len(data)):
            stepData = data[indexSec]
            stepValue = stepData["step_value"]
            executionStep = stepData["execution_step"]
            typeData = stepData["type"]
            element = stepData["element"]
            keyName = stepData["key_name"]
            sort = stepData["sort"]
            casesName = stepData["cases_name"]
            stepName = stepData["step_name"]

            try:            
                sql = "INSERT INTO ui_report_cases(report_id,cases_id,key_name,execution_step,sort,cases_name,step_name,created_time,result) values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',0)"% (reportTd,caseId,keyName,executionStep,sort,casesName,stepName,createdTime)
                basicLib().updateSql(sql)
                sqlId = "select id from ui_report_cases where report_id =\'%s\' and sort =\'%s\' " % (reportTd,sort)            
                id = (basicLib().getAllData(sqlId))[0]["id"]
                res = self.executionOneCase(typeData,executionStep,stepValue,id,element)
                if res == 'fail':
                    sql = "update ui_report_cases set result = 1 where id = \'%s\' "% (id)
                    basicLib().updateSql(sql)
                    sql = "update ui_report_task set result = 1 where id = \'%s\' "% (reportTd)
                    basicLib().updateSql(sql)
                    result = {"result":"fail","caseId":caseId}
                    return(result)

            except Exception  as e: 
                    sql = "update ui_report_cases set result = 1 id = \'%s\' "% (id)
                    basicLib().updateSql(sql)
                    sql = "update ui_report_task set result = 1 where id = \'%s\' "% (reportTd)
                    basicLib().updateSql(sql)                    
                    logging().debug('Error : {}'.format(e))
                    # webCase().close()
                    result = {"result":"fail","caseId":caseId}
                    return(result)                       
                # else:
                #     sql = "update ui_assertion set result = 0 where cases_id = %s "% (caseId)
                #     basicLib().updateSql(sql)
                #     webCase().close
                #     result = {"result":"success","caseId":caseId}
            # except Exception  as e:
            #     print ('Error : {}'.format(e))
            #     sql = "update ui_assertion set result = 0 where cases_id = %s "% (caseId)
            #     basicLib().updateSql(sql)
            #     return {"result":'fail',"caseId":caseId}    
            indexSec = indexSec +1
        # assertSql = "select element,assert_value,type from ui_assertion where cases_id = %s;" %(caseId)
        # res = basicLib().getAllData(assertSql)
        # assertTypeData = res[0]
        # assertType=assertTypeData["type"]
        # assertValue = assertTypeData["assert_value"]
        # assertElement = assertTypeData["element"]
        # result = webCase().assertionResult(assertType,assertValue,assertElement)
        sql = "update ui_report_task set result = 0 where id = \'%s\'" % reportTd
        basicLib().updateSql(sql)                    
        result = {"result":"success","caseId":caseId}
        return (result)

    def executionOneCase(self,type,executionStep,typeData,id,element):

        dir = os.getcwd()        
        if type == '1':
            if executionStep == '-1':
                '''
                    openChrome
                '''
                res =testWeb().visit(typeData)
                filename = "/home/zhangweiyang/coe_frontend/static/images/%s.png" % (id)
                testWeb().getScreenshotAsFile(filename)
                webCase().insertReportPicture(id)

            elif executionStep == '-2': 
                testWeb().executeScript(typeData)
                filename = "/home/zhangweiyang/coe_frontend/static/images/%s.png" % (id)
                testWeb().getScreenshotAsFile(filename)
                webCase().insertReportPicture(id)

            elif executionStep == '-3':
                testWeb().waitSleep(typeData)

            elif executionStep == '-4':
                testWeb().refreshBrowser()
                filename = "/home/zhangweiyang/coe_frontend/static/images//%s.png" % (id)
                testWeb().getScreenshotAsFile(filename)
                webCase().insertReportPicture(id)

            elif executionStep == '-5':
                testWeb().backPage()
                filename = "/home/zhangweiyang/coe_frontend/static/images//%s.png" % (id)
                testWeb().getScreenshotAsFile(filename)
                webCase().insertReportPicture(id)

            elif executionStep == '-6':
                testWeb().forwardPage()
                filename = "/home/zhangweiyang/coe_frontend/static/images//%s.png" % (id)
                testWeb().getScreenshotAsFile(filename)
                webCase().insertReportPicture(id)

            elif executionStep == '-7':
                testWeb().switchFrame()
                testWeb().forwardPage()
                filename = "/home/zhangweiyang/coe_frontend/static/images//%s.png" % (id)
                testWeb().getScreenshotAsFile(filename)
                webCase().insertReportPicture(id)  

            elif executionStep == '1':                    
                res =testWeb().findElementById(typeData)
                filename ="/home/zhangweiyang/coe_frontend/static/images//%s.png" % (id)
                testWeb().getScreenshotAsFile(filename)
                webCase().insertReportPicture(id)

            elif executionStep == '2':    
                res =testWeb().findElementByName(typeData)
                filename = "/home/zhangweiyang/coe_frontend/static/images//%s.png" % (id)
                testWeb().getScreenshotAsFile(filename)
                webCase().insertReportPicture(id)

            elif executionStep == '3': 
                res =testWeb().findElementByClassName(typeData)
                filename = "/home/zhangweiyang/coe_frontend/static/images//%s.png" % (id)
                testWeb().getScreenshotAsFile(filename)
                webCase().insertReportPicture(id)

            elif executionStep == '4':
                res =testWeb().findElementByTagName(typeData)
                filename = "/home/zhangweiyang/coe_frontend/static/images//%s.png" % (id)
                testWeb().getScreenshotAsFile(filename)
                webCase().insertReportPicture(id)

            elif executionStep == '5':
                res =testWeb().findElementByXpath(typeData)
                filename = "/home/zhangweiyang/coe_frontend/static/images//%s.png" % (id)
                testWeb().getScreenshotAsFile(filename)
                webCase().insertReportPicture(id)

            elif executionStep == '6':
                res =testWeb().findElementByCssSelector(typeData)
                filename = "/home/zhangweiyang/coe_frontend/static/images//%s.png" % (id)
                testWeb().getScreenshotAsFile(filename)
                webCase().insertReportPicture(id)

            elif executionStep == '7':
                res =testWeb().findElementByLinkText(typeData)
                filename = "/home/zhangweiyang/coe_frontend/static/images//%s.png" % (id)
                testWeb().getScreenshotAsFile(filename)
                webCase().insertReportPicture(id)

            elif executionStep == '8':
                res =testWeb().findElementByPartialLinkText(typeData)
                filename = "/home/zhangweiyang/coe_frontend/static/images//%s.png" % (id)
                testWeb().getScreenshotAsFile(filename)
                webCase().insertReportPicture(id)

        if type == '2':
            if executionStep =='1001':
                res =testWeb().byIdSendKey(typeData,element)
                filename = "/home/zhangweiyang/coe_frontend/static/images//%s.png" % (id)
                testWeb().getScreenshotAsFile(filename)
                webCase().insertReportPicture(id)

            elif executionStep == '1002':
                res =testWeb().byNameSendKey(typeData,element)
                filename = "/home/zhangweiyang/coe_frontend/static/images//%s.png" % (id)
                testWeb().getScreenshotAsFile(filename)
                webCase().insertReportPicture(id)

            elif executionStep =='1003':
                resAssert=testWeb().assertText(typeData)                
                filename = "/home/zhangweiyang/coe_frontend/static/images//%s.png" % (id)
                testWeb().getScreenshotAsFile(filename)
                webCase().insertReportPicture(id)                
                if typeData == resAssert:
                    res ="success"
                    return (res)
                else:
                    res = "fail"
                    return (res)

        if type == '3':
            res = os.system(dir + typeData)
            testWeb().forwardPage()
            filename = "/home/zhangweiyang/coe_frontend/static/images//%s.png" % (id)
            testWeb().getScreenshotAsFile(filename)
            webCase().insertReportPicture(id)                     
            if res == 0:
                res = {"code":0,"message":"success"}
                return (json.dumps(res).encode('utf-8').decode('unicode_escape'))
            else:
                res = {"code":0,"message":"Fail"}
                return (json.dumps(res).encode('utf-8').decode('unicode_escape'))                           
        
        if type == '4':
            if platform.system() == "Windows":
                slash = '\\'
                executing = "C:/Python37/python.exe " + " %s%s %s" % (dir,executionStep,typeData)
            else:
                slash = '/'
                executing = "python3 " + " %s%s %s" % (dir,executionStep,typeData)                
            res = os.popen(executing)
            filename = "/home/zhangweiyang/coe_frontend/static/images//%s.png" % (id)
            testWeb().getScreenshotAsFile(filename)
            webCase().insertReportPicture(id)                     
            return (res)

        if type == '5':            
            if platform.system() == "Windows":
                slash = '\\'
                executing = "C:/Python37/python.exe " + " %s%s %s %s" % (dir,executionStep,element,typeData)

            else:
                slash = '/'
                executing = "python3 " + " %s%s %s %s" % (dir,executionStep,element,typeData)                
            res = os.popen(executing)
            filename = "/home/zhangweiyang/coe_frontend/static/images//%s.png" % (id)
            testWeb().getScreenshotAsFile(filename)
            webCase().insertReportPicture(id)                     
            return (res)

# MyThread.py线程类
class MyThread(threading.Thread):
    
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args
        self.result = []

    def run(self):
        time.sleep(0.1)
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None

if __name__ == '__main__':
    w = TESTExecute(sys.argv[1],sys.argv[2])
    taskId = sys.argv[1]
    operatorId = sys.argv[2]
    createdTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insertSql= "INSERT INTO ui_report_task(task_id,created_time,updated_time,ast_operator,status,deleted)VALUES(\'%s\',\'%s\',\'%s\',\'%s\','0','0')" %(taskId,createdTime,createdTime,operatorId)
    basicLib().updateSql(insertSql)
    sqlId = "select id from ui_report_task order by id DESC limit 1"
    reportTd = (basicLib().getAllData(sqlId))[0]["id"]
    sql =  "select all_cases_id from ui_execute_task_cases where id = %s"% (sys.argv[1])
    thr = []
    res = (basicLib().getAllData(sql))[0]["all_cases_id"]
    res = json.loads(res)
    sum = len(res)
    
    for i in range(sum):
        task = MyThread(w.testExe,(res[i],reportTd))
        task.start()
        task.join()
        thr.append(task.get_result())
    sumSuccess = 0
    sumFail = 0
    caseIdSuccess = []
    caseIdFail = []
    
    for index in range(len(thr)):
        sumResult = thr[index]
        if sumResult["result"] == "success":
            sumSuccess = sumSuccess +1
            id = {"caseId":sumResult["caseId"]}
            caseIdSuccess.append(id)
        else:
            sumFail = sumFail +1
            id = {"caseId":sumResult["caseId"]}
            caseIdFail.append(id)  
        index = index+1            
    endTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # sql = "select task_id from ui_report_task where task_id = \'%s\'"%(taskId)
    # res = basicLib().getAllData(sql)
    caseIdSuccess = json.dumps(caseIdSuccess)
    caseIdFail = json.dumps(caseIdFail)
    sql = "update ui_report_task set sum = \'%s\' ,sum_success = \'%s\',sum_fail = \'%s\',case_id_fail = \'%s\',case_id_success = \'%s\',status = 1 where task_id = \'%s\' and id = \'%s\'"%(sum,sumSuccess,sumFail,caseIdFail,caseIdSuccess,taskId,reportTd)
    basicLib().updateSql(sql)

    # sql= "INSERT INTO ui_report_task(sum,task_id,sum_success,sum_fail,case_id_fail,case_id_success,created_time,updated_time,ast_operator)VALUES(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" %(sum,taskId,sumSuccess,sumFail,caseIdFail,caseIdSuccess,createdTime,endTime,operatorId)
    # basicLib().updateSql(sql)
    # if res ==():
    #     # if case_id_fail = = []:
    #     sql= "INSERT INTO ui_report_task(sum,task_id,sum_success,sum_fail,case_id_fail,case_id_success,created_time,updated_time)VALUES(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" %(sum,taskId,sumSuccess,sumFail,caseIdFail,caseIdSuccess,createdTime,endTime)
    #     print(sql)
    #     basicLib().updateSql(sql)
    # else:
    #     sql = insert 

