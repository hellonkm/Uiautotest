# -*- coding: utf-8 -*-
# from os import sys
# sys.path.append("..")
# from imp import reload
# reload(sys)
from flask import Flask,request,redirect,url_for,jsonify
from flask_restful import Api
import json,datetime,re,os
from common.basicLib import basicLib
from webUi.webCase import webCase
from werkzeug.utils import secure_filename
import platform,jwt
from functools import wraps
from page.pageSql import pageSql
from page.recognitionElement import recognitionElement
from Logging import Logging 

app = Flask(__name__)
api = Api(app)
uploadFolder = 'keyword'
app.config['uploadFolder'] = uploadFolder
if not os.path.exists(uploadFolder):
    os.makedirs(uploadFolder)
else:   
    pass    
allowExtensions = set(['py'])

@app.route('/')
def index():
    return '404 NOT FOUND'

def user(func):
    @wraps(func)    
    def inner(*args, **kwargs):
        # 获取token
        token = request.headers.get('token')
        if not token:
            return jsonify({"code": "4103", "message": "缺少参数"})

        data = {"roleId":"","roleName":""}
        # roleId = data['roleId']
        roleName = data['roleName']
        # 判断
        if roleName == '管理员':
            return func(*args, **kwargs)
        else:
            return jsonify({"code": "403", "message": "您没此权限，请联系管理员"})
    return inner

#用例相关
@app.route('/ui/createcase',methods = ['POST'])
def createCase():
    Logging().info("/ui/createcase/")
    Logging().info(request.json)
    casesName = request.json["casesName"].strip()
    projectId = request.json["projectId"].strip()
    moduleId = request.json["moduleId"].strip()
    operator = request.json["operator"].strip()
    if not casesName or not projectId or not moduleId or not operator:
        return jsonify({"code": "4103", "message": "缺少参数"})
    step = request.json["step"]
    if projectId == "" or casesName  == "" or moduleId == "" or step == "":
        res = {"code":"4103","message":"缺少参数"}
        return (json.dumps(res))
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    caseId = webCase().getCaseId(casesName,operator,projectId,moduleId,dt)
    if not caseId:
        return (json.dumps({"code":"4103","message":"缺少参数"}))
    for index in range(len(step)):
        stepOne = step[index]
        browserSession = stepOne["browserSession"]
        selectElement = stepOne["selectElement"].strip()
        elementMethods = stepOne["elementMethods"].strip()
        elementId = stepOne["elementId"].strip()
        deleted = stepOne["deleted"].strip()        
        keyName = stepOne["keyName"].strip()
        executionStep = (webCase().searchKeyData(keyName))["key_step"].strip()
        stepValue = stepOne["stepValue"].strip()
        element = stepOne["element"].strip()
        typeNum = (webCase().searchKeyData(keyName))["key_type"].strip()
        sort = stepOne["sort"]
        stepName = stepOne["stepName"].strip()
        sql = "INSERT INTO ui_auto_cases(cases_name,type,project_id,module_id,cases_id,execution_step,step_value,element,created_time,updated_time,ast_operator,sort,deleted,step_name,key_name,element_Id,browser_session,select_element,element_methods) VALUES(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" % (casesName,typeNum,projectId,moduleId,caseId,executionStep,stepValue,element,dt,dt,operator,sort,deleted,stepName,keyName,elementId,browserSession,selectElement,elementMethods)
        Logging().info(sql)
        res = basicLib().updateSql(sql)
        if res == "connecterror":
            res = {"code":"4003","msg":"data error"}
            return (json.dumps(res))       

    if res == "connecterror":
        res = {"code":"4003","msg":"data error"}
        return (json.dumps(res))
    data = {	
            "caseId":caseId,
            "projectId":projectId,
            "moduleId": moduleId,
            "casesName":casesName,
            "step":step,
            "operator":operator
        }                 
    res = {"code":0,"message":"success","data":data}
    return (json.dumps(res).encode('utf-8').decode('unicode_escape'))

