# from ctypes import*
# # give location of dll
# b1 = cdll.LoadLibrary("D:\Projects\Fanslink\DataInterface\src\libs\mSAP01.dll")
# b1.LoadForm1()
import data_access_layer as db
import sqlalchemy as sql
import urllib

import schedule
import time

import sys, string, os

import json
import subprocess

from datetime import datetime
# connect to database
conString = "DRIVER={SQL Server Native Client 11.0};SERVER=SAPB1_01;DATABASE=MFC_AIS;UID=sa;PWD=P@ssw0rd"
engine = sql.create_engine("mssql+pyodbc:///?odbc_connect=%s" % urllib.parse.quote_plus(conString))




def LoadMasterData():
    # m_sp_LoadItemMaster_export
    currentdate = datetime.today().strftime('%Y-%m-%d')
    parm = []
    parm.append({"name": '@FromDate',"value":currentdate})
    msg,  errFlag = db.exec_post_procedure(engine, "m_sp_LoadItemMaster_export",parm)

def LoadMovementExport():
    # m_sp_LoadInvtTRPOS_export
    currentdate = datetime.today().strftime('%Y-%m-%d')
    parm = []
    parm.append({"name": '@FromDate',"value":currentdate})
    msg,  errFlag = db.exec_post_procedure(engine, "m_sp_LoadInvtTRPOS_export",parm)

# def LoadInv():
#     s_sql = "select * from AIS_Monitoring where AMT_Setting = 'Invoice/Payment' and AMT_LogMsg = 'Idle'"
#     msg,data_rows, errFlag = db.exec_query(engine, s_sql)
#     if data_rows is not None:
#         subprocess.call(["E:\setupinterface\WS\libs\SAPB1Interface.exe",'Invoice/Payment'])
# # 	os.system('"E:\setupinterface\WS\libs\SAPB1Interface.exe"')

def LoadInvPayment():
    #os.system('"E:\setupinterface\WS\libs\SAPB1Interface.exe"')
    s_sql = "select * from AIS_Monitoring where AMT_Setting = 'Invoice/Payment' and AMT_LogMsg = 'Idle'"
    msg,data_rows, errFlag = db.exec_query(engine, s_sql)
    if data_rows is not None:
        subprocess.call(["E:\setupinterface\WS\libs\SAPB1Interface.exe",'Invoice/Payment'])

def LoadMovement():
    s_sql = "select * from AIS_Monitoring where AMT_Setting = 'Movement' and AMT_LogMsg = 'Idle'"
    msg,data_rows, errFlag = db.exec_query(engine, s_sql)
    if data_rows is not None:
        subprocess.call(["E:\setupinterface\WS\libs\SAPB1Interface.exe",'Movement'])

def LoadMovementRequest():    
	s_sql = "select * from AIS_Monitoring where AMT_Setting = 'MovementRequest' and AMT_LogMsg = 'Idle'"
	msg,data_rows, errFlag = db.exec_query(engine, s_sql)
	if data_rows is not None:
		# print(data_rows)
		subprocess.call(["E:\setupinterface\WS\libs\SAPB1Interface.exe",'MovementRequest'])

def LoadCNDN():
    s_sql = "select * from AIS_Monitoring where AMT_Setting = 'CN/DN' and AMT_LogMsg = 'Idle'"
    #print(s_sql)
    msg,data_rows, errFlag = db.exec_query(engine, s_sql)
    if data_rows is not None:
		# print(data_rows)
        subprocess.call(["E:\setupinterface\WS\libs\SAPB1Interface.exe",'CN/DN'])

# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("22:17").do(job)
# schedule.every(6).seconds.do(job)

