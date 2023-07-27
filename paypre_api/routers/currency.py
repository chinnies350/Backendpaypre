from fastapi.routing import APIRouter
from schemas import PostCurrency, PutCurrency
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete



router = APIRouter(prefix='/currency', tags=['Currency'])

@router.get('')
async def currencyGet(CurrId:Optional[str]=Query(None) ,ActiveStatus:Optional[str]=Query(None), db:Cursor= Depends(get_cursor)):
    query = 'EXEC getCurrency @CurrId=?, @ActiveStatus=?'
    queryParams = ( CurrId, ActiveStatus)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)

@router.post('')
async def currencyPost(request: PostCurrency, db:Cursor= Depends(get_cursor)):
    query = 'EXEC postCurrency @CurrName =?, @CurrShName =?, @ConvRate =?, @CreatedBy =?'
    queryParams = ( request.CurrName, request.CurrShName, request.ConvRate, request.CreatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPost)

@router.put('')
async def currencyPut(request: PutCurrency, db:Cursor = Depends(get_cursor)):
    query = 'EXEC putCurrency @CurrName =?, @CurrShName =?, @ConvRate =?, @UpdatedBy =?, @CurrId =?'
    queryParams = ( request.CurrName, request.CurrShName, request.ConvRate, request.UpdatedBy, request.CurrId)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)

@router.delete('')
async def currencyDelete(UpdatedBy: int, CurrId: int, ActiveStatus: str,db:Cursor = Depends(get_cursor)):
    query = 'EXEC deleteCurrency @UpdatedBy=?, @CurrId=?, @ActiveStatus=?'
    queryParams = (  UpdatedBy, CurrId, ActiveStatus)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)




