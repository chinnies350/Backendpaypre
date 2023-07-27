from fastapi.routing import APIRouter
from schemas import PostComboHdr,PutEmpAccess
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from typing import Tuple,Dict, List
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureTrans,ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete
import json
from joblib import Parallel, delayed

router = APIRouter(prefix='/comboHdr', tags=['ComboHdr'])

def callFunction(i):
    return i.dict()



@router.get('')
async def comboHdrGet(ComboId:Optional[int] = Query(None), ActiveStatus:Optional[str] = Query(None), CompId:Optional[int] = Query(None), BranchId:Optional[int] = Query(None) ,db:Cursor= Depends(get_cursor))->Dict:
    query :str = 'EXEC getComboHdr @ComboId=?, @ActiveStatus=?, @CompId=?, @BranchId=?'
    queryParams :Tuple = ( ComboId, ActiveStatus, CompId, BranchId)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)

@router.post('')
async def comboHdrPost(request:PostComboHdr, db:Cursor= Depends(get_cursor))-> Dict:
    query :str= f"""EXEC postComboHdr @CompId=?, @BranchId=?, @OfferPrice=?, @ValidFrom=?, @ValidTo=?, @CreatedBy=?, @ComboDtlDetails=?"""
    
    def transformFunction(request:PostComboHdr):
        ComboDtlDetails: str | None | List = None
        
        if request.ComboDtlDetails != None:
            ComboDtlDetails = Parallel(
                n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.ComboDtlDetails)
            ComboDtlDetails = json.dumps(ComboDtlDetails,indent=4, sort_keys=True, default=str)
        else:
            ComboDtlDetails = None
        return (request.CompId, request.BranchId, request.OfferPrice, request.ValidFrom, request.ValidTo, request.CreatedBy, ComboDtlDetails)

    return await ApiWithProcedureTrans(db=db, 
                                    query=query,
                                    request=request, 
                                    transformParam=transformFunction, 
                                    additionalFunction=additionalFunctionPost)
    
@router.delete('')
async def comboHdrDelete(ComboId: int, ActiveStatus: str, UpdatedBy: int,db:Cursor = Depends(get_cursor))->Dict:
    query :str = 'EXEC deleteComboHdr @ComboId=?, @ActiveStatus=?, @UpdatedBy=?'
    queryParams :Tuple = (  ComboId, ActiveStatus, UpdatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)