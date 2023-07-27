from fastapi.routing import APIRouter
from schemas import PostCustomer,PutCustomer
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from typing import Tuple,Dict
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete

router = APIRouter(prefix='/customer', tags=['Customer'])

@router.get('')
async def customerGet(CustId:Optional[int] = Query(None), ActiveStatus:Optional[str] = Query(None), CompId:Optional[int] = Query(None), BranchId:Optional[int] = Query(None),db:Cursor= Depends(get_cursor))->Dict:
    query :str = 'EXEC getCustomer @CustId=?, @ActiveStatus=?, @CompId=?, @BranchId=?'
    queryParams :Tuple = ( CustId, ActiveStatus, CompId, BranchId)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)

@router.post('')
async def customerPost(request:PostCustomer, db:Cursor= Depends(get_cursor))->Dict:
    query :str= f"""EXEC postCustomer @UserId=?, @CompId=?, @BranchId=?, @CustName=?, @CustGSTIN=?, @CustMobile=?, @CustEmail=?, @CreatedBy=?,
        @Address1=?, @Address2=?, @Zip=?, @City=?, @Dist=?, @State=?, @Latitude=?, @Longitude=?"""
    queryParams :Tuple = ( request.UserId, request.CompId, request.BranchId, request.CustName, request.CustGSTIN, request.CustMobile, request.CustEmail, request.CreatedBy,
        request.Address1, request.Address2, request.Zip, request.City, request.Dist, request.State, request.Latitude, request.Longitude)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPost)
    
    
@router.put('')
async def customerPut(request:PutCustomer, db:Cursor= Depends(get_cursor))->Dict:
    query :str= f"""EXEC putCustomer @UserId=?, @CompId=?, @BranchId=?, @CustName=?, @CustGSTIN=?, @CustMobile=?, @CustEmail=?, @UpdatedBy=?,
        @Address1=?, @Address2=?, @Zip=?, @City=?, @Dist=?, @State=?, @Latitude=?, @Longitude=?, @AddId=?, @CustId=?"""
    queryParams :Tuple = ( request.UserId, request.CompId, request.BranchId, request.CustName, request.CustGSTIN, request.CustMobile, request.CustEmail, request.UpdatedBy,
        request.Address1, request.Address2, request.Zip, request.City, request.Dist, request.State, request.Latitude, request.Longitude, request.AddId, request.CustId)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)
    
@router.delete('')
async def customerDelete(CustId: int, ActiveStatus: str, UpdatedBy: int,db:Cursor = Depends(get_cursor))->Dict:
    query :str = 'EXEC deleteCustomer @CustId=?, @ActiveStatus=?, @UpdatedBy=?'
    queryParams :Tuple = (  CustId, ActiveStatus, UpdatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)
    
