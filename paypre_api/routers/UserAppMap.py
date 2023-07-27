# from fastapi.routing import APIRouter
# from schemas import PostUserAppMap, PutUserAppMapPayment, PostFreeOption, PutUPIPmtStatus,PostInvoicedetails
# from aioodbc.cursor import Cursor
# from routers.config import get_cursor,logs_collection
# from fastapi import Depends
# from typing import Optional
# from fastapi import Query
# import datetime 
# from datetime import date
# import json
# from routers.eventServer import publish
# # from eventConsumer import publish
# from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost,additionalFunctionPostUserMapp, additionalFunctionPut, additionalFunctionDelete



# router = APIRouter(prefix='/userAppMap', tags=['UserAppMap'])

# def insert_log(user_id, message):
#     log_entry = {
#         'timestamp': datetime.datetime.utcnow(),
#         'user_id': user_id,
#         'message': message
#     }
    
#     logs_collection.insert_one(log_entry)

# @router.get('')
# async def userAppMapGet(UniqueId:Optional[int]=Query(None), AppId:Optional[str]=Query(None), UserId:Optional[int]=Query(None),Type:Optional[str]=Query(None),PaymentStatus:Optional[str]=Query(None), db:Cursor= Depends(get_cursor)):
#     query = 'EXEC getUserAppMap @UniqueId=?, @AppId=?, @UserId=?,@Type=?,@PaymentStatus=?'
#     queryParams = ( UniqueId,AppId, UserId,Type,PaymentStatus)

#     return await ApiWithProcedureGet(db=db, 
#                                         query=query, 
#                                         queryParams=queryParams)

# @router.post('')
# async def userAppMapPost(request: PostUserAppMap, db:Cursor= Depends(get_cursor)):
#     try:
#         query = 'EXEC postUserAppMap @UserId=?, @AppId=?, @PricingId=?, @CompId=?, @PurDate=?, @PaymentMode=?, @PaymentStatus=?, @LicenseStatus=?, @Price=?, @TaxId=?, @TaxAmount=?, @NetPrice=?, @ValidityStart=?, @ValidityEnd=?, @CreatedBy=?,@NoofDays=?'
#         queryParams = ( request.UserId, request.AppId, request.PricingId, request.CompId, request.PurDate, request.PaymentMode, request.PaymentStatus, request.LicenseStatus, request.Price, request.TaxId, request.TaxAmount, request.NetPrice, request.ValidityStart, request.ValidityEnd ,request.CreatedBy,request.NoofDays)
        
#         async def manipulatePostResponse(res):
#             current_date = date.today()
#             formatted_date = current_date.strftime("%B %d, %Y")
#             if res[0][1] == 1:
#                 insert_log(request.UserId, f"The Purchase of your Application starts from {request.ValidityStart} to {request.ValidityEnd}")
#                 userData = json.loads(res[0][3])
#                 tempData = json.loads(res[0][5])
#                 await publish(queueName='payprenotificationService', message = {
#                                     'action':'booking',
#                                     'body':{
#                                         'tempData': tempData,
#                                         'userData': userData,
#                                         'BookingId':res[0][2],
#                                         'totalAmount':str(request.NetPrice),
#                                         'AppName':res[0][4],
#                                         'paymenttype':res[0][6],
#                                         'taxAmount':str(request.TaxAmount),
#                                         'PaymentDate':str(formatted_date)
#                                     }
#                                 })
#             return additionalFunctionPostUserMapp(res)

#         return await ApiWithProcedure(db=db, 
#                                         query=query, 
#                                         queryParams=queryParams, 
#                                         additionalFunction=manipulatePostResponse)
#     except Exception as e:
#         print('Exception error',str(e))
#         return e

# @router.put('/paymentStatus')
# async def userAppMapPut(request: PutUserAppMapPayment, db:Cursor = Depends(get_cursor)):
#     query = 'EXEC putUserAppMap @PaymentStatus=?, @UpdatedBy=?, @UniqueId=?'
#     queryParams = ( request.PaymentStatus, request.UpdatedBy, request.UniqueId)
    

#     return await ApiWithProcedure(db=db, 
#                                     query=query, 
#                                     queryParams=queryParams, 
#                                     additionalFunction=additionalFunctionPut)
    