@app.route('/ui/updatecase',methods = ['POST'])
@user
def updateCase():
    Logging().info("/ui/updatecase/")
    Logging().info(request.json)    
    projectId = request.json["projectId"]
    caseId = request.json["caseId"]
    casesName = request.json["casesName"]
    moduleId = request.json["moduleId"]
    # createdTime = request.json["createdTime"]
    operator = request.json["operator"]
    step = request.json["step"]
    # id_list = []
    if casesName  == "" or moduleId == "" or step == "" or caseId == "":
        res = {"code":"4103","msg":"parameter error"}
        return (json.dumps(res))
    dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updateDeleteSql = "update ui_auto_cases set deleted = 1 where cases_id = %s" % (caseId)
    Logging().info("updatecase:" + updateDeleteSql)
    res = basicLib().updateSql(updateDeleteSql)

    for index in range(len(step)):
        stepOne = step[index]
        browserSession = stepOne["browserSession"]
        selectElement = stepOne["selectElement"].strip()
        elementMethods = stepOne["elementMethods"].strip()
        elementId = stepOne["elementId"].strip()
        deleted = stepOne["deleted"].strip()        
        keyName = stepOne["keyName"].strip()
        executionStep = (webCase().searchKeyData(keyName))["key_step"].strip()
        stepValue = stepOne["stepValue"].strip()
        element = stepOne["element"].strip()
        typeNum = (webCase().searchKeyData(keyName))["key_type"].strip()
        sort = stepOne["sort"]
        stepName = stepOne["stepName"].strip()
        sql = "INSERT INTO ui_auto_cases(cases_name,type,project_id,module_id,cases_id,execution_step,step_value,element,created_time,updated_time,ast_operator,sort,deleted,step_name,key_name,element_Id,browser_session,select_element,element_methods) VALUES(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" % (casesName,typeNum,projectId,moduleId,caseId,executionStep,stepValue,element,dt,dt,operator,sort,deleted,stepName,keyName,elementId,browserSession,selectElement,elementMethods)
        Logging().info(sql)
        res = basicLib().updateSql(sql)
        if res == "connecterror":
            res = {"code":"4003","msg":"data error"}
            return (json.dumps(res)) 

    updateAssertSql = "update ui_assertion set updated_time = \'%s\'  where cases_id = \'%s\'" %(dt,caseId)
    Logging().info("updatecase:"+ updateAssertSql)    
    res = basicLib().updateSql(updateAssertSql)
    if res == "connecterror":
        res = {"code":"4003","msg":"data error"}
        return (json.dumps(res))       
    res = {"code":0,"message":"success"}
    return (json.dumps(res).encode('utf-8').decode('unicode_escape'))

@app.route('/ui/executecase',methods = ['POST'])
@user
def executeCase():
    Logging().info("/ui/executecase/")
    Logging().info(request.json)     
    caseId = request.json["caseId"]
    if caseId == "" :
        res = {"code":"4103","msg":"parameter error"}
        return (json.dumps(res))  
    data = webCase().getDataByCaseId(caseId)

    for index in range(len(data)):
        stepData = data[index]
        stepValue = stepData["step_value"]
        executionStep = stepData["execution_step"]
        typeData = stepData["type"]
        element = stepData["element"]
        id = stepData["id"]
        try:
            res = webCase().executionOneCase(typeData,executionStep,stepValue,id,element)
            if res == 'fail':
                sql = "update ui_assertion set result = 1 where cases_id = %s "% (caseId)
                Logging().info(sql)       
                basicLib().updateSql(sql)
                res = {"code":0,"message":"success","result":"1"}
                webCase().close
                return (json.dumps(res).encode('utf-8').decode('unicode_escape'))  

        except Exception  as e: 
            sql = "update assertion set result = 1 where cases_id = %s "% (caseId)
            Logging().info(sql)   
            basicLib().updateSql(sql)
            Logging().debug('Error : {}'.format(e))
            res = {"code":0,"message":"success","result":"1"}
            webCase().close
            return (json.dumps(res).encode('utf-8').decode('unicode_escape'))         
        index = index +1

    sql = "update ui_assertion set result = 0 where cases_id = %s "% (caseId)
    Logging().info(sql)
    basicLib().updateSql(sql)
    res = {"code":0,"message":"success","result":"0"}
    webCase().close
    return (json.dumps(res).encode('utf-8').decode('unicode_escape')) 

