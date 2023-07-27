from fastapi.routing import APIRouter
from schemas import PostConfigType, PutConfigType
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional, Tuple,Dict
from fastapi import Query
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete



router = APIRouter(prefix='/configType', tags=['ConfigType'])

@router.get('')
async def configTypeGet(TypeId:Optional[int] = Query(None), ActiveStatus:Optional[str] = Query(None), TypeName: Optional[str]=Query(None), db:Cursor= Depends(get_cursor))->Dict:
    query :str = 'EXEC getConfigType @TypeId=?, @ActiveStatus=?, @TypeName=?'
    queryParams :Tuple = ( TypeId, ActiveStatus, TypeName)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)


@router.post('')
async def configTypePost(request: PostConfigType, db:Cursor= Depends(get_cursor))->Dict:
    query :str = 'EXEC postConfigType @TypeName=?, @CreatedBy=?'
    queryParams :Tuple = ( request.TypeName, request.CreatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPost)
    
@router.put('')
async def configTypePut(request: PutConfigType, db:Cursor = Depends(get_cursor))->Dict:
    query :str = 'EXEC putConfigType @TypeName=?, @UpdatedBy=?, @TypeId=?'
    queryParams :Tuple = ( request.TypeName, request.UpdatedBy, request.TypeId)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)
    
@router.delete('')
async def configTypeDelete(UpdatedBy: int, TypeId: int, ActiveStatus: str,db:Cursor = Depends(get_cursor))->Dict:
    query :str = 'EXEC deleteConfigType @UpdatedBy=?, @TypeId=?, @ActiveStatus=?'
    queryParams :Tuple = (  UpdatedBy, TypeId, ActiveStatus)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)

