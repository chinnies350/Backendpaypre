from fastapi.routing import APIRouter
from schemas import PostSettings,PutSettings
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from typing import Tuple,Dict
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete

router = APIRouter(prefix='/settings', tags=['Settings'])



@router.get('')
async def settingsGet(UniqueId:Optional[int] = Query(None), ActiveStatus:Optional[str] = Query(None), CompId:Optional[int] = Query(None), BranchId:Optional[int] =Query(None), SettingId:Optional[int] =Query(None), db:Cursor= Depends(get_cursor))->Dict:
    query :str = 'EXEC getSettings @UniqueId=?, @ActiveStatus=?, @CompId=?, @BranchId=?, @SettingId=?'
    queryParams :Tuple = ( UniqueId, ActiveStatus, CompId, BranchId, SettingId)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)

@router.post('')
async def settingsPost(request:PostSettings, db:Cursor= Depends(get_cursor))->Dict:
    query :str= 'EXEC postSettings @CompId=?, @BranchId=?, @SettingId=?, @SettingValue=?, @Comments=?, @CreatedBy=?'
    queryParams :Tuple = ( request.CompId, request.BranchId, request.SettingId, request.SettingValue, request.Comments, request.CreatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPost)
    
@router.put('')
async def settingsPut(request: PutSettings, db:Cursor = Depends(get_cursor))->Dict:
    query :str = 'EXEC putSettings @CompId=?, @BranchId=?, @SettingId=?, @SettingValue=?, @Comments=?, @UpdatedBy=?, @UniqueId=?'
    queryParams :Tuple = ( request.CompId, request.BranchId, request.SettingId, request.SettingValue, request.Comments, request.UpdatedBy, request.UniqueId)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)
    
@router.delete('')
async def settingsDelete(UniqueId: int, ActiveStatus: str, UpdatedBy: int,db:Cursor = Depends(get_cursor))->Dict:
    query :str = 'EXEC deleteSettings @UniqueId=?, @ActiveStatus=?, @UpdatedBy=?'
    queryParams :Tuple = (  UniqueId, ActiveStatus, UpdatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)