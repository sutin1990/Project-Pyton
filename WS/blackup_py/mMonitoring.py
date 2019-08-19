from flask import Flask, render_template, request, Response, send_file,json
from flask_cors import CORS

import time

import data_access_layer as db
import sqlalchemy as sql
import urllib

import os 
import win32serviceutil

# connect to database
conString = "DRIVER={SQL Server Native Client 11.0};SERVER=SAPB1_01;DATABASE=MFC_AIS;UID=sa;PWD=P@ssw0rd"
engine = sql.create_engine("mssql+pyodbc:///?odbc_connect=%s" % urllib.parse.quote_plus(conString))

app = Flask(__name__)
CORS(app)

def RestartWindowsService():
    serviceName = "POS_SAPB1_Schedule"
    win32serviceutil.RestartService(serviceName)

@app.route('/')
def home():
    return render_template('monitoring.html') 

@app.route('/monitoring')
def home_monitoring():
    return render_template('monitoring.html') 

@app.route('/transaction')
def home_transaction():
    return render_template('transaction.html') 


@app.route('/progress')
def progress():
    def generate():
        x = 0
        while x < 100:
            print (x)
            x = x + 10
            time.sleep(0.2)
            yield "data:" + str(x) + "\n\n"    
    return Response(generate(), mimetype= 'text/event-stream')


@app.route('/invoice')
def invoice():
    def generate():
        # x = 0
        # while x < 100:
        #     print (x)
        #     x = x + 10
        #     time.sleep(0.2)
        #     yield "data:" + str(x) + "\n\n"    
        log_msg = "Idle"
        while 1==1:
            log_msg = "Idle"
            s_sql = "select * from AIS_Monitoring where AMT_Setting = 'Invoice'"
            # print(s_sql)
            msg, data_rows, errFlag = db.exec_query(engine, s_sql)
            if data_rows is not None:
                rows = data_rows.to_json(orient='records')
                json_rows = json.loads(rows)

                for r in json_rows:
                    log_msg = r["AMT_LogMsg"] 
            
            yield "data:" + log_msg + "\n\n" 

    return Response(generate(), mimetype= 'text/event-stream')

@app.route('/payment')
def payment():
    def generate():
        # x = 0
        # while x < 100:
        #     print (x)
        #     x = x + 10
        #     time.sleep(0.2)
        #     yield "data:" + str(x) + "\n\n"
        log_msg = "Idle"
        while 1==1:
            log_msg = "Idle"
            s_sql = "select * from AIS_Monitoring where AMT_Setting = 'Payment'"
            # print(s_sql)
            msg, data_rows, errFlag = db.exec_query(engine, s_sql)
            if data_rows is not None:
                rows = data_rows.to_json(orient='records')
                json_rows = json.loads(rows)

                for r in json_rows:
                    log_msg = r["AMT_LogMsg"] 
            
            yield "data:" + log_msg + "\n\n"     
    return Response(generate(), mimetype= 'text/event-stream')

@app.route('/movement')
def movement():
    def generate():
        # x = 0
        # while x < 100:
        #     print (x)
        #     x = x + 10
        #     time.sleep(0.2)
        #     yield "data:" + str(x) + "\n\n"
        log_msg = "Idle"
        while 1==1:
            log_msg = "Idle"
            s_sql = "select * from AIS_Monitoring where AMT_Setting = 'Movement'"
            # print(s_sql)
            msg, data_rows, errFlag = db.exec_query(engine, s_sql)
            if data_rows is not None:
                rows = data_rows.to_json(orient='records')
                json_rows = json.loads(rows)

                for r in json_rows:
                    log_msg = r["AMT_LogMsg"] 
            
            yield "data:" + log_msg + "\n\n"  
    return Response(generate(), mimetype= 'text/event-stream')

