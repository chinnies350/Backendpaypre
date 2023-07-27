from fastapi.routing import APIRouter
from schemas import PutInwardDtl
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from typing import Tuple,Dict
from routers.utils.apiCommon import ApiWithProcedure,ApiWithProcedureGet, additionalFunctionPut


router = APIRouter(prefix='/inwardDtl', tags=['InwardDtl'])

@router.get('')
async def inwardDtlGet(InwardDtlId:Optional[int] = Query(None), ProdId:Optional[str] = Query(None), db:Cursor= Depends(get_cursor))->Dict:
    query :str = 'EXEC getInwardDtl @InwardDtlId=?, @ProdId=?'
    queryParams :Tuple = ( InwardDtlId, ProdId )

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)

@router.put('')
async def inwardDtlPut(request: PutInwardDtl, db:Cursor = Depends(get_cursor))->Dict:
    query :str = f"""EXEC putInwardDtl @InwardId=?, @ProdId=?, @BatchRef=?, @ReceivedQty=?, @AcceptedQty=?, @RejectedQty=?, @RejectionReason=?, @IssuedQty=?, @BalanceQty=?, 
        @InwardPrice=?, @MRP=?, @SellPrice=?, @WhSalePrice=?, @OfferPrice=?, @ACSellPrice=?, @InwardDtlId=?"""
    queryParams :Tuple = ( request.InwardId, request.ProdId, request.BatchRef, request.ReceivedQty, request.AcceptedQty, request.RejectedQty, request.RejectionReason, request.IssuedQty, request.BalanceQty,
        request.InwardPrice, request.MRP, request.SellPrice, request.WhSalePrice, request.OfferPrice, request.ACSellPrice, request.InwardDtlId)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)

