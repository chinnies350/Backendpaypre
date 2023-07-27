from fastapi.routing import APIRouter
from schemas import Forgotpassword
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from routers.utils.apiCommon import ApiWithProcedure, additionalFunctionPut

router = APIRouter(prefix='/forgotpassword', tags=['Forgotpassword'])


@router.put('')
async def forgotpassword(request: Forgotpassword, db:Cursor = Depends(get_cursor)):
    query = 'EXEC forgotPassword @password =?, @userName =?'
    queryParams = ( request.password, request.username)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)