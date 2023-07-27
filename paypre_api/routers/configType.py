from fastapi.routing import APIRouter
from schemas import PostConfigType, PutConfigType
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete



router = APIRouter(prefix='/configType', tags=['ConfigType'])

@router.get('')
async def configTypeGet(TypeId:Optional[int] = Query(None), ActiveStatus:Optional[str] = Query(None), TypeName: Optional[str]=Query(None), db:Cursor= Depends(get_cursor)):
    query = 'EXEC getConfigType @TypeId=?, @ActiveStatus=?, @TypeName=?'
    queryParams = ( TypeId, ActiveStatus, TypeName)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)

@router.post('')
async def configTypePost(request: PostConfigType, db:Cursor= Depends(get_cursor)):
    query = 'EXEC postConfigType @TypeName=?, @CreatedBy=?'
    queryParams = ( request.TypeName, request.CreatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPost)

@router.put('')
async def configTypePut(request: PutConfigType, db:Cursor = Depends(get_cursor)):
    query = 'EXEC putConfigType @TypeName=?, @UpdatedBy=?, @TypeId=?'
    queryParams = ( request.TypeName, request.UpdatedBy, request.TypeId)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)

@router.delete('')
async def configTypePut(UpdatedBy: int, TypeId: int, ActiveStatus: str,db:Cursor = Depends(get_cursor)):
    query = 'EXEC deleteConfigType @UpdatedBy=?, @TypeId=?, @ActiveStatus=?'
    queryParams = (  UpdatedBy, TypeId, ActiveStatus)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)




