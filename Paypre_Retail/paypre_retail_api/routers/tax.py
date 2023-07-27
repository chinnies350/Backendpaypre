from fastapi.routing import APIRouter
from schemas import PostTaxMaster
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional,Tuple,Dict
from fastapi import Query
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost



router = APIRouter(prefix='/tax', tags=['Tax'])


@router.get('')
async def taxGet(TaxId:Optional[int] = Query(None), ActiveStatus:Optional[str] = Query(None), db:Cursor= Depends(get_cursor))->Dict:
    query :str = 'EXEC getTax @TaxId=?, @ActiveStatus=?'
    queryParams :Tuple = ( TaxId, ActiveStatus)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)

@router.post('')
async def taxPost(request: PostTaxMaster, db:Cursor= Depends(get_cursor))->Dict:
    query :str= 'EXEC postTax @CompId=?, @TaxName=?, @TaxPercentage=?, @EffectiveFrom=?, @Reference=?, @CreatedBy=?'
    queryParams :Tuple = ( request.CompId, request.TaxName, request.TaxPercentage, request.EffectiveFrom, request.Reference, request.CreatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPost)
    
