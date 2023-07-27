from routers.utils.errorHandling import handleError
from routers.utils.statusCodes import FAILED, SUCCESS
from routers.utils.responseMessages import NOT_ADD, ADD_MSG, ALREADY_EXISTS, NOT_UPDATE, UPDATE_MSG, DELETE_MSG, NOT_DELETE, NOT_FOUND, FOUND, OTP
import json
import pyodbc
from typing import List,Dict,Tuple
from collections.abc import Callable
from pydantic import ValidationError
from aioodbc.cursor import Cursor
import inspect
from routers.eventServer import publish
from routers.sms import sendSMS
from routers.eventServer import publish
import inspect


async def ApiWithProcedureTransfun(db: Cursor, query: str, request: any,transformParam: Callable, additionalFunction: Callable) -> Dict:
    try:
        print(f"""{query}""")
        queryParams:Tuple = transformParam(request)
        print(queryParams)
        await db.execute(f"""{query}""", queryParams)
        res:List = await db.fetchall()
        return additionalFunction(res)
    except ValidationError as pe:
        # handle the validation error
        print(f"Validation error for field type {pe.field_type}: {pe.errors()}")
        
        def pydanticError(e) -> str:
            return f"Validation error for field type {pe.field_type}: {pe.errors()}"
        return handleError(pe, pydanticError)
    except Exception as e:
        def errorFunc(e):
            return e
        return handleError(e, errorFunc)

async def ApiWithProcedure(db, query, queryParams, additionalFunction):
    try:
        print('queryParams', queryParams)
        print(f"""{query}""", queryParams)
        await db.execute(f"""{query}""", queryParams)
        res = await db.fetchall()
        print(type(additionalFunction), "typeCheck", inspect.iscoroutinefunction(additionalFunction))
        if inspect.iscoroutinefunction(additionalFunction):
            print('came inside')
            return await additionalFunction(res)
        else:
            return additionalFunction(res)
    except pyodbc.Error as pe:
         print(str(pe))
         return {
              'response': 'DataBase error ',
              'statusCode': FAILED
         }
    except Exception as e:
        def errorFunc(e):
            return e
        return handleError(e, errorFunc)

async def ApiWithProcedureTrans(db, query, request,transformParam, additionalFunction):
    try:
        
        # queryParams = transformParam(request)
        queryParams:Tuple = transformParam(request)
        print('queryParams', queryParams)
        print(f"""{query}""", queryParams)
        await db.execute(f"""{query}""", queryParams)
        res = await db.fetchall()
        return additionalFunction(res)
    except Exception as e:
        def errorFunc(e):
            return e
        return handleError(e, errorFunc)

    
async def ApiWithProcedureGet(db, query, queryParams, additionalFunction=None, dataTransform=None):
    try:
        print('queryParams', queryParams)
        print(f"""{query}""", queryParams)
        await db.execute(f"""{query}""", queryParams)
        res = await db.fetchall()
        if additionalFunction: 
            return additionalFunction(res,dataTransform if dataTransform else getData)
        else:
             return additionalFunctionGet(res,dataTransform if dataTransform else getData)
    except Exception as e:
        def errorFunc(e):
            return e
        return handleError(e, errorFunc)

def getData(res):
    data = FOUND
    data['data'] = json.loads(res) 
    return data

def additionalFunctionGet(res, getData=None):
        print('res111', (res[0][0]))
        if len(res) == 0:
            return NOT_FOUND
        elif res[0][0] != None:
            return getData(res[0][0])
        else: 
            return NOT_FOUND
    
def additionalFunctionPost(res):
        # print(res,"resres")
        if len(res) == 0:
            return ALREADY_EXISTS
        elif res[0][1] == 0:
            return NOT_ADD
        elif res[0][1] == 2:
            return ALREADY_EXISTS
        else: 
            return ADD_MSG
        
def additionalFunctionPostUserMapp(res):
        # print(res,"resres")
        if len(res) == 0:
            return ALREADY_EXISTS
        elif res[0][1] == 0:
            return NOT_ADD
        elif res[0][1] == 2:
            return ALREADY_EXISTS
        elif res[0][1] == 1:
            return {
                        'statusCode': SUCCESS,
                        'response': 'Data Added Successfully',
                        'BookingId':res[0][2]
                    }
        else: 
            return ADD_MSG

def additionalFunctionPut(res):
        if len(res) == 0:
            return NOT_UPDATE
        elif res[0][1] == 0:
            return NOT_UPDATE
        elif res[0][1] == 2:
            return ALREADY_EXISTS
        else: 
            return UPDATE_MSG

def additionalFunctionDelete(res):
        if len(res) == 0:
            return NOT_DELETE
        elif res[0][1] == 0:
            return NOT_DELETE
        else: 
            return DELETE_MSG
        