@app.route('/ui/getecase/all',methods = ['GET'])
@user
def getCases():
    Logging().info("/ui/executecase/")
    Logging().info(request.args)      
    # data = request.get_data(as_text=True)
    caseName = request.args.get('caseName')
    caseId = request.args.get('caseId')
    projectId = request.args.get('projectId')
    pageSize = request.args.get('pageSize')
    curPage = request.args.get('curPage')
    res =  json.loads(webCase().searchAll(caseName,caseId,projectId, pageSize, curPage))
    return {"code":0,"message":"success","data":res}

@app.route('/ui/getecasedetail',methods = ['GET'])
@user
def getCasesDetail():
    Logging().info("/ui/getecasedetail/")
    Logging().info(request.args)       
    data = request.get_data(as_text = True)
    caseId = request.args.get('caseId')
    sql = "select element_methods as elementMethods,select_element as selectElement,type,execution_step as executionStep,step_name as stepName,key_name as keyName,browser_session as browserSession,step_value as stepValue,element,created_time as createdTime,updated_time as updatedTime,sort,deleted from ui_auto_cases where cases_id = %s and deleted <> 1" % (caseId)
    Logging().info(sql)
    step = basicLib().getAllJsonData(sql)
    step= json.loads(step)
    if step =="[]":
        res = {"code":0,"message":"success","data":""}
        return (res)

    sql2 = "select A.cases_name as casesName,A.project_id as projectId,B.created_time as createdTime,A.module_id as moduleId,A.cases_id as casesId,A.ast_operator as operator,B.result from ui_auto_cases A,ui_assertion B where A.cases_id = B.cases_id and A.cases_id = %s and A.sort = 1 order by A.cases_id ASC"% (caseId)
    Logging().info(sql2)
    resData = basicLib().getAllData(sql2)
    if resData == ():
        return {"code":0,"message":"success","data":''}
    data = resData[0] 

    for index in range(len(step)):       
        stepData = step[index]
        data.setdefault("step",[]).append(stepData)
        index = index +1
    data = webCase().searchCaseDetail(data)    
    res = {"code":0,"message":"success","data":data}
    return (res)

@app.route('/ui/deletecase',methods = ['POST'])
@user
def deletedCases():
    Logging().info("/ui/deletecase/")
    Logging().info(request.json)    
    operator = request.json["operator"]
    projectId = request.json["projectId"]
    caseId = request.json["caseId"]
    dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if operator  == "" or projectId == "" or caseId == "":
        res = {"code":"4003","msg":"data error"}
        return (json.dumps(res)) 

    sql = "update ui_auto_cases set deleted = '1',updated_time = \'%s\',ast_operator = \'%s\' where cases_id = %s" %(dt,operator,caseId)
    Logging().info(sql)
    res = basicLib().updateSql(sql)
    if res == "connecterror":
        res = {"code":"4003","msg":"data error"}
        return (json.dumps(res))       
    res = {"code":0,"message":"success"}
    return (json.dumps(res).encode('utf-8').decode('unicode_escape'))

