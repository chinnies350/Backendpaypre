from fastapi.routing import APIRouter
from schemas import PostBranch,PutBranch
from aioodbc.cursor import Cursor
from routers.config import get_cursor,logs_collection
from fastapi import Depends
from typing import Optional
from fastapi import Query
import datetime
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete


router = APIRouter(prefix='/branch', tags=['Branch'])

def insert_log(user_id, message):
    log_entry = {
        'timestamp': datetime.datetime.utcnow(),
        'user_id': user_id,
        'message': message
    }

    logs_collection.insert_one(log_entry)

@router.get('')
async def branchGet(BrId:Optional[int] = Query(None), ActiveStatus:Optional[str] = Query(None),CompId:Optional[int] = Query(None), UserId:Optional[int] = Query(None),db:Cursor= Depends(get_cursor)):
    query = 'EXEC getBranch @BrId=?, @ActiveStatus=?,@CompId=?, @UserId=?'
    queryParams = ( BrId, ActiveStatus,CompId, UserId)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)


@router.post('')
async def branchPost(request: PostBranch, db:Cursor= Depends(get_cursor)):
    query = f"""EXEC postBranch @CompId=?, @BrName=?, @BrShName=?, @BrGSTIN=?, @BrInCharge=?, @BrMobile=?,@BrEmail=?,
        @BrRegnNo=?, @WorkingFrom=?, @WorkingTo=?, @CreatedBy=?, @Address1=?, @Address2=?, @Zip=?, @City=?, @Dist=?, @State=?, @Latitude=?, @Longitude=?, @AppId=?, @UserId=?"""
    queryParams = (  request.CompId, request.BrName, request.BrShName, request.BrGSTIN, request.BrInCharge, request.BrMobile, request.BrEmail,
        request.BrRegnNo, request.WorkingFrom, request.WorkingTo, request.CreatedBy, request.Address1, request.Address2, request.Zip, request.City, request.Dist, request.State, request.Latitude, request.Longitude, request.AppId, request.UserId)
    
    def manipulatePostResponse(res):
        if res[0][1] == 1:
            insert_log(request.UserId, f"{request.BrName} branch created by {res[0][2]}")
        return additionalFunctionPost(res)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=manipulatePostResponse)
    
    
    
@router.put('')
async def branchPut(request: PutBranch, db:Cursor = Depends(get_cursor)):
    query = f"""EXEC putBranch @CompId=?, @BrName=?, @BrShName=?, @BrGSTIN=?, @BrInCharge=?, @BrMobile=?,@BrEmail=?,
        @BrRegnNo=?, @WorkingFrom=?, @WorkingTo=?, @UpdatedBy=?, @Address1=?, @Address2=?, @Zip=?, @City=?, @Dist=?, @State=?, @Latitude=?, @Longitude=?, @BrId=?, @AddId=?"""
    queryParams = ( request.CompId, request.BrName, request.BrShName, request.BrGSTIN, request.BrInCharge, request.BrMobile, request.BrEmail,
        request.BrRegnNo, request.WorkingFrom, request.WorkingTo, request.UpdatedBy, request.Address1, request.Address2, request.Zip, request.City, request.Dist, request.State, request.Latitude, request.Longitude, request.BrId, request.AddId)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)
    
@router.delete('')
async def branchdelete(BrId: int, ActiveStatus: str, UpdatedBy: int, db:Cursor = Depends(get_cursor)):
    query = 'EXEC deleteBranch @BrId=?, @ActiveStatus=?, @UpdatedBy=?'
    queryParams = (  BrId, ActiveStatus, UpdatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)