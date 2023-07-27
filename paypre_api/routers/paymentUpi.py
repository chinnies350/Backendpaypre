from fastapi.routing import APIRouter
from schemas import PostPaymentUpiDetails,PutPaymentUpiDetails
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from typing import Tuple,Dict, List
import json
from joblib import Parallel, delayed
from routers.utils.apiCommon import ApiWithProcedure,ApiWithProcedureTrans, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete



router = APIRouter(prefix='/paymentUpiDetails', tags=['paymentUpiDetails'])
def callFunction(i):
    return i.dict()

@router.get('')
async def paymentUpiDetailsGet(activeStatus:Optional[str]=Query(None), type:Optional[str]=Query(None), AdminId:Optional[int]=Query(None),PaymentUPIDetailsId:Optional[int]=Query(None),db:Cursor= Depends(get_cursor)):
    query = 'EXEC getPaymentUPIDetails @activeStatus=?, @type=?, @UserId=?,@PaymentUPIDetailsId=?'
    queryParams = ( activeStatus, type, AdminId, PaymentUPIDetailsId)
    

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)
    

@router.post('')
async def paymentUpiDetailsPost(request: PostPaymentUpiDetails, db:Cursor= Depends(get_cursor)):
    query = 'EXEC postPaymentUpiDetails  @MobileNo=?,@Name=?,@UPIId=?,@UserId=?,@CompId=?,@BrId=?,@type=?,@MerchantCode=?,@MerchantId=?,@mode=?,@orgid=?,@sign=?,@url=?,@CreatedBy=?'
    queryParams = ( request.MobileNo, request.Name, request.UPIId, request.UserId, request.CompId, request.BrId, request.type, request.MerchantCode, request.MerchantId,request.mode,request.orgid,request.sign, request.url, request.CreatedBy)
    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPost)
    

@router.put('')
async def paymentUpiDetailsPut(request: PutPaymentUpiDetails, db:Cursor = Depends(get_cursor)):
    query = 'EXEC putPaymentUpiDetails  @MobileNo=?,@Name=?,@UPIId=?,@AdminId=?,@CompId=?,@BranchId=?,@type=?,@MerchantCode=?,@MerchantId=?,@mode=?,@orgid=?,@sign=?,@url=?,@UpdatedBy=?,@PaymentUPIDetailsId=?'
    queryParams = ( request.MobileNo, request.Name, request.UPIId, request.AdminId, request.CompId, request.BranchId, request.type, request.MerchantCode, request.MerchantId,request.mode,request.orgid,request.sign, request.url, request.UpdatedBy, request.PaymentUPIDetailsId)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)
    
    
@router.delete('')
async def paymentUpiDetailsdelete(PaymentUPIDetailsId: int, ActiveStatus: str, UpdatedBy: int, CompId: Optional[int]=Query(None), BranchId: Optional[int]=Query(None) ,db:Cursor = Depends(get_cursor)):
    query = 'EXEC deletePaymentUPIDetails @PaymentUPIDetailsId=?, @ActiveStatus=?, @UpdatedBy=?,@CompId=?,@BranchId=?'
    queryParams = (  PaymentUPIDetailsId, ActiveStatus, UpdatedBy, CompId, BranchId)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)


    
# postPaymentUpiDetails







# from fastapi.routing import APIRouter
# from schemas import PostPaymentUpiDetails,PutPaymentUpiDetails
# from aioodbc.cursor import Cursor
# from routers.config import get_cursor
# from fastapi import Depends
# from typing import Optional
# from fastapi import Query
# from typing import Tuple,Dict, List
# import json
# from joblib import Parallel, delayed
# from routers.utils.apiCommon import ApiWithProcedure,ApiWithProcedureTrans, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete



# router = APIRouter(prefix='/paymentUpiDetails', tags=['paymentUpiDetails'])
# def callFunction(i):
#     return i.dict()

# @router.get('')
# async def paymentUpiDetailsGet(activeStatus:Optional[str]=Query(None), type:Optional[str]=Query(None), AdminId:Optional[int]=Query(None),db:Cursor= Depends(get_cursor)):
#     query = 'EXEC getPaymentUPIDetails @activeStatus=?, @type=?, @UserId=?'
#     queryParams = ( activeStatus, type, AdminId)
    

#     return await ApiWithProcedureGet(db=db, 
#                                         query=query, 
#                                         queryParams=queryParams)
    

# @router.post('')
# async def paymentUpiDetailsPost(request: PostPaymentUpiDetails, db:Cursor= Depends(get_cursor)):
#     query = 'EXEC postPaymentUpiDetails  @MobileNo=?,@Name=?,@UPIId=?,@UserId=?,@CompId=?,@BrId=?,@type=?,@MerchantCode=?,@MerchantId=?,@mode=?,@orgid=?,@sign=?,@url=?,@CreatedBy=?'
#     queryParams = ( request.MobileNo, request.Name, request.UPIId, request.UserId, request.CompId, request.BrId, request.type, request.MerchantCode, request.MerchantId,request.mode,request.orgid,request.sign, request.url, request.CreatedBy)
#     return await ApiWithProcedure(db=db, 
#                                     query=query, 
#                                     queryParams=queryParams, 
#                                     additionalFunction=additionalFunctionPost)
    

# @router.put('')
# async def paymentUpiDetailsPut(request: PutPaymentUpiDetails, db:Cursor = Depends(get_cursor)):
#     query = 'EXEC putPaymentUpiDetails  @MobileNo=?,@Name=?,@UPIId=?,@AdminId=?,@CompId=?,@BranchId=?,@type=?,@MerchantCode=?,@MerchantId=?,@mode=?,@orgid=?,@sign=?,@url=?,@UpdatedBy=?,@PaymentUPIDetailsId=?'
#     queryParams = ( request.MobileNo, request.Name, request.UPIId, request.AdminId, request.CompId, request.BranchId, request.type, request.MerchantCode, request.MerchantId,request.mode,request.orgid,request.sign, request.url, request.UpdatedBy, request.PaymentUPIDetailsId)

#     return await ApiWithProcedure(db=db, 
#                                     query=query, 
#                                     queryParams=queryParams, 
#                                     additionalFunction=additionalFunctionPut)
    
    
# @router.delete('')
# async def paymentUpiDetailsdelete(PaymentUPIDetailsId: int, ActiveStatus: str, UpdatedBy: int, CompId: Optional[int]=Query(None), BranchId: Optional[int]=Query(None) ,db:Cursor = Depends(get_cursor)):
#     query = 'EXEC deletePaymentUPIDetails @PaymentUPIDetailsId=?, @ActiveStatus=?, @UpdatedBy=?,@CompId=?,@BranchId=?'
#     queryParams = (  PaymentUPIDetailsId, ActiveStatus, UpdatedBy, CompId, BranchId)

#     return await ApiWithProcedure(db=db, 
#                                     query=query, 
#                                     queryParams=queryParams, 
#                                     additionalFunction=additionalFunctionDelete)


    
# # postPaymentUpiDetails


