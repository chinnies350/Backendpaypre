from fastapi.routing import APIRouter
from schemas import PostPricingType, PutPricingType
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from joblib import Parallel, delayed
import json
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete



router = APIRouter(prefix='/pricingType', tags=['pricingType'])


@router.get('')
async def pricingTypeGet(PricingId:Optional[str]=Query(None) ,ActiveStatus:Optional[str]=Query(None), AppId:Optional[int]=Query(None), NoOfDays:Optional[int]=Query(None),Type:Optional[str]=Query(None),UserId:Optional[int]=Query(None),db:Cursor= Depends(get_cursor)):
    query = 'EXEC getPricingType @PricingId=?, @ActiveStatus=?, @AppId=?, @NoOfDays=?, @Type=?,@UserId=?'
    queryParams = (PricingId, ActiveStatus, AppId, NoOfDays, Type,UserId)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)

@router.post('')
async def pricingTypePost(request: PostPricingType, db:Cursor= Depends(get_cursor)):
    query = 'EXEC postPricingType @AppId=?,@PricingName=?, @Price=?, @DisplayPrice=?, @PriceTag=?, @TaxId=?, @TaxAmount=?, @NetPrice=?, @CurrId=?, @NoOfDays=?, @CreatedBy=?'
    queryParams = ( request.AppId, request.PricingName, request.Price, request.DisplayPrice, request.PriceTag, request.TaxId, request.TaxAmount, request.NetPrice, request.CurrId, request.NoOfDays, request.CreatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPost)

@router.put('')
async def pricingTypePut(request: PutPricingType, db:Cursor = Depends(get_cursor)):
    query = 'EXEC putPricingType @AppId=?,@PricingName=?, @Price=?, @DisplayPrice=?, @PriceTag=?, @TaxId=?, @TaxAmount=?, @NetPrice=?, @CurrId=?, @NoOfDays=?, @UpdatedBy=?, @PricingId=?'
    queryParams = ( request.AppId, request.PricingName, request.Price, request.DisplayPrice, request.PriceTag, request.TaxId, request.TaxAmount, request.NetPrice, request.CurrId, request.NoOfDays,request.UpdatedBy, request.PricingId)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)

@router.delete('')
async def pricingTypeDelete(UpdatedBy: int, PricingId: int, ActiveStatus: str,db:Cursor = Depends(get_cursor)):
    query = 'EXEC deletePricingType @UpdatedBy=?, @PricingId=?, @ActiveStatus=?'
    queryParams = (  UpdatedBy, PricingId, ActiveStatus)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)




