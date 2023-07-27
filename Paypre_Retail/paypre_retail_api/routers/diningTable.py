from fastapi.routing import APIRouter
from schemas import PostDiningTable,PutDiningTable
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from typing import Tuple,Dict
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete

router = APIRouter(prefix='/diningTable', tags=['DiningTable'])

@router.get('')
async def diningTableGet(TableId:Optional[int] = Query(None), ActiveStatus:Optional[str] = Query(None), CompId:Optional[int] = Query(None), BranchId:Optional[int] = Query(None), DineInType:Optional[int] = Query(None) ,db:Cursor= Depends(get_cursor))->Dict:
    query :str = 'EXEC getDiningTable @TableId=?, @ActiveStatus=?, @CompId=?, @BranchId=?, @DineInType=?'
    queryParams :Tuple = ( TableId, ActiveStatus, CompId, BranchId, DineInType)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)


@router.post('')
async def diningTablePost(request:PostDiningTable, db:Cursor= Depends(get_cursor))->Dict:
    query :str= 'EXEC postDiningTable @CompId=?, @BranchId=?, @TableName=?, @ChairCount=?, @ChairLevelSer=?, @DineInType=?, @CreatedBy=?'
    queryParams :Tuple = ( request.CompId, request.BranchId, request.TableName, request.ChairCount, request.ChairLevelSer, request.DineInType, request.CreatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPost)
    
@router.put('')
async def diningTablePut(request: PutDiningTable, db:Cursor = Depends(get_cursor))->Dict:
    query :str = 'EXEC putDiningTable @CompId=?, @BranchId=?, @TableName=?, @ChairCount=?, @ChairLevelSer=?, @DineInType=?, @UpdatedBy=?, @TableId=?'
    queryParams :Tuple = ( request.CompId, request.BranchId, request.TableName, request.ChairCount, request.ChairLevelSer, request.DineInType, request.UpdatedBy, request.TableId)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)
    
@router.delete('')
async def diningTableDelete(TableId: int, ActiveStatus: str, UpdatedBy: int,db:Cursor = Depends(get_cursor))->Dict:
    query :str = 'EXEC deleteDiningTable @TableId=?, @ActiveStatus=?, @UpdatedBy=?'
    queryParams :Tuple = (  TableId, ActiveStatus, UpdatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)