from fastapi.routing import APIRouter
from schemas import PostShift,PutShift
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from typing import Tuple,Dict
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete

router = APIRouter(prefix='/shift', tags=['Shift'])


@router.get('')
async def shiftGet(ShiftId:Optional[int] = Query(None), ActiveStatus:Optional[str] = Query(None), CompId:Optional[int] = Query(None), db:Cursor= Depends(get_cursor))->Dict:
    query :str = 'EXEC getShift @ShiftId=?, @ActiveStatus=?, @CompId=?'
    queryParams :Tuple = ( ShiftId, ActiveStatus, CompId)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)


@router.post('')
async def shiftPost(request:PostShift, db:Cursor= Depends(get_cursor))->Dict:
    query :str= 'EXEC postShift @CompId=?, @ShiftName=?, @StartTime=?, @EndTime=?, @BreakStartTime=?, @BreakEndTime=?, @GracePeriod=?, @CreatedBy=?'
    queryParams :Tuple = ( request.CompId, request.ShiftName, request.StartTime, request.EndTime, request.BreakStartTime, request.BreakEndTime, request.GracePeriod, request.CreatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPost)
    
@router.put('')
async def shiftPut(request: PutShift, db:Cursor = Depends(get_cursor))->Dict:
    query :str = 'EXEC putShift @CompId=?, @ShiftName=?, @StartTime=?, @EndTime=?, @BreakStartTime=?, @BreakEndTime=?, @GracePeriod=?, @UpdatedBy=?, @ShiftId=?'
    queryParams :Tuple = ( request.CompId, request.ShiftName, request.StartTime, request.EndTime, request.BreakStartTime, request.BreakEndTime, request.GracePeriod, request.UpdatedBy, request.ShiftId)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)
    
@router.delete('')
async def shiftDelete(ShiftId: int, ActiveStatus: str, UpdatedBy: int,db:Cursor = Depends(get_cursor))->Dict:
    query :str = 'EXEC deleteShift @ShiftId=?, @ActiveStatus=?, @UpdatedBy=?'
    queryParams :Tuple = (  ShiftId, ActiveStatus, UpdatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)