s_sql = "select * from AIS_Setting"
# print(s_sql)
msg, data_rows, errFlag = db.exec_query(engine, s_sql)
if data_rows is not None:
    rows = data_rows.to_json(orient='records')
    json_rows = json.loads(rows)

    for r in json_rows:
        s_Setting = r["AST_Setting"] 
        s_ScheduleType = r["AST_ScheduleType"] 
        n_ScheduleTime = r["AST_ScheduleTime"] 
        s_ScheduleTimeType =  r["AST_ScheduleTimeType"]
        s_DailyTime = "08:30"

        print("setting "+s_Setting+" schedule")
        # MasterData 
        if s_Setting == "MasterData":
            if s_ScheduleType==1:
                #print("Every "+str(n_ScheduleTime) + " "+ s_ScheduleTimeType)
                if s_ScheduleTimeType == "Second":
                    schedule.every(n_ScheduleTime).seconds.do(LoadMasterData)
                if s_ScheduleTimeType == "Minute":
                    schedule.every(n_ScheduleTime).minutes.do(LoadMasterData)
                if s_ScheduleTimeType == "Hour":
                    schedule.every(n_ScheduleTime).hours.do(LoadMasterData)
            if s_ScheduleType==2:
                schedule.every().day.at(s_DailyTime).do(LoadMasterData)

        #Payment 
        if s_Setting == "Invoice/Payment":
            if s_ScheduleType==1:
                if s_ScheduleTimeType == "Second":
                    schedule.every(n_ScheduleTime).seconds.do(LoadInvPayment)
                if s_ScheduleTimeType == "Minute":
                    schedule.every(n_ScheduleTime).minutes.do(LoadInvPayment)
                if s_ScheduleTimeType == "Hour":
                    schedule.every(n_ScheduleTime).hours.do(LoadInvPayment)
            if s_ScheduleType==2:
                schedule.every().day.at(s_DailyTime).do(LoadInvPayment)

        # Movement 
        if s_Setting == "Movement":
            if s_ScheduleType==1:
                if s_ScheduleTimeType == "Second":
                    schedule.every(n_ScheduleTime).seconds.do(LoadMovement)
                if s_ScheduleTimeType == "Minute":
                    schedule.every(n_ScheduleTime).minutes.do(LoadMovement)
                if s_ScheduleTimeType == "Hour":
                    schedule.every(n_ScheduleTime).hours.do(LoadMovement)
            if s_ScheduleType==2:
                schedule.every().day.at(s_DailyTime).do(LoadMovement)
        # Movement Request
        if s_Setting == "MovementRequest":
            if s_ScheduleType==1:
                if s_ScheduleTimeType == "Second":
                    schedule.every(n_ScheduleTime).seconds.do(LoadMovementRequest)
                if s_ScheduleTimeType == "Minute":
                    schedule.every(n_ScheduleTime).minutes.do(LoadMovementRequest)
                if s_ScheduleTimeType == "Hour":
                    schedule.every(n_ScheduleTime).hours.do(LoadMovementRequest)
            if s_ScheduleType==2:
                schedule.every().day.at(s_DailyTime).do(LoadMovementRequest)
        #MovementVerify
        if s_Setting == "MovementVRF":
            if s_ScheduleType==1:
                if s_ScheduleTimeType == "Second":
                    schedule.every(n_ScheduleTime).seconds.do(LoadMovementExport)
                if s_ScheduleTimeType == "Minute":
                    schedule.every(n_ScheduleTime).minutes.do(LoadMovementExport)
                if s_ScheduleTimeType == "Hour":
                    schedule.every(n_ScheduleTime).hours.do(LoadMovementExport)
            if s_ScheduleType==2:
                schedule.every().day.at(s_DailyTime).do(LoadMovementExport)

        # CNDN 
        if s_Setting == "CN/DN":
            if s_ScheduleType==1:
                #print("Every "+str(n_ScheduleTime) + " "+ s_ScheduleTimeType)
                if s_ScheduleTimeType == "Second":
                    schedule.every(n_ScheduleTime).seconds.do(LoadCNDN)
                if s_ScheduleTimeType == "Minute":
                    schedule.every(n_ScheduleTime).minutes.do(LoadCNDN)
                if s_ScheduleTimeType == "Hour":
                    schedule.every(n_ScheduleTime).hours.do(LoadCNDN)
            if s_ScheduleType==2:
                schedule.every().day.at(s_DailyTime).do(LoadCNDN)


while 1:
    schedule.run_pending()
    time.sleep(1)    