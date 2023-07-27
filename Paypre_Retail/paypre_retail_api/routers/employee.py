from fastapi.routing import APIRouter
from schemas import PostEmployee,PutEmployee
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from typing import Tuple,Dict
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete

router = APIRouter(prefix='/employee', tags=['Employee'])

@router.get('')
async def employeeGet(UniqueId:Optional[int] = Query(None), ActiveStatus:Optional[str] = Query(None), CompId:Optional[int] = Query(None), BranchId:Optional[int] =Query(None), db:Cursor= Depends(get_cursor))->Dict:
    query :str = 'EXEC getEmployee @UniqueId=?, @ActiveStatus=?, @CompId=?, @BranchId=?'
    queryParams :Tuple = ( UniqueId, ActiveStatus, CompId, BranchId)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)


@router.post('')
async def employeePost(request:PostEmployee, db:Cursor= Depends(get_cursor))->Dict:
    query :str= f"""EXEC postEmployee @UserId=?, @CompId=?, @BranchId=?,@EmpFirstName=?, @EmpLastName=?, @EmpType=?, @EmpDesig=?, @EmpDept=?,
        @EmpDOJ=?, @EmpPhotoLink=?, @RoleId=?, @EmpShiftId=?, @MobileAppAccess=?, @CreatedBy=?, @Address1=?, @Address2=?, @Zip=?, @City=?, @Dist=?, @State=?,
        @Latitude=?, @Longitude=?"""
    queryParams :Tuple = ( request.UserId, request.CompId, request.BranchId, request.EmpFirstName, request.EmpLastName, request.EmpType, request.EmpDesig,
        request.EmpDept, request.EmpDOJ, request.EmpPhotoLink, request.RoleId, request.EmpShiftId, request.MobileAppAccess, request.CreatedBy, request.Address1, request.Address2, request.Zip,
        request.City, request.Dist, request.State, request.Latitude, request.Longitude)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPost)
    
@router.put('')
async def employeePut(request: PutEmployee, db:Cursor = Depends(get_cursor))->Dict:
    query :str = f"""EXEC putEmployee @UserId=?, @CompId=?, @BranchId=?, @EmpCode=?,@EmpFirstName=?, @EmpLastName=?, @EmpType=?, @EmpDesig=?, @EmpDept=?,
        @EmpDOJ=?, @EmpPhotoLink=?, @RoleId=?, @EmpShiftId=?, @MobileAppAccess=?, @UpdatedBy=?, @Address1=?, @Address2=?, @Zip=?, @City=?, @Dist=?, @State=?,
        @Latitude=?, @Longitude=?, @AddId=?, @UniqueId=?"""
    queryParams :Tuple = ( request.UserId, request.CompId, request.BranchId, request.EmpCode, request.EmpFirstName, request.EmpLastName, request.EmpType, request.EmpDesig,
        request.EmpDept, request.EmpDOJ, request.EmpPhotoLink, request.RoleId, request.EmpShiftId, request.MobileAppAccess, request.UpdatedBy, request.Address1, request.Address2, request.Zip,
        request.City, request.Dist, request.State, request.Latitude, request.Longitude, request.AddId, request.UniqueId)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)
    
@router.delete('')
async def employeeDelete(UniqueId: int, ActiveStatus: str, UpdatedBy: int,db:Cursor = Depends(get_cursor))->Dict:
    query :str = 'EXEC deleteEmployee @UniqueId=?, @ActiveStatus=?, @UpdatedBy=?'
    queryParams :Tuple = (  UniqueId, ActiveStatus, UpdatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)