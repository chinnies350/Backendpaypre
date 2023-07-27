from fastapi.routing import APIRouter
from schemas import PostOrderHdr,PutOrderHdr
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from typing import Tuple,Dict,List
import json
from joblib import Parallel, delayed
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureTrans, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut

router = APIRouter(prefix='/orderHdr', tags=['OrderHdr'])

def callFunction(i):
    return i.dict()

@router.get('')
async def orderHdrGet(OrderId:Optional[int] = Query(None), ActiveStatus:Optional[str] = Query(None), CompId:Optional[int]=Query(None), BranchId:Optional[int]=Query(None), db:Cursor= Depends(get_cursor))->Dict:
    query :str = 'EXEC getOrderHdr @OrderId=?, @ActiveStatus=?, @CompId=? ,@BranchId=?'
    queryParams :Tuple = ( OrderId, ActiveStatus, CompId, BranchId )

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)



@router.post('')
async def orderHdrPost(request:PostOrderHdr, db:Cursor= Depends(get_cursor))-> Dict:
    query :str= f"""EXEC postOrderHdr @CompId=?, @BranchId=?, @OrderDate=?, @OrderType=?, @CustSuppId=?, @Reference=?, @BookingType=?, @ServiceProvider=?,
        @ActiveStatus=?, @CreatedBy=?, @OrderDtlDetails=?"""
    
    def transformFunction(request:PostOrderHdr):
        OrderDtlDetails: str | None | List = None
        
        if request.OrderDtlDetails != None:
            OrderDtlDetails = Parallel(
                n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.OrderDtlDetails)
            OrderDtlDetails = json.dumps(OrderDtlDetails,indent=4, sort_keys=True, default=str)
        else:
            OrderDtlDetails = None
        return (request.CompId, request.BranchId, request.OrderDate, request.OrderType, request.CustSuppId, request.Reference, request.BookingType, request.ServiceProvider,
                request.ActiveStatus, request.CreatedBy, OrderDtlDetails)

    return await ApiWithProcedureTrans(db=db, 
                                    query=query,
                                    request=request, 
                                    transformParam=transformFunction, 
                                    additionalFunction=additionalFunctionPost)
    
    
@router.put('')
async def orderHdrPut(request: PutOrderHdr, db:Cursor = Depends(get_cursor))->Dict:
    query :str = 'EXEC putOrderHdr @OrderId=?, @ActiveStatus=?, @UpdatedBy=?'
    queryParams :Tuple = ( request.OrderId, request.ActiveStatus, request.UpdatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)