async def ApiWithProcedurePaymentLink(db, query, queryParams, additionalFunction, Link,MobileNo):
    try:
        await db.execute(f"""{query}""", queryParams)
        res = await db.fetchall()
        print('lenssss',query,queryParams)
        if len(res)>0 and res[0][0]!=None:
            print(res[0][0],"testres")
           
    
            
            tempData = json.loads(res[0][0])
            print('tempData',tempData)
            await publish(queueName='payprenotificationService', message = {
                                    'action':'paymentLink',
                                    'body':{
                                        'tempData': tempData,
                                        'MobileNo': MobileNo,
                                        'Link':Link
                                    }
                                })
            return {
            'statusCode':1,
            'response': 'Payment Link Sent Successfully'
             }
        else:
            return{
            'statusCode':0,
            'response': 'Payment Link Sended',
            'OTP': OTP,
        }
        
        # return additionalFunction(res, OTP)
    except pyodbc.Error as pe:
         print(str(pe))
         return {
              'response': 'DataBase error ',
              'statusCode': FAILED
         }
    except Exception as e:
        def errorFunc(e):
            return e
        return handleError(e, errorFunc)
        
async def ApiWithProcedureOTPGet(db, query, queryParams, additionalFunction, OTP,MobileNo):
    try:
        await db.execute(f"""{query}""", queryParams)
        res = await db.fetchall()
        print('lenssss',query,queryParams)
        if len(res)>0 and res[0][0]!=None:
            print(res[0][0],"testres")
           
    
            
            tempData = json.loads(res[0][0])
            print('tempData',tempData)
            print('queue data', 
                #   json.dumps({
                #                     'action':'otp',
                #                     'body':{
                #                         'tempData': tempData,
                #                         'MobileNo': MobileNo,
                #                         'OTP':OTP
                #                     }
                #                 }) 
                                )
            await publish(queueName='payprenotificationService', message = {
                                    'action':'otp',
                                    'body':{
                                        'tempData': tempData,
                                        'MobileNo': MobileNo,
                                        'OTP':OTP
                                    }
                                })
            return {
            'statusCode':1,
            'response': 'Otp Sent Successfully',
            'OTP': OTP,
             }
        else:
            return{
            'statusCode':0,
            'response': 'Otp not Sended',
            'OTP': OTP,
        }
        
        # return additionalFunction(res, OTP)
    except pyodbc.Error as pe:
         print(str(pe))
         return {
              'response': 'DataBase error ',
              'statusCode': FAILED
         }
    except Exception as e:
        def errorFunc(e):
            return e
        return handleError(e, errorFunc)
        
async def ApiWithProcedureOTP(db, query, queryParams, additionalFunction, OTP):
    try:
        print('queryParams', queryParams)
        print(f"""{query}""", queryParams)
        await db.execute(f"""{query}""", queryParams)
        res = await db.fetchall()
        print('len',len(res),res)
        if res[0][1]==1:
            print(res[0][3])
           
    
            
            tempData = json.loads(res[0][3])
            print('tempData',tempData)
            print('queue data', 
                  json.dumps({
                                    'action':'otp',
                                    'body':{
                                        'tempData': tempData,
                                        'MobileNo': queryParams,
                                        'OTP':OTP
                                    }
                                }) 
                                )

            await publish(queueName='payprenotificationService', message = {
                                    'action':'otp',
                                    'body':{
                                        'tempData': tempData,
                                        'MobileNo': queryParams,
                                        'OTP':OTP
                                    }
                                })
        
        # if res[0][1]==1:
        #     msgquery = 'EXEC getMessagetemplate @MessageHeader=?'
        #     msgqueryParams = ('OTP')
        #     await db.execute(f"""{msgquery}""", msgqueryParams)
        #     msgres = await db.fetchall()
        #     print(msgres[0][0],len(msgres),"test")
        #     if (len(msgres)>0):
        #         MessageTemplate=json.loads(msgres[0][0])
        #         print(MessageTemplate,"MessageTemplate")
        #         if len(MessageTemplate):
        #             data=sendSMS(MessageTemplate[0]['Subject'],'',MessageTemplate[0]['MessageBody'],MessageTemplate[0]['Peid'],MessageTemplate[0]['Tpid'])
        #     pass
        return additionalFunction(res, OTP)
    except pyodbc.Error as pe:
         print(str(pe))
         return {
              'response': 'DataBase error ',
              'statusCode': FAILED
         }
    except Exception as e:
        def errorFunc(e):
            return e
        return handleError(e, errorFunc)
        
def additionalFunctionOTP(res: List, OTP: str) -> Dict:
    if len(res) == 0:
        return {
            'statusCode': FAILED,
            'response': 'User not found'
        }
    elif res[0][0] == None:
        return {
            'statusCode': FAILED,
            'response': 'OTP could not be sent'
        }
    else:
        return {
            'statusCode': res[0][1],
            'response': res[0][0],
            'OTP': OTP,
            'UserId':res[0][2]
        }
