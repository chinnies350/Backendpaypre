from fastapi.routing import APIRouter
from schemas import PostAdminTax,PutUser
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete


router = APIRouter(prefix='/adminTax', tags=['AdminTax'])

@router.get('')
async def adminTaxGet(TaxId:Optional[int] = Query(None), ActiveStatus:Optional[str] = Query(None), db:Cursor= Depends(get_cursor)):
    query = 'EXEC getAdminTax @TaxId=?, @ActiveStatus=?'
    queryParams = ( TaxId, ActiveStatus)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)



@router.post('')
async def adminTaxPost(request: PostAdminTax, db:Cursor= Depends(get_cursor)):
    query = 'EXEC postAdminTax @TaxName=?, @TaxPercentage=?, @EffectiveFrom=?, @Reference=?, @CreatedBy=?'
    queryParams = ( request.TaxName, request.TaxPercentage, request.EffectiveFrom, request.Reference, request.CreatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPost)
    
    


