from fastapi.routing import APIRouter
from schemas import PostSupplier,PutSupplier
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from typing import Tuple,Dict
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete

router = APIRouter(prefix='/supplier', tags=['Supplier'])

@router.get('')
async def supplierGet(SuppId:Optional[int] = Query(None), ActiveStatus:Optional[str] = Query(None), CompId:Optional[int] = Query(None), BranchId:Optional[int] = Query(None), db:Cursor= Depends(get_cursor))->Dict:
    query :str = 'EXEC getSupplier @SuppId=?, @ActiveStatus=?, @CompId=?, @BranchId=?'
    queryParams :Tuple = ( SuppId, ActiveStatus, CompId, BranchId)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)

@router.post('')
async def supplierPost(request:PostSupplier, db:Cursor= Depends(get_cursor))->Dict:
    query :str= f"""EXEC postSuppiler @CompId=?, @BranchId=?, @SuppName=?, @SuppGSTIN=?, @SuppPOC=?, @SuppMobile=?, @SuppEmail=?, @CreatedBy=?,
        @Address1=?, @Address2=?, @Zip=?, @City=?, @Dist=?, @State=?, @Latitude=?, @Longitude=?"""
    queryParams :Tuple = ( request.CompId, request.BranchId, request.SuppName, request.SuppGSTIN, request.SuppPOC, request.SuppMobile, request.SuppEmail, request.CreatedBy,
        request.Address1, request.Address2, request.Zip, request.City, request.Dist, request.State, request.Latitude, request.Longitude)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPost)
    
@router.put('')
async def supplierPut(request: PutSupplier, db:Cursor = Depends(get_cursor))->Dict:
    query :str = f"""EXEC putSupplier @CompId=?, @BranchId=?, @SuppName=?, @SuppGSTIN=?, @SuppPOC=?, @SuppMobile=?, @SuppEmail=?, @UpdatedBy=?,
        @Address1=?, @Address2=?, @Zip=?, @City=?, @Dist=?, @State=?, @Latitude=?, @Longitude=?, @AddId=?, @SuppId=?"""
    queryParams :Tuple = ( request.CompId, request.BranchId, request.SuppName, request.SuppGSTIN, request.SuppPOC, request.SuppMobile, request.SuppEmail, request.UpdatedBy,
        request.Address1, request.Address2, request.Zip, request.City, request.Dist, request.State, request.Latitude, request.Longitude, request.AddId, request.SuppId)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)
    
@router.delete('')
async def supplierDelete(SuppId: int, ActiveStatus: str, UpdatedBy: int,db:Cursor = Depends(get_cursor))->Dict:
    query :str = 'EXEC deleteSupplier @SuppId=?, @ActiveStatus=?, @UpdatedBy=?'
    queryParams :Tuple = (  SuppId, ActiveStatus, UpdatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)