@app.route('/cndn')
def cndn():
    def generate():
        # x = 0
        # while x < 100:
        #     print (x)
        #     x = x + 10
        #     time.sleep(0.2)
        #     yield "data:" + str(x) + "\n\n"
        log_msg = "Idle"
        while 1==1:
            log_msg = "Idle"
            s_sql = "select * from AIS_Monitoring where AMT_Setting = 'CNDN'"
            # print(s_sql)
            msg, data_rows, errFlag = db.exec_query(engine, s_sql)
            if data_rows is not None:
                rows = data_rows.to_json(orient='records')
                json_rows = json.loads(rows)

                for r in json_rows:
                    log_msg = r["AMT_LogMsg"] 
            
            yield "data:" + log_msg + "\n\n"    
    return Response(generate(), mimetype= 'text/event-stream')

@app.route('/masterdata')
def masterdata():
    def generate():
        # x = 0
        # while x < 100:
        #     print (x)
        #     x = x + 10
        #     time.sleep(0.2)
        #     yield "data:" + str(x) + "\n\n" 
        log_msg = "Idle"
        while 1==1:
            log_msg = "Idle"
            s_sql = "select * from AIS_Monitoring where AMT_Setting = 'MasterData'"
            # print(s_sql)
            msg, data_rows, errFlag = db.exec_query(engine, s_sql)
            if data_rows is not None:
                rows = data_rows.to_json(orient='records')
                json_rows = json.loads(rows)

                for r in json_rows:
                    log_msg = r["AMT_LogMsg"] 

            # print (log_msg)
            yield "data:" + log_msg + "\n\n"    
    return Response(generate(), mimetype= 'text/event-stream')


@app.route('/SettingLoad', methods=['GET', 'POST'])
def SettingLoad():
    s_title=''
    _data = []
    if request.method == 'POST':
        data = request.json
        s_title = data["title"]
        res = {"title" : s_title}

        _data.append(res)

        s_sql = "select * from AIS_Setting where AST_Setting = N'"+ s_title +"'"
        # print(s_sql)
        msg, data_rows, errFlag = db.exec_query(engine, s_sql)
        if data_rows is not None:
            rows = data_rows.to_json(orient='records')
            json_rows = json.loads(rows)
    
            for r in json_rows:
                _data.append({"Setting": r["AST_Setting"] })
                _data.append({"ScheduleType": r["AST_ScheduleType"] })
                _data.append({"ScheduleTime": r["AST_ScheduleTime"] })
                _data.append({"ScheduleTimeType": r["AST_ScheduleTimeType"] })

    # print(_data)
    json_string = json.dumps(_data,ensure_ascii = False)
    print(json_string)
    #creating a Response object to set the content type and the encoding
    response = Response(json_string,content_type="application/json; charset=utf-8" )
    return response

@app.route('/SettingSave', methods=['POST'])
def SettingSave():
    if request.method == 'POST':
        data = request.json
        s_sql = "sp_AIS_SettingInsUpd"
        parm=[]
        parm.append({"name": '@Setting',"value": data["title"]})
        parm.append({"name": '@ScheduleType',"value": data["ScheduleType"]})
        parm.append({"name": '@ScheduleTime',"value": str(data["ScheduleTime"])})
        parm.append({"name": '@ScheduleTimeType',"value": data["ScheduleTimeType"]})
 
        msg,  errFlag = db.exec_post_procedure(engine, s_sql,parm)
        if errFlag==False:
            RestartWindowsService()
            
    return msg    

@app.route('/transactionview', methods=['GET', 'POST'])
def TransactionView():
    s_sp = "sp_AIS_TransactionViewLoad"
    params = {
        'transaction': None,
        'FromDate': None,
        'ToDate': None
    }    
    # print(s_sql)
    msg, data_rows, errFlag = db.exec_procedure(engine, s_sp,params)
    # if data_rows is not None:
    #     rows = data_rows.to_json(orient='records')
    #     json_rows = json.loads(rows)

    return data_rows.to_json(orient='records')

if __name__ == "__main__":
    app.debug = True
    # app.run(threaded=True)
    app.run(threaded=True, host = '0.0.0.0', port = 8081)
    
    
