from fastapi.routing import APIRouter
from schemas import PostInwardHdr
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from typing import Tuple,Dict, List
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureTrans,ApiWithProcedureGet,additionalFunctionPost, additionalFunctionDelete
import json
from joblib import Parallel, delayed

router = APIRouter(prefix='/inwardHdr', tags=['InwardHdr'])

def callFunction(i):
    return i.dict()


@router.get('')
async def inwardHdrGet(InwardId:Optional[int] = Query(None), ActiveStatus:Optional[str] = Query(None), CompId:Optional[int] = Query(None), BranchId:Optional[int] =Query(None), SuppId:Optional[int] =Query(None), db:Cursor= Depends(get_cursor))->Dict:
    query :str = 'EXEC getInwardHdr @InwardId=?, @ActiveStatus=?, @CompId=?, @BranchId=?, @SuppId=?'
    queryParams :Tuple = ( InwardId, ActiveStatus, CompId, BranchId, SuppId)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)
    
@router.post('')
async def inwardHdrPost(request:PostInwardHdr, db:Cursor= Depends(get_cursor))-> Dict:
    query :str= f"""EXEC postInwardHdr @CompId=?, @BranchId=?, @InwardDate=?, @SuppId=?, @Reference=?, @CreatedBy=?, @InwardDtlDetails=?"""
    
    def transformFunction(request:PostInwardHdr):
        InwardDtlDetails: str | None | List = None
        
        if request.InwardDtlDetails != None:
            InwardDtlDetails = Parallel(
                n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.InwardDtlDetails)
            InwardDtlDetails = json.dumps(InwardDtlDetails,indent=4, sort_keys=True, default=str)
        else:
            InwardDtlDetails = None
        return (request.CompId, request.BranchId, request.InwardDate, request.SuppId, request.Reference, request.CreatedBy, InwardDtlDetails)

    return await ApiWithProcedureTrans(db=db, 
                                    query=query,
                                    request=request, 
                                    transformParam=transformFunction, 
                                    additionalFunction=additionalFunctionPost)
    
    
@router.delete('')
async def inwardHdrDelete(InwardId: int, ActiveStatus: str, UpdatedBy: int,db:Cursor = Depends(get_cursor))->Dict:
    query :str = 'EXEC deleteInwardHdr @InwardId=?, @ActiveStatus=?, @UpdatedBy=?'
    queryParams :Tuple = (  InwardId, ActiveStatus, UpdatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)