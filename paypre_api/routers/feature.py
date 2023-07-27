from fastapi.routing import APIRouter
from schemas import PostFeature, PutFeature
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete



router = APIRouter(prefix='/feature', tags=['Feature'])

@router.get('')
async def featureGet(ActiveStatus:Optional[str]=Query(None), db:Cursor= Depends(get_cursor)):
    query = 'EXEC getFeature @ActiveStatus=?'
    queryParams = ( ActiveStatus)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)

@router.post('')
async def featurePost(request: PostFeature, db:Cursor= Depends(get_cursor)):
    query = 'EXEC postFeature @FeatCat =?, @FeatName =?, @FeatDescription =?, @FeatType =?, @FeatConstraint =?, @CoreAddon =?, @CreatedBy=?'
    queryParams = ( request.FeatCat, request.FeatName, request.FeatDescription, request.FeatType, request.FeatConstraint, request.CoreAddon, request.CreatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPost)

@router.put('')
async def featurePut(request: PutFeature, db:Cursor = Depends(get_cursor)):
    query = 'EXEC putFeature @FeatCat =?, @FeatName =?, @FeatDescription =?, @FeatType =?, @FeatConstraint =?, @CoreAddon =?, @UpdatedBy=?, @FeatId=?'
    queryParams = ( request.FeatCat, request.FeatName, request.FeatDescription, request.FeatType, request.FeatConstraint, request.CoreAddon, request.UpdatedBy, request.FeatId)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)

@router.delete('')
async def featureDelete(UpdatedBy: int, FeatId: int, ActiveStatus: str,db:Cursor = Depends(get_cursor)):
    query = 'EXEC deleteFeature @UpdatedBy=?, @FeatId=?, @ActiveStatus=?'
    queryParams = (  UpdatedBy, FeatId, ActiveStatus)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)




