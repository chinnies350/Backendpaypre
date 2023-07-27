from fastapi.routing import APIRouter
from schemas import Changepassword
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from routers.utils.passwordEncrypt import verify_password,get_password_hash
from routers.utils.apiCommon import ApiWithProcedure, additionalFunctionPut

router = APIRouter(prefix='/changepassword',tags=['Changepassword'])

@router.put('')
async def changepassword(request: Changepassword, db:Cursor= Depends(get_cursor)):
    query = f"SELECT password FROM [User] WHERE UserId=?"
    queryParams= (request.UserId)
    result = await db.execute(query, queryParams)
    row = await result.fetchone()
    if row[0] == None:
        return {
            'statusCode':0,
            'response':'check your userId'
        }    
    if verify_password(request.Oldpassword,row[0])==False:
        return {
            'statusCode':0,
            'response':'check your old password'
        }
    else:
        query = 'EXEC Changepassword @UserId=?, @Newpassword=?'
        queryParams = ( request.UserId, request.Newpassword)

        return await ApiWithProcedure(db=db, 
                                        query=query, 
                                        queryParams=queryParams, 
                                        additionalFunction=additionalFunctionPut)