#testTask
@app.route('/ui/createcasestask',methods = ['POST'])
@user
def createCasesTask():
    Logging().info("/ui/createcasestask/")
    Logging().info(request.json)      
    executeCaseId = json.dumps(request.json['executeCaseId'])
    dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    projectId = request.json["projectId"]
    operator = request.json["operator"]
    taskName = request.json["taskName"]
    common = request.json["common"]
    sql = "INSERT INTO ui_execute_task_cases(project_id,all_cases_id,created_time,updated_time,ast_operator,task_name,common,deleted) values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\','0')" % (projectId,executeCaseId,dt,dt,operator,taskName,common)
    Logging().info(sql)
    res = basicLib().updateSql(sql)
    if res == "connecterror":
        res = {"code":"4003","msg":"data error"}
        return (json.dumps(res))

    sql = "select id from ui_execute_task_cases where created_time = \'%s\'" % dt
    Logging().info(sql)
    resData = basicLib().getAllData(sql)
    id = resData[0]["id"]   
    res = {"code":0,"message":"success","taskId":id}
    return (json.dumps(res).encode('utf-8').decode('unicode_escape'))    
    
@app.route('/ui/executetask',methods = ['POST'])
@user
def executeTask():
    Logging().info("/ui/executetask/")
    Logging().info(request.json)       
    taskId = request.json["taskId"]
    operatorId = request.json["operatorId"]    
    webCase().executeTaskTest(taskId,operatorId)
    return ({"code":0,"message":"success"})

@app.route('/ui/gettaskdetail',methods = ['GET'])
@user
def getTaskDetail():
    Logging().info("/ui/gettaskdetail/")
    Logging().info(request.args)     
    # data = request.get_data(as_text=True)
    taskId = request.args.get('taskId')
    try:
        res =  webCase().searchTaskDetail(taskId)
    except Exception  as e:
        return{"code":500,"message":"数据库错误，请联系管理员"}
    return {"code":0,"message":"success","data":res}

@app.route('/ui/findtaskall',methods = ['GET'])
@user
def findTaskAll():
    Logging().info("/ui/findtaskall/")
    Logging().info(request.args)    
    # data = request.get_data(as_text=True)
    pageSize = request.args.get('pageSize')
    curPage = request.args.get('curPage')
    taskName = request.args.get('taskName')
    taskId = request.args.get('taskId')
    projectId = request.args.get('projectId')
    res =  webCase().searchTaskAll(taskName,taskId ,projectId, pageSize, curPage)
    res = json.loads(res)
    return {"code":0,"message":"success","data":res}

@app.route('/ui/deletetask',methods = ['POST'])
@user
def deleteTaskById():
    Logging().info("/ui/deletetask/")
    Logging().info(request.json)       
    taskId = request.json["taskId"]    
    sql = "update ui_execute_task_cases set deleted = 1 where id = \'%s\'" % taskId
    basicLib().updateSql(sql)
    return {"code":0,"message":"success"}

@app.route('/ui/updatetask',methods = ['POST'])
@user
def updateTaskById():
    Logging().info("/ui/updatetask/")
    Logging().info(request.json)   
    taskId = request.json["taskId"]
    taskName = request.json["taskName"]
    executeCaseId = json.dumps(request.json['executeCaseId'])
    operator = request.json["operator"]
    common = request.json["common"]
    dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "update ui_execute_task_cases set task_name = \'%s\',ast_operator = \'%s\',common = \'%s\',all_cases_id =\'%s\',updated_time =\'%s\' where id = \'%s\'" % (taskName,operator,common,executeCaseId,dt,taskId)
    basicLib().updateSql(sql)
    return {"code":0,"message":"success"}

#keyWork
def allowedFile(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1] in allowExtensions

