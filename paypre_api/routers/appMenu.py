from fastapi.routing import APIRouter
from schemas import PostAppMenu,putAppMenu
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete

router = APIRouter(prefix='/appMenu', tags=['AppMenu'])

@router.get('')
async def appMenuGet(MenuId:Optional[int] = Query(None), ActiveStatus:Optional[str] = Query(None), AppId:Optional[int] = Query(None), db:Cursor= Depends(get_cursor)):
    query = 'EXEC getAppMenu @MenuId=?, @ActiveStatus=?, @AppId=?'
    queryParams = ( MenuId, ActiveStatus, AppId)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)


@router.post('')
async def appMenuPost(request: PostAppMenu, db:Cursor= Depends(get_cursor)):
    query = f"""EXEC postAppMenu @AppId=?, @MenuName=?, @Level=?, @Level1Id=?, @Level2Id=?, @CreatedBy=?"""
    queryParams = (  request.AppId, request.MenuName, request.Level, request.Level1Id, request.Level2Id, request.CreatedBy )

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPost)
    
@router.put('')
async def appMenuPut(request: putAppMenu, db:Cursor = Depends(get_cursor)):
    query = f"""EXEC putAppMenu @AppId=?, @MenuName=?, @Level=?, @Level1Id=?, @Level2Id=?, @UpdatedBy=?, @MenuId=?"""
    queryParams = ( request.AppId, request.MenuName, request.Level, request.Level1Id, request.Level2Id, request.UpdatedBy, request.MenuId )

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)
    
@router.delete('')
async def appMenudelete(MenuId: int, ActiveStatus: str, UpdatedBy: int, db:Cursor = Depends(get_cursor)):
    query = 'EXEC deleteAppMenu @MenuId=?, @ActiveStatus=?, @UpdatedBy=?'
    queryParams = (  MenuId, ActiveStatus, UpdatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)
    
