from fastapi.routing import APIRouter
# from schemas import PostBranch,PutBranch
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from routers.utils.apiCommon import ApiWithProcedureGet


router = APIRouter(prefix='/login', tags=['Login'])


@router.get('')


async def loginGet(UserName:Optional[str] = Query(None), Password:Optional[str] = Query(None),Type:Optional[str] = Query(None), CompId:Optional[int] = Query(None), UserId:Optional[int] = Query(None),BranchId:Optional[int] = Query(None),Pin:Optional[str] = Query(None) ,db:Cursor= Depends(get_cursor)):
    query = 'EXEC getLogin @UserName=?, @Password=?,@Type=?,@CompId=?,@UserId=?,@BranchId=?,@Pin=?'
    queryParams = ( UserName, Password,Type,CompId,UserId,BranchId,Pin)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)

# @router.get('')
# async def loginGet(UserName:Optional[str] = Query(None), Password:Optional[str] = Query(None),Type:Optional[str] = Query(None), CompId:Optional[int] = Query(None), UserId:Optional[int] = Query(None),BranchId:Optional[int] = Query(None), db:Cursor= Depends(get_cursor)):
#     query = 'EXEC getLogin @UserName=?, @Password=?,@Type=?,@CompId=?,@UserId=?,@BranchId=?'
#     queryParams = ( UserName, Password,Type,CompId,UserId,BranchId)

#     return await ApiWithProcedureGet(db=db, 
#                                         query=query, 
#                                         queryParams=queryParams)