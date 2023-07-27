from fastapi.routing import APIRouter
from schemas import PostApplication, PutApplication
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from joblib import Parallel, delayed
import json
import asyncio
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete



router = APIRouter(prefix='/application', tags=['Application'])


@router.get('')
async def applicationGet(AppId:Optional[int]=Query(None), ActiveStatus:Optional[str]=Query(None),UserId:Optional[int]=Query(None),Type:Optional[str]=Query(None),SubId:Optional[int]=Query(None),CateId:Optional[int]=Query(None),BranchId:Optional[int]=Query(None), db:Cursor= Depends(get_cursor)):
    query = 'EXEC getApplication @AppId=?, @ActiveStatus=?, @UserId=?, @Type=?,@subId=?,@CateId=?,@BranchId=?'
    queryParams = ( AppId, ActiveStatus, UserId, Type,SubId,CateId,BranchId)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)
    
    
@router.post('')
async def applicationPost(request: PostApplication, db:Cursor= Depends(get_cursor)):
    query = 'EXEC postApplication @AppName=?, @AppDescription=?, @AppLogo=?, @CateId=?, @SubCateId=?, @BannerImage=?, @CreatedBy=?'
    queryParams = ( request.AppName, request.AppDescription, request.AppLogo, request.CateId, request.SubCateId, request.BannerImage, request.CreatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPost)

@router.put('')
async def applicationPut(request: PutApplication, db:Cursor = Depends(get_cursor)):
    query = 'EXEC putApplication @AppName=?, @AppDescription=?, @AppLogo=?, @CateId=?, @SubCateId=?, @BannerImage=?, @UpdatedBy=?, @AppId=?'
    queryParams = ( request.AppName, request.AppDescription, request.AppLogo, request.CateId, request.SubCateId, request.BannerImage, request.UpdatedBy, request.AppId)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)

@router.delete('')
async def applicationDelete(UpdatedBy: int, AppId: int, ActiveStatus: str,db:Cursor = Depends(get_cursor)):
    query = 'EXEC deleteApplication @UpdatedBy=?, @AppId=?, @ActiveStatus=?'
    queryParams = (  UpdatedBy, AppId, ActiveStatus)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)




