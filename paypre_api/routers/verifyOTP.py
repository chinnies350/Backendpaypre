from fastapi.routing import APIRouter
from schemas import VerifyOTP,GetOTP,SendLink
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from random import randint
import json
import re
from routers.utils.apiCommon import ApiWithProcedureOTP, additionalFunctionOTP,ApiWithProcedureOTPGet,ApiWithProcedurePaymentLink
from routers.sms import sendSMS


router = APIRouter(prefix='/verifyOTP', tags=['VerifyOTP'])




@router.post('')
async def verifyOTP(request: VerifyOTP, db:Cursor = Depends(get_cursor)):
    OTP = randint(100000, 999999)
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    Pattern = re.compile("(0|91)?[6-9][0-9]{9}")
    if Pattern.match(request.UserName):
        query = 'EXEC VerifyOTP @UserName =?'
        queryParams = (request.UserName)
        

        
        return await ApiWithProcedureOTP(db=db, 
                                        query=query, 
                                        queryParams=queryParams, 
                                        additionalFunction=additionalFunctionOTP,
                                        OTP=OTP
                                        )
    elif re.fullmatch(regex, request.UserName):
        query = 'EXEC VerifyOTP @UserName =?'
        queryParams = (request.UserName)

        return await ApiWithProcedureOTP(db=db, 
                                        query=query, 
                                        queryParams=queryParams, 
                                        additionalFunction=additionalFunctionOTP,
                                        OTP=OTP
                                        )
        
@router.post('/getOTP')
async def getOTP(request: GetOTP, db:Cursor = Depends(get_cursor)):
    OTP = randint(100000, 999999)
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    Pattern = re.compile("(0|91)?[6-9][0-9]{9}")
    if re.fullmatch(regex, request.UserName):
        query = 'EXEC getMessagetemplate @MessageHeader=?'
        queryParams = ('OTP')
        return await ApiWithProcedureOTPGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams, 
                                        additionalFunction=additionalFunctionOTP,
                                        OTP=OTP,
                                        MobileNo=request.UserName
        )
        
        # return {
        #     'statusCode':1,
        #     'response': "OTP Sended Successfully",
        #     'OTP': OTP
            
        # }
       
    elif Pattern.match(request.UserName):
        query = 'EXEC getMessagetemplate @MessageHeader=?'
        queryParams = ('OTP')
        return await ApiWithProcedureOTPGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams, 
                                        additionalFunction=additionalFunctionOTP,
                                        OTP=OTP,
                                        MobileNo=request.UserName
        )
        # return {
        #     'statusCode':1,
        #     'response': "OTP Sended Successfully",
        #     'OTP': OTP
            
        # }
    else:
      return ("please enter Valid Mobile")
  
  
# @router.post('/setUser')
# async def setUser(request: getOTP, db:Cursor = Depends(get_cursor)):
#     pass

@router.post('/setUser')
async def setUser(request: GetOTP, db:Cursor = Depends(get_cursor)):
    OTP = randint(100000, 999999)
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    Pattern = re.compile("(0|91)?[6-9][0-9]{9}")
    if re.fullmatch(regex, request.UserName):
        query = 'EXEC VerifyOTP @UserName =?,@Type=?'
        queryParams = (request.UserName,"N")
        return await ApiWithProcedureOTP(db=db, 
                                        query=query, 
                                        queryParams=queryParams, 
                                        additionalFunction=additionalFunctionOTP,
                                        OTP=OTP
        )
       
    elif Pattern.match(request.UserName):
        query = 'EXEC VerifyOTP @UserName =?,@Type=?'
        queryParams = (request.UserName,"N")
        return await ApiWithProcedureOTP(db=db, 
                                        query=query, 
                                        queryParams=queryParams, 
                                        additionalFunction=additionalFunctionOTP,
                                        OTP=OTP
                                        )
    else:
      return ("please enter Valid Mobile")
  
  
