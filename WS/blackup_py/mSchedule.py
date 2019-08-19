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

# connect to database
conString = "DRIVER={SQL Server Native Client 11.0};SERVER=SAPB1_01;DATABASE=MFC_AIS;UID=sa;PWD=P@ssw0rd"
engine = sql.create_engine("mssql+pyodbc:///?odbc_connect=%s" % urllib.parse.quote_plus(conString))




def LoadMasterData():
    # m_sp_LoadItemMaster_export
    msg,  errFlag = db.exec_post_procedure(engine, "m_sp_LoadItemMaster_export",None)

def LoadInv():
    #pass
	os.system('"E:\setupinterface\WS\libs\SAPB1Interface.exe"')

def LoadPayment():
   os.system('"E:\setupinterface\WS\libs\SAPB1Interface.exe"')

def LoadMovement():    
	s_sql = "select * from AIS_Monitoring where AMT_Setting = 'Movement' and AMT_LogMsg = 'Idle'"
	msg,data_rows, errFlag = db.exec_query(engine, s_sql)
	if data_rows is not None:
		# print(data_rows)
		os.system('"D:\Fanslink\System\WS\libs\SAPB1Interface.exe"')

def LoadCNDN():
    #pass
	os.system('"E:\setupinterface\WS\libs\SAPB1Interface.exe"')

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
                print("Every "+str(n_ScheduleTime) + " "+ s_ScheduleTimeType)
                if s_ScheduleTimeType == "Second":
                    schedule.every(n_ScheduleTime).seconds.do(LoadMasterData)
                if s_ScheduleTimeType == "Minute":
                    schedule.every(n_ScheduleTime).minutes.do(LoadMasterData)
                if s_ScheduleTimeType == "Hour":
                    schedule.every(n_ScheduleTime).hours.do(LoadMasterData)
            if s_ScheduleType==2:
                schedule.every().day.at(s_DailyTime).do(LoadMasterData)

        # Payment 
        if s_Setting == "Payment":
            if s_ScheduleType==1:
                if s_ScheduleTimeType == "Second":
                    schedule.every(n_ScheduleTime).seconds.do(LoadPayment)
                if s_ScheduleTimeType == "Minute":
                    schedule.every(n_ScheduleTime).minutes.do(LoadPayment)
                if s_ScheduleTimeType == "Hour":
                    schedule.every(n_ScheduleTime).hours.do(LoadPayment)
            if s_ScheduleType==2:
                schedule.every().day.at(s_DailyTime).do(LoadPayment)

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

        # CNDN 
        if s_Setting == "CNDN":
            if s_ScheduleType==1:
                if s_ScheduleTimeType == "Second":
                    schedule.every(n_ScheduleTime).seconds.do(LoadMovement)
                if s_ScheduleTimeType == "Minute":
                    schedule.every(n_ScheduleTime).minutes.do(LoadMovement)
                if s_ScheduleTimeType == "Hour":
                    schedule.every(n_ScheduleTime).hours.do(LoadMovement)
            if s_ScheduleType==2:
                schedule.every().day.at(s_DailyTime).do(LoadMovement)


while 1:
    schedule.run_pending()
    time.sleep(1)    