# @router.post('/FreeOption')
# async def userAppMapPost(request: PostFreeOption, db:Cursor= Depends(get_cursor)):
#     query = 'EXEC postFreeOption @UserId=?, @AppId=?, @PricingId=?, @CompId=?, @PurDate=?, @PaymentMode=?, @PaymentStatus=?, @LicenseStatus=?, @Price=?, @TaxId=?, @TaxAmount=?, @NetPrice=?, @ValidityStart=?, @ValidityEnd=?, @CreatedBy=?'
#     queryParams = ( request.UserId, request.AppId, request.PricingId, request.CompId, request.PurDate, request.PaymentMode, request.PaymentStatus, request.LicenseStatus, request.Price, request.TaxId, request.TaxAmount, request.NetPrice, request.ValidityStart, request.ValidityEnd ,request.CreatedBy)

#     return await ApiWithProcedure(db=db, 
#                                     query=query, 
#                                     queryParams=queryParams, 
#                                     additionalFunction=additionalFunctionPost)
    
# @router.post('/send-invoicedetail')
# async def invoicedeatilsPost(request: PostInvoicedetails, db:Cursor= Depends(get_cursor)):
#     try:
#         query = 'EXEC postInvoicedeatils @UniqueId=?, @MailId=?'
#         queryParams = (request.UniqueId, request.MailId)
        
#         async def manipulatePostResponse(res):
#             current_date = date.today()
#             formatted_date = current_date.strftime("%B %d, %Y")
#             if len(res)>0 :
#                 tempData=json.loads(res[0][23])                
#                 userData = json.loads(res[0][23])                
#                 tempData = json.loads(res[0][24])
#                 await publish(queueName='payprenotificationService', message = {
#                                     'action':'booking',
#                                     'body':{
#                                         'tempData': tempData,
#                                         'userData': userData,
#                                         'BookingId':res[0][0],
#                                         'totalAmount':str(res[0][12]),
#                                         'AppName':res[0][22],
#                                         'paymenttype':res[0][26],
#                                         'taxAmount':str(res[0][11]),
#                                         'PaymentDate':str(formatted_date),
#                                         'link':str(res[0][25])
#                                     }
#                                 })
#                 return additionalFunctionPost(res)
#             else:
#                 return{
#                     'StatusCode':0,
#                     'response':'No data Found'
#                 }
        

#         return await ApiWithProcedure(db=db, 
#                                         query=query, 
#                                         queryParams=queryParams, 
#                                         additionalFunction=manipulatePostResponse)
#     except Exception as e:
#         print('Exception error',str(e))
#         return e
    

from fastapi.routing import APIRouter
from schemas import PostUserAppMap, PutUserAppMapPayment, PostFreeOption, PutUPIPmtStatus,PostInvoicedetails
from aioodbc.cursor import Cursor
from routers.config import get_cursor,logs_collection
from fastapi import Depends
from typing import Optional
from fastapi import Query
import datetime 
from datetime import date
import json
from routers.eventServer import publish
# from eventConsumer import publish
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost,additionalFunctionPostUserMapp, additionalFunctionPut, additionalFunctionDelete



router = APIRouter(prefix='/userAppMap', tags=['UserAppMap'])

def insert_log(user_id, message):
    log_entry = {
        'timestamp': datetime.datetime.utcnow(),
        'user_id': user_id,
        'message': message
    }
    
    logs_collection.insert_one(log_entry)

@router.get('')
async def userAppMapGet(UniqueId:Optional[int]=Query(None), AppId:Optional[str]=Query(None), UserId:Optional[int]=Query(None),Type:Optional[str]=Query(None),PaymentStatus:Optional[str]=Query(None), db:Cursor= Depends(get_cursor)):
    query = 'EXEC getUserAppMap @UniqueId=?, @AppId=?, @UserId=?,@Type=?,@PaymentStatus=?'
    queryParams = ( UniqueId,AppId, UserId,Type,PaymentStatus)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)