@router.post('/SendPaymentLink')
async def SendPaymentLink(request: SendLink, db:Cursor = Depends(get_cursor)):
    query = 'EXEC getMessagetemplate @MessageHeader=?'
    queryParams = (request.MessageHeader)
    
    return await ApiWithProcedurePaymentLink(db=db, 
                                        query=query, 
                                        queryParams=queryParams, 
                                        additionalFunction=additionalFunctionOTP,
                                        Link=request.Link,
                                        MobileNo=request.MobileNo
        )
    
    
    # await db.execute(f"""{query}""", queryParams)
    # res = await db.fetchall()
    # if (len(res)>0 and res[0][0]!=None):
    #     MessageTemplate=json.loads(res[0][0])
    #     if len(MessageTemplate):
    #         data=sendSMS(MessageTemplate[0]['Subject'],request.MobileNo,MessageTemplate[0]['MessageBody'],MessageTemplate[0]['Peid'],MessageTemplate[0]['Tpid'])
           
    #         if (data["statusCode"]==1):
    #             return {
    #                 'statusCode':1,
    #                 'response': "Payment link sended successfully", 
    #             }
    #         else:
    #             return {
    #                 'statusCode':0,
    #                 'response': "Payment link not sended", 
    #             }
    #     else:
    #         return {
    #                 'statusCode':0,
    #                 'response': "Message Template Not Found", 
    #             }
            
    # else:
    #         return {
    #                 'statusCode':0,
    #                 'response': "Message Template Not Found", 
    #             }
            
            
@router.post('/SendSMS')
async def SendSMSLink(request: SendLink, db:Cursor = Depends(get_cursor)):
    
    query = 'EXEC getMessagetemplate @MessageHeader=?'
    queryParams = (request.MessageHeader)
    
    
    await db.execute(f"""{query}""", queryParams)
    res = await db.fetchall()
    if (len(res)>0 and res[0][0]!=None):
        MessageTemplate=json.loads(res[0][0])
        if len(MessageTemplate):
            data=sendSMS(MessageTemplate[0]['Subject'],request.MobileNo,MessageTemplate[0]['MessageBody'],MessageTemplate[0]['Peid'],MessageTemplate[0]['Tpid'])
           
            if (data["statusCode"]==1):
                return {
                    'statusCode':1,
                    'response': f"{request.MessageHeader} sended successfully", 
                }
            else:
                return {
                    'statusCode':0,
                    'response': f"{request.MessageHeader} not sended", 
                }
        else:
            return {
                    'statusCode':0,
                    'response': "Message Template Not Found", 
                }
            
    else:
            return {
                    'statusCode':0,
                    'response': "Message Template Not Found", 
                }
        
        





# from fastapi.routing import APIRouter
# from schemas import VerifyOTP,GetOTP,SendLink
# from aioodbc.cursor import Cursor
# from routers.config import get_cursor
# from fastapi import Depends
# from typing import Optional
# from fastapi import Query
# from random import randint
# import json
# import re
# from routers.utils.apiCommon import ApiWithProcedureOTP, additionalFunctionOTP,ApiWithProcedureOTPGet,ApiWithProcedurePaymentLink
# from routers.sms import sendSMS


# router = APIRouter(prefix='/verifyOTP', tags=['VerifyOTP'])




# @router.post('')
# async def verifyOTP(request: VerifyOTP, db:Cursor = Depends(get_cursor)):
#     OTP = randint(100000, 999999)
#     regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
#     Pattern = re.compile("(0|91)?[6-9][0-9]{9}")
#     if Pattern.match(request.UserName):
#         query = 'EXEC VerifyOTP @UserName =?'
#         queryParams = (request.UserName)
        

        
#         return await ApiWithProcedureOTP(db=db, 
#                                         query=query, 
#                                         queryParams=queryParams, 
#                                         additionalFunction=additionalFunctionOTP,
#                                         OTP=OTP
#                                         )
#     elif re.fullmatch(regex, request.UserName):
#         query = 'EXEC VerifyOTP @UserName =?'
#         queryParams = (request.UserName)

#         return await ApiWithProcedureOTP(db=db, 
#                                         query=query, 
#                                         queryParams=queryParams, 
#                                         additionalFunction=additionalFunctionOTP,
#                                         OTP=OTP
#                                         )
        
# @router.post('/getOTP')
# async def getOTP(request: GetOTP, db:Cursor = Depends(get_cursor)):
#     OTP = randint(100000, 999999)
#     regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
#     Pattern = re.compile("(0|91)?[6-9][0-9]{9}")
#     if re.fullmatch(regex, request.UserName):
#         query = 'EXEC getMessagetemplate @MessageHeader=?'
#         queryParams = ('OTP')
#         return await ApiWithProcedureOTPGet(db=db, 
#                                         query=query, 
#                                         queryParams=queryParams, 
#                                         additionalFunction=additionalFunctionOTP,
#                                         OTP=OTP,
#                                         MobileNo=request.UserName
#         )
        
#         # return {
#         #     'statusCode':1,
#         #     'response': "OTP Sended Successfully",
#         #     'OTP': OTP
            
#         # }
       
