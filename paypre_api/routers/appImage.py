from fastapi.routing import APIRouter
from schemas import PostAppImage, PutAppImage
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete



router = APIRouter(prefix='/appImage', tags=['AppImage'])

@router.get('')
async def appImageGet(ImageId:Optional[int]=Query(None), ActiveStatus:Optional[str]=Query(None), db:Cursor= Depends(get_cursor)):
    query = 'EXEC getAppImage @ImageId=?, @ActiveStatus=?'
    queryParams = ( ImageId, ActiveStatus)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)

@router.post('')
async def appImagePost(request: PostAppImage, db:Cursor= Depends(get_cursor)):
    query = 'EXEC postAppImage @AppId=?, @ImageType=?, @ImageName=?, @ImageLink=?, @CreatedBy=?'
    queryParams = ( request.AppId, request.ImageType, request.ImageName, request.ImageLink, request.CreatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPost)

@router.put('')
async def appImagePut(request: PutAppImage, db:Cursor = Depends(get_cursor)):
    query = 'EXEC putAppImage @AppId=?, @ImageType=?, @ImageName=?, @ImageLink=?, @UpdatedBy=?, @ImageId=?'
    queryParams = ( request.AppId, request.ImageType, request.ImageName, request.ImageLink, request.updatedBy, request.ImageId)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)

@router.delete('')
async def appImageDelete(UpdatedBy: int, ImageId: int, ActiveStatus: str,db:Cursor = Depends(get_cursor)):
    query = 'EXEC deleteAppImage @UpdatedBy=?, @ImageId=?, @ActiveStatus=?'
    queryParams = (  UpdatedBy, ImageId, ActiveStatus)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)




