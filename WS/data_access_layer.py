#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import sqlalchemy as sql
import pyodbc
from io import BytesIO, StringIO

def exec_scalar(engine, sql_string):
    try:
        connection = engine.connect()
        result = connection.execute(sql_string)
        rows = result.fetchone()
        connection.close()
        return rows[0], False

    except pyodbc.Error as ex:
        return ex.message, True
    except (sql.exc.SQLAlchemyError, sql.exc.DBAPIError) as ex:
        return ex.message, True
    except Exception as ex:
        return ex, True

def exec_query(engine, sql_string):
    try:
        connection = engine.connect()
        df = pd.read_sql(sql_string, engine)
        connection.close()
        return "", df, False

    except pyodbc.Error as ex:
        return ex.message, None, True
    except (sql.exc.SQLAlchemyError, sql.exc.DBAPIError) as ex:
        return ex.message, None, True
    except Exception as ex:
        return ex, None, True

def exec_procedure(engine, proc_name, params=None):
    # params = {
    #     'Foo': foo_value,
    #     'Bar': bar_value
    # }
    try:
        if(params != None):
            sql_params = ",".join(["@" + name + ("=NULL" if value == None else "=N'" + value.replace("'","''") + "'") for name, value in params.items()])
            sql_string = "exec " + proc_name + " " + sql_params + ";"
        else:
            sql_string = "exec " + proc_name + ";"

        print(sql_string)
        # connection = engine.connect()

        connection = engine.connect()
        # result = connection.execute()
        df = pd.read_sql(sql_string, connection)
        connection.execute(sql_string).fetchall()

        connection.close()

        # connection.close()
        return "", df, False


    except pyodbc.Error as ex:
        return ex.message, None, True
    except (sql.exc.SQLAlchemyError, sql.exc.DBAPIError) as ex:
        return ex.message, None, True
    except Exception as ex:
        return ex, None, True


def exec_post_query(engine, sql_string):
    try:
        connection = engine.connect()
        # transaction = connection.begin()
        connection.execute(sql_string)
        # transaction.commit()
        connection.close()
        return "", False

    except pyodbc.Error as ex:
        # transaction.rollback()
        return ex.message, True
    except (sql.exc.SQLAlchemyError, sql.exc.DBAPIError) as ex:
        # transaction.rollback()
        return ex.message, True
    except Exception as ex:
        # transaction.rollback()
        return ex, True


def exec_post_procedure(engine, proc_name, params=None):
    try:
        # if (params != None):

        #     # sql_params = ",".join(["@" + name + ("=NULL" if value == None else "=N'" + value.replace("'","''") + "'") for name, value in params.items()])
        #     for name, value in params.items():
        #         print (name,value)
        #     # sql_string = "exec " + proc_name + " " + sql_params + ";"
        # else:
        #     sql_string = "exec " + proc_name + ";"

        # print(sql_string)    
        # connection = engine.connect()
        # # transaction = connection.begin()
        # connection.execute(sql_string)
        # # transaction.commit()
        # connection.close()
        sql_params = ""
        if (params != None):
            for p in params:
                if sql_params=="":
                    sql_params = p["name"] + " = N'" + p["value"] + "'"
                else:
                    sql_params = sql_params +", "+p["name"] + " = '" + p["value"] + "'"
            
            sql_string = "exec " + proc_name + " " + sql_params + ";"
        else:
            sql_string = "exec " + proc_name + ";"


        print(sql_string)
        
        connection = engine.connect()
        transaction = connection.begin()
        connection.execute(sql_string)
        transaction.commit()
        connection.close()

        return "", False

    except pyodbc.Error as ex:
        transaction.rollback()
        return ex, True
    except (sql.exc.SQLAlchemyError, sql.exc.DBAPIError) as ex:
        transaction.rollback()
        return ex, True
    except Exception as ex:
        transaction.rollback()
        return ex, True


def to_xml(df, filename=None, mode='w'):
    def row_to_xml(row):
        xml = ['  <row>']
        for i, col_name in enumerate(row.index):
            xml.append('    <{0}>{1}</{0}>'.format(col_name, row.iloc[i]))
        xml.append('  </row>')
        return '\n'.join(xml)
    res = '\n'.join(df.apply(row_to_xml, axis=1))

    xml = '<?xml version="1.0" encoding="utf-8"?>'
    xml = xml + '\n' + '<table>'
    xml = xml + '\n' + res
    xml = xml + '\n' + '</table>'

    buffer = StringIO.StringIO()
    buffer.write(xml)
    buffer.seek(0)
    return buffer

def to_csv(df):
    # df.to_csv('data.csv', index=False)
    buffer = StringIO.StringIO()
    df.to_csv(buffer, encoding='utf-8', index=False)
    buffer.seek(0)
    return buffer

def to_excel(df):
    buffer = BytesIO()
    writer = pd.ExcelWriter(buffer, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    buffer.seek(0)
    return buffer

def to_json(df):
    buffer = StringIO.StringIO()
    df.to_json(buffer, orient='records')
    buffer.seek(0)
    return buffer

def sql_string(sqlstring):
    return str.replace(sqlstring, "'", "")