from fastapi.routing import APIRouter
from schemas import PostConfigMaster,PutConfigMaster
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from typing import Tuple,Dict
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete

router = APIRouter(prefix='/configMaster', tags=['ConfigMaster'])


@router.get('')
async def configMasterGet(TypeId:Optional[int] = Query(None), ActiveStatus:Optional[str] = Query(None), TypeName: Optional[str]=Query(None), ConfigId:Optional[int]=Query(None), db:Cursor= Depends(get_cursor))->Dict:
    query :str = 'EXEC getConfigMaster @ConfigId=?, @TypeId, @ActiveStatus=?, @TypeName=?'
    queryParams :Tuple = ( ConfigId, TypeId, ActiveStatus, TypeName )

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)

@router.post('')
async def configMasterPost(request: PostConfigMaster, db:Cursor= Depends(get_cursor))->Dict:
    query :str = 'EXEC postConfigMaster @TypeId=?, @ConfigName=?, @AlphaNumFld=?, @NumFld=?, @CreatedBy=?'
    queryParams :Tuple = (  request.TypeId, request.ConfigName, request.AlphaNumFld, request.NumFld, request.CreatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPost)
    
@router.put('')
async def configMasterPut(request: PutConfigMaster, db:Cursor = Depends(get_cursor))->Dict:
    query :str= 'EXEC putConfigMaster @TypeId=?, @ConfigName=?, @AlphaNumFld=?, @NumFld=?, @UpdatedBy=?, @ConfigId=?'
    queryParams :Tuple = ( request.TypeId, request.ConfigName, request.AlphaNumFld, request.NumFld, request.UpdatedBy, request.ConfigId)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)
    
@router.delete('')
async def configMasterPut(UpdatedBy: int, ConfigId: int, ActiveStatus: str,db:Cursor = Depends(get_cursor))->Dict:
    query :str = 'EXEC deleteConfigMaster @UpdatedBy=?, @ConfigId=?, @ActiveStatus=?'
    queryParams :Tuple = (  UpdatedBy, ConfigId, ActiveStatus)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)