from fastapi.routing import APIRouter
from schemas import PostFeature, PutFeature
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from routers.utils.apiCommon import ApiWithProcedureGet

router = APIRouter(prefix='/FeatureMapping', tags=['FeatureMapping'])

@router.get('')
async def featureMappingGet(AppId:Optional[int]=Query(None), Type:Optional[str]=Query(None), db:Cursor= Depends(get_cursor)):
    query = 'EXEC GetFEatureMapping @AppId=?,@Type=?'
    queryParams = ( AppId,Type)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)