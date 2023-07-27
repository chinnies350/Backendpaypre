from fastapi.routing import APIRouter
from schemas import PostCompany,PutCompany
from aioodbc.cursor import Cursor
from routers.config import get_cursor,logs_collection
from fastapi import Depends
from typing import Optional
from fastapi import Query
import datetime
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete


router = APIRouter(prefix='/company', tags=['Company'])

def insert_log(user_id, message):
    log_entry = {
        'timestamp': datetime.datetime.utcnow(),
        'user_id': user_id,
        'message': message
    }

    logs_collection.insert_one(log_entry)

@router.get('')
async def companyGet(CompId:Optional[int] = Query(None), ActiveStatus:Optional[str] = Query(None), Type:Optional[str] = Query(None),UserId:Optional[int] = Query(None), db:Cursor= Depends(get_cursor)):
    query = 'EXEC getCompany @CompId=?, @ActiveStatus=?, @Type=?,@UserId=?'
    queryParams = ( CompId, ActiveStatus, Type,UserId)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)
    


@router.post('')
async def companyPost(request: PostCompany, db:Cursor= Depends(get_cursor)):
    query = f"""EXEC postCompany @CompName=?, @CompShName=?, @BusiBrief=?, @CompLogo=?, @CompGSTIN=?, @Proprietor=?,
        @CompPOC=?, @CompMobile=?, @CompEmail=?, @CompRegnNo=?, @CreatedBy=?, @Address1=?, @Address2=?, @Zip=?, @City=?, @Dist=?, @State=?, @Latitude=?, @Longitude=?, @UserId=?, @AppId=?"""
    queryParams = (  request.CompName, request.CompShName, request.BusiBrief, request.CompLogo, request.CompGSTIN, request.Proprietor,
        request.CompPOC, request.CompMobile, request.CompEmail, request.CompRegnNo, request.CreatedBy, request.Address1, request.Address2, request.Zip, request.City, request.Dist, request.State, request.Latitude, request.Longitude, request.UserId, request.AppId)

    def manipulatePostResponse(res):
        if res[0][1] == 1:
            insert_log(request.UserId, f"{request.CompName} organization created by {res[0][2]}")
        return additionalFunctionPost(res)
    
    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=manipulatePostResponse)
    
    
@router.put('')
async def companyPut(request: PutCompany, db:Cursor = Depends(get_cursor)):
    query = f"""EXEC putCompany @CompName=?, @CompShName=?, @BusiBrief=?, @CompLogo=?, @CompAddId=?, @CompGSTIN=?, @Proprietor=?,
        @CompPOC=?, @CompMobile=?, @CompEmail=?, @CompRegnNo=?, @UpdatedBy=?, @Address1=?, @Address2=?, @Zip=?, @City=?, @Dist=?, @State=?, @Latitude=?, @Longitude=?, @AddId=?, @CompId=?"""
    queryParams = ( request.CompName, request.CompShName, request.BusiBrief, request.CompLogo, request.CompAddId, request.CompGSTIN, request.Proprietor,
        request.CompPOC, request.CompMobile, request.CompEmail, request.CompRegnNo, request.UpdatedBy, request.Address1, request.Address2, request.Zip, request.City, request.Dist, request.State, request.Latitude, request.Longitude, request.AddId, request.CompId)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)

    
@router.delete('')
async def companydelete(CompId: int, ActiveStatus: str, UpdatedBy: int, db:Cursor = Depends(get_cursor)):
    query = 'EXEC deleteCompany @CompId=?, @ActiveStatus=?, @UpdatedBy=?'
    queryParams = (  CompId, ActiveStatus, UpdatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)

