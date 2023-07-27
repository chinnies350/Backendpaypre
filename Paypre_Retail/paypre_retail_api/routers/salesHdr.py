from fastapi.routing import APIRouter
from schemas import PostSalesHdr,PutSalesHdr
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from typing import Tuple,Dict,List
import json
from joblib import Parallel, delayed
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureTrans, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut

router = APIRouter(prefix='/salesHdr', tags=['SalesHdr'])

def callFunction(i):
    return i.dict()


@router.get('')
async def salesHdrGet(SalesId:Optional[int] = Query(None), ActiveStatus:Optional[str] = Query(None), CompId:Optional[int] = Query(None), BranchId:Optional[int] =Query(None), db:Cursor= Depends(get_cursor))->Dict:
    query :str = 'EXEC getSalesHdr @SalesId=?, @ActiveStatus=?, @CompId=?, @BranchId=?'
    queryParams :Tuple = ( SalesId, ActiveStatus, CompId, BranchId)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)
    
@router.post('')
async def salesHdrPost(request:PostSalesHdr, db:Cursor= Depends(get_cursor))-> Dict:
    query :str= f"""EXEC postSalesHdr @CompId=?, @BranchId=?, @SalesDate=?, @UserId=?, @OrderId=?, @AddlInfo=?, @BillAmount=?, @OverallDisc=?,
        @TaxAmount=?, @VatAmount=?, @NetAmount=?, @PaymentType=?, @GivenAmt=?, @BalGiven=?, @ActiveStatus=?, @BookingMedia=?, @PaymentStatus=?, @CreatedBy=?,
        @SalesDtlDetails=?, @SalesTaxDtlDetails=?, @SalesTableLinkDetails=?"""
    
    def transformFunction(request:PostSalesHdr):
        SalesDtlDetails: str | None | List = None
        SalesTaxDtlDetails: str | None | List = None
        SalesTableLinkDetails: str | None | List = None
        
        if request.SalesDtlDetails != None:
            SalesDtlDetails = Parallel(
                n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.SalesDtlDetails)
            SalesDtlDetails = json.dumps(SalesDtlDetails,indent=4, sort_keys=True, default=str)
        else:
            SalesDtlDetails = None
            
        if request.SalesTaxDtlDetails != None:
            SalesTaxDtlDetails = Parallel(
                n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.SalesTaxDtlDetails)
            SalesTaxDtlDetails = json.dumps(SalesTaxDtlDetails,indent=4, sort_keys=True, default=str)
        else:
            SalesTaxDtlDetails = None
            
        if request.SalesTableLinkDetails != None:
            SalesTableLinkDetails = Parallel(
                n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.SalesTableLinkDetails)
            SalesTableLinkDetails = json.dumps(SalesTableLinkDetails,indent=4, sort_keys=True, default=str)
        else:
            SalesTableLinkDetails = None
            
        return (request.CompId, request.BranchId, request.SalesDate, request.UserId, request.OrderId, request.AddlInfo, request.BillAmount, request.OverallDisc,
                request.TaxAmount, request.VatAmount, request.NetAmount, request.PaymentType, request.GivenAmt, request.BalGiven, request.ActiveStatus, request.BookingMedia, request.PaymentStatus, request.CreatedBy,
                SalesDtlDetails, SalesTaxDtlDetails, SalesTableLinkDetails)

    return await ApiWithProcedureTrans(db=db, 
                                    query=query,
                                    request=request, 
                                    transformParam=transformFunction, 
                                    additionalFunction=additionalFunctionPost)


@router.put('')
async def salesHdrPut(request: PutSalesHdr, db:Cursor = Depends(get_cursor))->Dict:
    query :str = f"""EXEC putSalesHdr @SalesId=?, @ActiveStatus=?, @UpdatedBy=?"""
    queryParams :Tuple = ( request.SalesId, request.ActiveStatus, request.UpdatedBy )

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)