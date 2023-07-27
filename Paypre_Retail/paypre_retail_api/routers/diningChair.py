from fastapi.routing import APIRouter
from schemas import PostDiningChair,PutDiningChair
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from typing import Tuple,Dict
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete

router = APIRouter(prefix='/diningChair', tags=['DiningChair'])


@router.get('')
async def diningChairGet(TableId:Optional[int] = Query(None), ActiveStatus:Optional[str] = Query(None), CompId:Optional[int] = Query(None), BranchId:Optional[int] = Query(None), ChairId:Optional[int] = Query(None) ,db:Cursor= Depends(get_cursor))->Dict:
    query :str = 'EXEC getDiningChair @TableId=?, @ActiveStatus=?, @CompId=?, @BranchId=?, @ChairId=?'
    queryParams :Tuple = ( TableId, ActiveStatus, CompId, BranchId, ChairId)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)


@router.post('')
async def diningChairPost(request:PostDiningChair, db:Cursor= Depends(get_cursor))->Dict:
    query :str= 'EXEC postDiningChair @CompId=?, @BranchId=?, @TableId=?, @ChairName=?, @CreatedBy=?'
    queryParams :Tuple = ( request.CompId, request.BranchId, request.TableId, request.ChairName, request.CreatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPost)
    
@router.put('')
async def diningChairPut(request: PutDiningChair, db:Cursor = Depends(get_cursor))->Dict:
    query :str = 'EXEC putDiningChair @CompId=?, @BranchId=?, @ChairName=?, @UpdatedBy=?, @TableId=?, @ChairId=?'
    queryParams :Tuple = ( request.CompId, request.BranchId, request.ChairName, request.UpdatedBy, request.TableId, request.ChairId)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)
    
@router.delete('')
async def diningChairDelete(ChairId: int, ActiveStatus: str, UpdatedBy: int,db:Cursor = Depends(get_cursor))->Dict:
    query :str = 'EXEC deleteDiningChair @ChairId=?, @ActiveStatus=?, @UpdatedBy=?'
    queryParams :Tuple = (  ChairId, ActiveStatus, UpdatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)