#     elif Pattern.match(request.UserName):
#         query = 'EXEC getMessagetemplate @MessageHeader=?'
#         queryParams = ('OTP')
#         return await ApiWithProcedureOTPGet(db=db, 
#                                         query=query, 
#                                         queryParams=queryParams, 
#                                         additionalFunction=additionalFunctionOTP,
#                                         OTP=OTP,
#                                         MobileNo=request.UserName
#         )
#         # return {
#         #     'statusCode':1,
#         #     'response': "OTP Sended Successfully",
#         #     'OTP': OTP
            
#         # }
#     else:
#       return ("please enter Valid Mobile")
  
  
# # @router.post('/setUser')
# # async def setUser(request: getOTP, db:Cursor = Depends(get_cursor)):
# #     pass

# @router.post('/setUser')
# async def setUser(request: GetOTP, db:Cursor = Depends(get_cursor)):
#     OTP = randint(100000, 999999)
#     regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
#     Pattern = re.compile("(0|91)?[6-9][0-9]{9}")
#     if re.fullmatch(regex, request.UserName):
#         query = 'EXEC VerifyOTP @UserName =?,@Type=?'
#         queryParams = (request.UserName,"N")
#         return await ApiWithProcedureOTP(db=db, 
#                                         query=query, 
#                                         queryParams=queryParams, 
#                                         additionalFunction=additionalFunctionOTP,
#                                         OTP=OTP
#         )
       
#     elif Pattern.match(request.UserName):
#         query = 'EXEC VerifyOTP @UserName =?,@Type=?'
#         queryParams = (request.UserName,"N")
#         return await ApiWithProcedureOTP(db=db, 
#                                         query=query, 
#                                         queryParams=queryParams, 
#                                         additionalFunction=additionalFunctionOTP,
#                                         OTP=OTP
#                                         )
#     else:
#       return ("please enter Valid Mobile")
  
  
# @router.post('/SendPaymentLink')
# async def SendPaymentLink(request: SendLink, db:Cursor = Depends(get_cursor)):
#     query = 'EXEC getMessagetemplate @MessageHeader=?'
#     queryParams = (request.MessageHeader)
    
#     return await ApiWithProcedurePaymentLink(db=db, 
#                                         query=query, 
#                                         queryParams=queryParams, 
#                                         additionalFunction=additionalFunctionOTP,
#                                         Link=request.Link,
#                                         MobileNo=request.MobileNo
#         )
    
    
#     # await db.execute(f"""{query}""", queryParams)
#     # res = await db.fetchall()
#     # if (len(res)>0 and res[0][0]!=None):
#     #     MessageTemplate=json.loads(res[0][0])
#     #     if len(MessageTemplate):
#     #         data=sendSMS(MessageTemplate[0]['Subject'],request.MobileNo,MessageTemplate[0]['MessageBody'],MessageTemplate[0]['Peid'],MessageTemplate[0]['Tpid'])
           
#     #         if (data["statusCode"]==1):
#     #             return {
#     #                 'statusCode':1,
#     #                 'response': "Payment link sended successfully", 
#     #             }
#     #         else:
#     #             return {
#     #                 'statusCode':0,
#     #                 'response': "Payment link not sended", 
#     #             }
#     #     else:
#     #         return {
#     #                 'statusCode':0,
#     #                 'response': "Message Template Not Found", 
#     #             }
            
#     # else:
#     #         return {
#     #                 'statusCode':0,
#     #                 'response': "Message Template Not Found", 
#     #             }
            
            
# @router.post('/SendSMS')
# async def SendSMSLink(request: SendLink, db:Cursor = Depends(get_cursor)):
    
#     query = 'EXEC getMessagetemplate @MessageHeader=?'
#     queryParams = (request.MessageHeader)
    
    
#     await db.execute(f"""{query}""", queryParams)
#     res = await db.fetchall()
#     if (len(res)>0 and res[0][0]!=None):
#         MessageTemplate=json.loads(res[0][0])
#         if len(MessageTemplate):
#             data=sendSMS(MessageTemplate[0]['Subject'],request.MobileNo,MessageTemplate[0]['MessageBody'],MessageTemplate[0]['Peid'],MessageTemplate[0]['Tpid'])
           
#             if (data["statusCode"]==1):
#                 return {
#                     'statusCode':1,
#                     'response': f"{request.MessageHeader} sended successfully", 
#                 }
#             else:
#                 return {
#                     'statusCode':0,
#                     'response': f"{request.MessageHeader} not sended", 
#                 }
#         else:
#             return {
#                     'statusCode':0,
#                     'response': "Message Template Not Found", 
#                 }
            
#     else:
#             return {
#                     'statusCode':0,
#                     'response': "Message Template Not Found", 
#                 }
        
        