from fastapi.routing import APIRouter
from schemas import PostCompAppMap,PutCompAppMap
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete

router = APIRouter(prefix='/compAppMap', tags=['CompAppMap'])


@router.get('')
async def compAppMapGet(UniqueId:Optional[int] = Query(None), ActiveStatus:Optional[str] = Query(None), CompId:Optional[int]=Query(None), BranchId:Optional[int]=Query(None), AppId:Optional[int]=Query(None), db:Cursor= Depends(get_cursor)):
    query = 'EXEC getCompAppMap @UniqueId=?, @ActiveStatus=?, @CompId=?, @BranchId=?, @AppId=?'
    queryParams = ( UniqueId, ActiveStatus, CompId, BranchId, AppId)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)

@router.post('')
async def compAppMapPost(request: PostCompAppMap, db:Cursor= Depends(get_cursor)):
    query = f"""EXEC postCompAppMap @CompId=?, @BranchId=?, @AppId=?, @CreatedBy=?"""
    queryParams = (  request.CompId, request.BranchId, request.AppId, request.CreatedBy )

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPost)
    
@router.put('')
async def compAppMapPut(request: PutCompAppMap, db:Cursor = Depends(get_cursor)):
    query = f"""EXEC putCompAppMap @CompId=?, @BranchId=?, @AppId=?, @UpdatedBy=?, @UniqueId=?"""
    queryParams = ( request.CompId, request.BranchId, request.AppId, request.UpdatedBy, request.UniqueId )

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)
    
@router.delete('')
async def compAppMapdelete(UniqueId: int, ActiveStatus: str, UpdatedBy: int, db:Cursor = Depends(get_cursor)):
    query = 'EXEC deleteCompAppMap @UniqueId=?, @ActiveStatus=?, @UpdatedBy=?'
    queryParams = (  UniqueId, ActiveStatus, UpdatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)
    