@router.post('')
async def userAppMapPost(request: PostUserAppMap, db:Cursor= Depends(get_cursor)):
    try:
        query = 'EXEC postUserAppMap @UserId=?, @AppId=?, @PricingId=?, @CompId=?, @PurDate=?, @PaymentMode=?, @PaymentStatus=?, @LicenseStatus=?, @Price=?, @TaxId=?, @TaxAmount=?, @NetPrice=?, @ValidityStart=?, @ValidityEnd=?, @CreatedBy=?,@NoofDays=?'
        queryParams = ( request.UserId, request.AppId, request.PricingId, request.CompId, request.PurDate, request.PaymentMode, request.PaymentStatus, request.LicenseStatus, request.Price, request.TaxId, request.TaxAmount, request.NetPrice, request.ValidityStart, request.ValidityEnd ,request.CreatedBy,request.NoofDays)
        
        async def manipulatePostResponse(res):
            formattedStart_date = request.ValidityStart.strftime("%B %d, %Y")
            formattedEnd_date = request.ValidityEnd.strftime("%B %d, %Y")
            userData = json.loads(res[0][3])
            userName = userData[0]["UserName"]
            AppName = res[0][4]
            if res[0][1] == 1:
                insert_log(request.UserId, f"Dear {userName}, The Purchase of your {AppName} Application is successfull. Validity starts from {formattedStart_date} to {formattedEnd_date}")
                userData = json.loads(res[0][3])
                tempData = json.loads(res[0][5])
                await publish(queueName='notificationService', message = {
                                    'action':'booking',
                                    'body':{
                                        'tempData': tempData,
                                        'userData': userData,
                                        'BookingId':res[0][2],
                                        'AppName':None,
                                        'Link':f"https://paypre.in/restaurant/payment-page?paymentId={res[0][2]}"
                                    }
                                })
            return additionalFunctionPostUserMapp(res)

        return await ApiWithProcedure(db=db, 
                                        query=query, 
                                        queryParams=queryParams, 
                                        additionalFunction=manipulatePostResponse)
    except Exception as e:
        print('Exception error',str(e))
        return e

@router.put('/paymentStatus')
async def userAppMapPut(request: PutUserAppMapPayment, db:Cursor = Depends(get_cursor)):
    query = 'EXEC putUserAppMap @PaymentStatus=?, @UpdatedBy=?, @UniqueId=?'
    queryParams = ( request.PaymentStatus, request.UpdatedBy, request.UniqueId)
    
    async def manipulatePutResponse(res):
            current_date = date.today()
            formatted_date = current_date.strftime("%B %d, %Y")
            if res[0][1] == 1:
                userData = json.loads(res[0][3])
                tempData = json.loads(res[0][5])
                await publish(queueName='notificationService', message = {
                                    'action':'booking',
                                    'body':{
                                        'tempData': tempData,
                                        'userData': userData,
                                        'BookingId':(request.UniqueId),
                                        'totalAmount':userData[0]["NetPrice"],
                                        'AppName':res[0][4],
                                        'paymenttype':res[0][6],
                                        'taxAmount':userData[0]["TaxAmount"],
                                        'PaymentDate':str(formatted_date),
                                        'Link':f"https://paypre.in/paypre/payment-pdf?paymentId={request.UniqueId}"
                                    }
                                })
            return additionalFunctionPut(res)
    

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=manipulatePutResponse)
    
@router.post('/FreeOption')
async def userAppMapPost(request: PostFreeOption, db:Cursor= Depends(get_cursor)):
    query = 'EXEC postFreeOption @UserId=?, @AppId=?, @PricingId=?, @CompId=?, @PurDate=?, @PaymentMode=?, @PaymentStatus=?, @LicenseStatus=?, @Price=?, @TaxId=?, @TaxAmount=?, @NetPrice=?, @ValidityStart=?, @ValidityEnd=?, @CreatedBy=?'
    queryParams = ( request.UserId, request.AppId, request.PricingId, request.CompId, request.PurDate, request.PaymentMode, request.PaymentStatus, request.LicenseStatus, request.Price, request.TaxId, request.TaxAmount, request.NetPrice, request.ValidityStart, request.ValidityEnd ,request.CreatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPost)
    
@router.post('/send-invoicedetail')
async def invoicedeatilsPost(request: PostInvoicedetails, db:Cursor= Depends(get_cursor)):
    try:
        query = 'EXEC postInvoicedeatils @UniqueId=?, @MailId=?'
        queryParams = (request.UniqueId, request.MailId)
        
        async def manipulatePostResponse(res):
            current_date = date.today()
            formatted_date = current_date.strftime("%B %d, %Y")
            if len(res)>0 :
                tempData=json.loads(res[0][23])                
                userData = json.loads(res[0][23])                
                tempData = json.loads(res[0][24])
                await publish(queueName='notificationService', message = {
                                    'action':'booking',
                                    'body':{
                                        'tempData': tempData,
                                        'userData': userData,
                                        'BookingId':res[0][0],
                                        'totalAmount':str(res[0][12]),
                                        'AppName':res[0][22],
                                        'paymenttype':res[0][26],
                                        'taxAmount':str(res[0][11]),
                                        'PaymentDate':str(formatted_date),
                                        'Link':str(res[0][25])
                                    }
                                })
                return additionalFunctionPost(res)
            else:
                return{
                    'StatusCode':0,
                    'response':'No data Found'
                }
        

        return await ApiWithProcedure(db=db, 
                                        query=query, 
                                        queryParams=queryParams, 
                                        additionalFunction=manipulatePostResponse)
    except Exception as e:
        print('Exception error',str(e))
        return e
    











