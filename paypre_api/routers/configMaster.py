from fastapi.routing import APIRouter
from schemas import PostConfigMaster, PutConfigMaster,PostBulkUpload
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Tuple,Dict, List,Optional
from fastapi import Query
import json
from joblib import Parallel, delayed
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete,ApiWithProcedureTrans



router = APIRouter(prefix='/configMaster', tags=['ConfigMaster'])

def callFunction(i):
    return i.dict()

@router.get('')
async def configMasterGet(TypeId:Optional[int] = Query(None), ActiveStatus:Optional[str] = Query(None), TypeName: Optional[str]=Query(None), ConfigId:Optional[int]=Query(None), db:Cursor= Depends(get_cursor)):
    query = 'EXEC getConfigMaster @TypeId=?, @ActiveStatus=?, @TypeName=?, @ConfigId=?'
    queryParams = ( TypeId, ActiveStatus, TypeName, ConfigId)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)

@router.post('')
async def configMasterPost(request: PostConfigMaster, db:Cursor= Depends(get_cursor)):
    query = 'EXEC postConfigMaster @TypeId=?, @ConfigName=?, @AlphaNumFld=?, @NumFld=?, @SmallIcon=?, @CreatedBy=?'
    queryParams = (  request.TypeId, request.ConfigName, request.AlphaNumFld, request.NumFld, request.SmallIcon, request.CreatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPost)

@router.put('')
async def configMasterPut(request: PutConfigMaster, db:Cursor = Depends(get_cursor)):
    query = 'EXEC putConfigMaster @TypeId=?, @ConfigName=?, @AlphaNumFld=?, @NumFld=?, @SmallIcon=?, @UpdatedBy=?, @ConfigId=?'
    queryParams = ( request.TypeId, request.ConfigName, request.AlphaNumFld, request.NumFld, request.SmallIcon, request.UpdatedBy, request.ConfigId)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)

@router.delete('')
async def configMasterPut(UpdatedBy: int, ConfigId: int, ActiveStatus: str,db:Cursor = Depends(get_cursor)):
    query = 'EXEC deleteConfigMaster @UpdatedBy=?, @ConfigId=?, @ActiveStatus=?'
    queryParams = (  UpdatedBy, ConfigId, ActiveStatus)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)
    
# @router.post('/BulkUpload')
# async def BulkUploadPost(request:PostBulkUpload, db:Cursor= Depends(get_cursor))-> Dict:
#     query :str= f"""EXEC postBulkUpload @configMasterDetailsJson=?"""
    
#     def transformFunction(request:PostBulkUpload):
#         ConfigMasterDetails: str | None | List = None
        
#         if request.ConfigMasterDetails != None:
#             ConfigMasterDetails = Parallel(
#                 n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.ConfigMasterDetails)
#             ConfigMasterDetails = json.dumps(ConfigMasterDetails,indent=4, sort_keys=True, default=str)
#         else:
#             ConfigMasterDetails = None
#         return (ConfigMasterDetails)
#     # queryParams :Tuple = ( request.EmpId, request.CompId, request.BranchId, request.AppId, request.CreatedBy,request.EmpAccessDetails)
#     return await ApiWithProcedureTrans(db=db, 
#                                     query=query,
#                                     request=request, 
#                                     transformParam=transformFunction, 
#                                     additionalFunction=additionalFunctionPost)

@router.post('/BulkUpload')
async def BulkUploadPost(request: PostBulkUpload, db: Cursor = Depends(get_cursor)) -> Dict:
    query: str = "EXEC PostBulkUpload @configMasterDetailsJson=?"
    def transformFunction(request: PostBulkUpload) -> Tuple:
        formattedData = []
        if request.ConfigMasterDetails:
         configDetails = list(set([(data.TypeId, data.ConfigName, data.AlphaNumFld, data.NumFld, data.SmallIcon) for data in request.ConfigMasterDetails]))
         formattedData = [{"TypeId": typeId, "ConfigName": configName, "AlphaNumFld": alphaNumFld, "NumFld": numFld, "SmallIcon": smallIcon} for typeId, configName, alphaNumFld, numFld, smallIcon in configDetails]
        return (json.dumps(formattedData),)

    return await ApiWithProcedureTrans(db=db, 
                                    query=query,
                                    request=request, 
                                    transformParam=transformFunction, 
                                    additionalFunction=additionalFunctionPost)




