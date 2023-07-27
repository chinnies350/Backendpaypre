from fastapi.routing import APIRouter
from schemas import PostEmpAccess,PutEmpAccess
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from typing import Tuple,Dict, List
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureTrans,ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete
import json
from joblib import Parallel, delayed

router = APIRouter(prefix='/empAccess', tags=['EmpAccess'])

def callFunction(i):
    return i.dict()

@router.get('')
async def empAccessGet(AccessId:Optional[int] = Query(None), ActiveStatus:Optional[str] = Query(None), CompId:Optional[int] = Query(None), BranchId:Optional[int] =Query(None), EmpId:Optional[int] =Query(None), AppId:Optional[int] =Query(None), db:Cursor= Depends(get_cursor))->Dict:
    query :str = 'EXEC getEmpAccess @AccessId=?, @ActiveStatus=?, @CompId=?, @BranchId=?, @EmpId=?, @AppId=?'
    queryParams :Tuple = ( AccessId, ActiveStatus, CompId, BranchId, EmpId, AppId)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)



@router.post('')
async def empAccessPost(request:PostEmpAccess, db:Cursor= Depends(get_cursor))-> Dict:
    query :str= f"""EXEC postEmpAccess @EmpId=?, @CompId=?, @BranchId=?, @AppId=?, @CreatedBy=?, @EmpAccessDetails=?"""
    
    def transformFunction(request:PostEmpAccess):
        EmpAccessDetails: str | None | List = None
        
        if request.EmpAccessDetails != None:
            EmpAccessDetails = Parallel(
                n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.EmpAccessDetails)
            EmpAccessDetails = json.dumps(EmpAccessDetails,indent=4, sort_keys=True, default=str)
        else:
            EmpAccessDetails = None
        return (request.EmpId, request.CompId, request.BranchId, request.AppId, request.CreatedBy, EmpAccessDetails)
    # queryParams :Tuple = ( request.EmpId, request.CompId, request.BranchId, request.AppId, request.CreatedBy,request.EmpAccessDetails)
    return await ApiWithProcedureTrans(db=db, 
                                    query=query,
                                    request=request, 
                                    transformParam=transformFunction, 
                                    additionalFunction=additionalFunctionPost)
    
@router.put('')
async def empAccessPut(request:PutEmpAccess, db:Cursor= Depends(get_cursor))-> Dict:
    query :str= f"""EXEC putEmpAccess @EmpId=?, @CompId=?, @BranchId=?, @AppId=?, @UpdatedBy=?, @EmpAccessDetails=?"""
    
    def transformFunction(request:PutEmpAccess):
        EmpAccessDetails: str | None | List = None
        
        if request.EmpAccessDetails != None:
            EmpAccessDetails = Parallel(
                n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.EmpAccessDetails)
            EmpAccessDetails = json.dumps(EmpAccessDetails,indent=4, sort_keys=True, default=str)
        else:
            EmpAccessDetails = None
        return (request.EmpId, request.CompId, request.BranchId, request.AppId, request.UpdatedBy, EmpAccessDetails)
    return await ApiWithProcedureTrans(db=db, 
                                    query=query,
                                    request=request, 
                                    transformParam=transformFunction, 
                                    additionalFunction=additionalFunctionPut)
    
    
    
@router.delete('')
async def empAccessDelete(AccessId: int, ActiveStatus: str, UpdatedBy: int,db:Cursor = Depends(get_cursor))->Dict:
    query :str = 'EXEC deleteEmpAccess @AccessId=?, @ActiveStatus=?, @UpdatedBy=?'
    queryParams :Tuple = (  AccessId, ActiveStatus, UpdatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)