@app.route('/ui/createkeyword',methods = ['GET','POST'])
@user
def createKeyWord():
    Logging().info("/ui/createkeyword/")
    if platform.system() == "Windows":
        slash = '\\'
    else:
        platform.system() == "Linux"
        slash = '/'
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if request.method == 'POST':   # 如果是 POST 请求方式  
        file = request.files.get('file')
        data = request.get_data(as_text=True)
        data =  dict(request.args)
        operator = data["operator"][0]
        keyCnName = data['keyCnName'][0]
        keyName = data['keyName'][0]
        type = data['type'][0]

        if file:
            if file and allowedFile(file.filename):
                # secure_filename方法会去掉文件名中的中文
                filename = secure_filename(file.filename)
                #因为上次的文件可能有重名，因此使用uuid保存文件
                file.save(os.path.join(app.config['uploadFolder'],filename))
                basePath = os.getcwd()
                filePath = basePath + slash + app.config['uploadFolder'] + slash + filename
                keyValue = slash + 'keyword' + slash + filename
                sql = 'select key_name from ui_exec_step where key_name = \'%s\'' % keyName
                res = basicLib().getAllData(sql)    
                if res != ():
                    return ({"code":0,"message":"keyword existed"})
                else:
                    sql = 'INSERT INTO ui_exec_step(key_cn_name,key_name,key_type,key_step,created_time,updated_time,operator,deleted)values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',0)' % (keyCnName,keyName,type,keyValue,dt,dt,operator)
                    basicLib().updateSql(sql)
                return redirect(url_for('createKeyWord',filename = filename))
            # 表示没有发送文件
        else:
            return "未上传文件"
    return ({"code":0,"message":"success"})

@app.route('/ui/getekey/all',methods = ['GET'])
@user
def getKey():
    Logging().info("/ui/getekey/all")
    Logging().info(request.args)       
    Logging().info("/ui/getekey/all/")
    # data = request.get_data(as_text=True)
    res = webCase().searchKeyAll()
    res = json.loads(res)
    return {"code":0,"message":"success","data":res}

@app.route('/ui/getekeyword/all',methods = ['GET'])
@user
def getKeyWord():
    Logging().info("/ui/getekeyword/all")
    Logging().info(request.args)       
    # data = request.get_data(as_text=True)
    pageSize = request.args.get('pageSize')
    curPage = request.args.get('curPage')
    keyName = request.args.get('keyName')
    res = webCase().searchKeyWordAll(pageSize,curPage,keyName)    
    res = json.loads(res)
    return {"code":0,"message":"success","data":res}

@app.route('/ui/deletekey',methods = ['POST'])
@user
def deleteKey():
    Logging().info("/ui/getekey/all")
    Logging().info(request.json)       
    id = request.json["id"]
    keyType = request.json["keyType"]
    keyStep =  request.json["keyStep"]
    operator = request.json["operator"]       
    if keyType < '3':
        return ({"code":0,"message":"此关键字不支持删除"})
    sql = "update ui_exec_step set deleted = 1,operator =\'%s\' where id = \'%s\' and key_type = \'%s\'" %(operator,id,keyType) 
    basicLib().updateSql(sql)
    # dir = os.getcwd()    
    keyFile = "mv "+os.getcwd() + keyStep + " "+os.getcwd()+keyStep+".bak"
    Logging().info(keyFile)       
    os.popen(keyFile)    
    return ({"code":0,"message":"success"})

#report
@app.route('/ui/getreportbyid', methods = ['GET'])
@user
def getReport():
    Logging().info("/ui/getreportbyid/")
    Logging().info(request.args)     
    # data = request.get_data(as_text=True)
    taskId = request.args.get('taskId')
    res = webCase().searchReportDetail(taskId)
    res = {"code": 0, "message": "success", "data": res}
    return res

@app.route('/ui/getreport/all', methods = ['GET'])
@user
def getReportAll():
    Logging().info("/ui/getreport/all/")
    Logging().info(request.args)     
    pageSize = request.args.get('pageSize')
    curPage = request.args.get('curPage')
    operatorId = request.args.get('operatorId')
    res = webCase().searchReportAll(pageSize,curPage,operatorId)
    res = json.loads(res)
    return {"code": 0, "message": "success", "data": res}

@app.route('/ui/getreportdetail', methods = ['GET'])
@user
def getReportDetail():
    Logging().info("/ui/getreportdetail/")
    Logging().info(request.args)     
    data = request.get_data(as_text=True)
    reportId = request.args.get('reportId')
    res = webCase().searchReportCasesDetail(reportId)    
    res = json.loads(res)
    return {"code": 0, "message": "success", "data": res}

