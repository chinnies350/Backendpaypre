from fastapi.routing import APIRouter
from schemas import PostAppAccess,PutBranchDefault
from aioodbc.cursor import Cursor
from routers.config import get_cursor,logs_collection
from fastapi import Depends
from typing import Optional
from fastapi import Query
from typing import Tuple,Dict, List
import json
from joblib import Parallel, delayed
import datetime
from routers.utils.apiCommon import ApiWithProcedure,ApiWithProcedureTrans, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete




router = APIRouter(prefix='/appAccess', tags=['AppAccess'])                   
def callFunction(i):
    return i.dict()

def insert_log(user_id, message):
    log_entry = {
        'timestamp': datetime.datetime.utcnow(),
        'user_id': user_id,
        'message': message
    }
    
    logs_collection.insert_one(log_entry)

@router.get('')
async def userGet(UserId:Optional[int] = Query(None), AppId:Optional[int] = Query(None), CompId:Optional[int] = Query(None),Type:Optional[str] = Query(None),ActiveStatus:Optional[str] = Query(None), db:Cursor= Depends(get_cursor)):
    query = 'EXEC getAppAccess @UserId=?,@AppId=?,@CompId=?,@Type=?,@ActiveStatus=?'
    queryParams = ( UserId,AppId,CompId,Type,ActiveStatus)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)



@router.post('')
async def postAppAccess(request: PostAppAccess, db:Cursor= Depends(get_cursor)):

    query = 'EXEC postAppAccess @UserId=?,@ModuleDetails =?,@CreatedBy=?'
    
    def transformFunction(request: PostAppAccess) -> Tuple:
        formattedData = []
        if request.ModuleDetails:
            moduleDetails = list(set([(data.AppId, data.CompId, data.BranchId) for data in request.ModuleDetails]))
            formattedData = [{"AppId": appId, "CompId": compId, "BranchId": branchId} for appId, compId, branchId in moduleDetails]
            
        return (request.UserId,json.dumps(formattedData), request.CreatedBy)
        # formattedData = []
        # if request.ModuleDetails:
        #     appIds = list(set([data.AppId for data in request.ModuleDetails]))
        #     formattedData = [{"AppId": AppId} for AppId in appIds]
            
        # return (request.UserId,json.dumps(formattedData), request.CreatedBy)
        
    
    def manipulatePostResponse(res):
        if res[0][1] == 1:
            insert_log(request.UserId, f"User {res[0][2]} Your Appaccess is confirmed")
        return additionalFunctionPost(res)

    
    return await ApiWithProcedureTrans(db=db, 
                                    query=query,
                                    request=request, 
                                    transformParam=transformFunction, 
                                    additionalFunction=manipulatePostResponse)

@router.put('')
async def putDefaultBranch(request: PutBranchDefault, db:Cursor= Depends(get_cursor)):
    query = 'EXEC putDeafaulBranch @DefaultBranch=?, @CompId=?, @BranchId=?,@UserId=?'
    queryParams = ( request.DefaultBranch, request.CompId, request.BranchId,request.UserId)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)


    








