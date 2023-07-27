from fastapi.routing import APIRouter
from schemas import PutUPIPmtStatus
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from routers.utils.apiCommon import ApiWithProcedure,additionalFunctionPut

router = APIRouter(prefix='/UPIPmtStatus', tags=['UPIPmtStatus'])

@router.put('')
async def UPIPmtStatusPut(request: PutUPIPmtStatus, db:Cursor = Depends(get_cursor)):
    query = 'EXEC putUPIPmtStatus @PaymentStatus=?,@TransactionId=?,@BankName=?,@BankReferenceNumber=?, @UpdatedBy=?, @UniqueId=?'
    queryParams = ( request.PaymentStatus, request.TransactionId, request.BankName, request.BankReferenceNumber, request.UpdatedBy, request.bookingId)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)