@app.route('/ui/deletereportbyid', methods = ['POST'])
@user
def deleteReportById():
    Logging().info("/ui/deletereportbyid/")
    Logging().info(request.json)      
    reportId = request.json["reportId"]
    operatorId = request.json["operatorId"]
    sql = "update ui_report_task set deleted = 1,ast_operator=\'%s\' where id = \'%s\'" % (operatorId,reportId)
    basicLib().updateSql(sql)
    return {"code": 0, "message": "success"}

#页面元素部分接口
@app.route('/ui/recognitionelements', methods = ['POST'])
@user
def recognitionElements():
    url = request.json['pageurl']
    if url == '':
        return { "code": 0, "message": "fail", 'data': "pageurl不能为空" }
    f = recognitionElement(request.json['pageurl'])
    elements = f.recognition(request.json['elements'])
    res = { "code": 0, "message": "success", "data": elements }
    return res

@app.route('/ui/createpage', methods = ['POST'])
@user
def createPage():
    operator = request.json['operator']
    projectid = request.json['projectid']
    pagename = request.json['pagename']
    pageurl = request.json['pageurl']
    pagenodes = request.json['pagenotes']
    res1 = pageSql().addPage(pagename, pageurl, pagenodes, operator, projectid)
    insertid = str(res1['lastid'])
    res = { "code": 0, "message": "success", "data": { "pageid": insertid } }
    return res

@app.route('/ui/getallpage', methods = ['GET'])
@user
def getAllPage():
    projectid = request.args.get('projectid')
    pagename = request.args.get('pagename')
    pageSize = request.args.get('pageSize')
    curPage = request.args.get('curPage')
    res =  pageSql().searchAll(pagename=pagename, projectid=projectid, pageSize=pageSize, curPage=curPage)
    res["code"] = 0
    res["message"] = "success"
    return res

@app.route('/ui/deletepage', methods = ['DELETE'])
@user
def deletePage():
    id = int(request.json['id'])
    res = pageSql().deleteData(id)
    data = { "code": 0, "message": res }
    return data

@app.route('/ui/getpagedetail', methods = ['GET'])
@user
def getPageDetail():
    id = request.args.get('id')
    res = pageSql().searchOne(id)
    data = { "code": 0, "message": "success", "data": res }
    return data

@app.route('/ui/addmultipleelement', methods = ['POST'])
@user
def addMultipleElement():
    pageid = request.json['pageid']
    elements = request.json['elements']
    keywords = ''
    for i in range(len(elements)):
        content = str((elements[i]['attr'], elements[i]['type'], elements[i]['name'], elements[i]['depict'], pageid))
        if i < len(elements) - 1:
            keywords += content + ','
        else:
            keywords += content

    res1 = pageSql().addElement(keywords)
    res = { "code": 0, "message": "success", "data": res1['lastid'] }
    return res

@app.route('/ui/addelement', methods = ['POST'])
@user
def addElement():
    attr = request.json['attr']
    methods = request.json['methods']
    name = request.json['name']
    depict = request.json['depict']
    pageid = request.json['pageid']
    datas = str((attr, methods, name, depict, pageid))
    res = pageSql().addElement(datas)
    data = {"code": 0, "message": res }
    return data

@app.route('/ui/omitelement', methods = ['DELETE'])
@user
def omitElement():
    id = request.json['id']
    res = pageSql().deleteElement(id)
    data = {"code": 0, "message": res }
    return data

@app.route('/ui/getelements', methods = ['GET'])
@user
def getElements():
    pageid = request.args.get('pageid')
    res = pageSql().getElements(pageid)
    data = { "code": 0, "message": "success", 'data': res }
    return data

@app.route('/ui/mendelement', methods = ['put'])
@user
def mendElement():
    elementid = request.json['elementid']
    attr = request.json['attr']
    methods = request.json['methods']
    name = request.json['name']
    depict = request.json['depict']
    res = pageSql().mendElement(elementid, name, attr, methods, depict)
    data = { "code": 0, "message": res }
    return data

if __name__ == '__main__':
    app.run( debug = True,port = 5198)