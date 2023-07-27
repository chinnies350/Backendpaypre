from fastapi.routing import APIRouter
from schemas import PostUser,PutUser,PutPassword,PutPin,PutUserProfile
from aioodbc.cursor import Cursor
from routers.config import get_cursor,logs_collection
from fastapi import Depends
from typing import Optional
from fastapi import Query
import datetime
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete


router = APIRouter(prefix='/user', tags=['User'])

def insert_log(user_id, message):
    log_entry = {
        'timestamp': datetime.datetime.utcnow(),
        'user_id': user_id,
        'message': message
    }

    logs_collection.insert_one(log_entry)

@router.get('')
async def userGet(UserId:Optional[int] = Query(None), ActiveStatus:Optional[str] = Query(None), MobileNo:Optional[str] = Query(None) ,UserType:Optional[str] = Query(None) ,db:Cursor= Depends(get_cursor)):
    query = 'EXEC getUser @UserId=?, @ActiveStatus=?,@MobileNo=? ,@UserType=?'
    queryParams = ( UserId, ActiveStatus, MobileNo, UserType)
    

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)


@router.post('')
async def userPost(request: PostUser, db:Cursor= Depends(get_cursor)):
    query = f"""EXEC postUser @UserType=?, @CompId=?, @BranchId=?, @MobileNo=?, @MailId=?, @UserName=?, @UserImage=?, @Password=?, @Pin=?, @CreatedBy=?,@AppId=?"""
    queryParams = (  request.UserType, request.CompId, request.BranchId, request.MobileNo, request.MailId, request.UserName, request.UserImage ,request.Password, request.Pin, request.CreatedBy,request.AppId)
    
    def manipulatePostResponse(res):
        if res[0][1] == 1:
            username = request.UserName if request.UserName else request.MobileNo
            insert_log(res[0][2], f"{username} User have been Created")
        return additionalFunctionPost(res)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=manipulatePostResponse)
    
@router.put('')
async def userPut(request: PutUser, db:Cursor = Depends(get_cursor)):
    query = f"""EXEC putUser @UserType=?,@MobileNo=?, @MailId=?, @UserName=?, @UserImage=?, @Password=?, @Pin=?, @UpdatedBy=?, @UserId=?"""
    queryParams = ( request.UserType, 
                #    request.CompId, request.BranchId, 
                   request.MobileNo, request.MailId, request.UserName, request.UserImage ,request.Password, request.Pin, request.UpdatedBy, request.UserId )

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)
    
@router.delete('')
async def userdelete(UserId: int, ActiveStatus: str, UpdatedBy: int, db:Cursor = Depends(get_cursor)):
    query = 'EXEC deleteUser @UserId=?, @ActiveStatus=?, @UpdatedBy=?'
    queryParams = (  UserId, ActiveStatus, UpdatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)
    
    
@router.put('/setPassword')
async def userPutPassword(request: PutPassword, db:Cursor= Depends(get_cursor)):
    query = f"""EXEC putUserPassword @Password=?, @UpdatedBy=?,@UserId=?"""
    queryParams = (  request.Password,request.UpdatedBy,request.UserId )

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)
    


@router.put('/setPin')
async def userPutPin(request: PutPin, db:Cursor= Depends(get_cursor)):
    query = f"""EXEC putUserPin @Pin=?, @UpdatedBy=?,@UserId=?"""
    queryParams = (  request.Pin,request.UpdatedBy,request.UserId )

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)
    
@router.put('/updateUserProfile')
async def userPutProfile(request: PutUserProfile, db:Cursor = Depends(get_cursor)):
    query = f"""EXEC putUserProfile @MobileNo=?, @MailId=?, @UserName=?, @UserImage=?, @UpdatedBy=?, @UserId=?"""
    queryParams = ( request.MobileNo, request.MailId, request.UserName, request.UserImage, request.UpdatedBy, request.UserId )

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)






# from fastapi.routing import APIRouter
# from schemas import PostUser,PutUser,PutPassword,PutPin,PutUserProfile
# from aioodbc.cursor import Cursor
# from routers.config import get_cursor,logs_collection
# from fastapi import Depends
# from typing import Optional
# from fastapi import Query
# import datetime
# from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete


# router = APIRouter(prefix='/user', tags=['User'])

# def insert_log(user_id, message):
#     log_entry = {
#         'timestamp': datetime.datetime.utcnow(),
#         'user_id': user_id,
#         'message': message
#     }

#     logs_collection.insert_one(log_entry)

# @router.get('')
# async def userGet(UserId:Optional[int] = Query(None), ActiveStatus:Optional[str] = Query(None), MobileNo:Optional[str] = Query(None) ,UserType:Optional[str] = Query(None) ,db:Cursor= Depends(get_cursor)):
#     query = 'EXEC getUser @UserId=?, @ActiveStatus=?,@MobileNo=? ,@UserType=?'
#     queryParams = ( UserId, ActiveStatus, MobileNo, UserType)
    

#     return await ApiWithProcedureGet(db=db, 
#                                         query=query, 
#                                         queryParams=queryParams)


# @router.post('')
# async def userPost(request: PostUser, db:Cursor= Depends(get_cursor)):
#     query = f"""EXEC postUser @UserType=?, @CompId=?, @BranchId=?, @MobileNo=?, @MailId=?, @UserName=?, @UserImage=?, @Password=?, @Pin=?, @CreatedBy=?"""
#     queryParams = (  request.UserType, request.CompId, request.BranchId, request.MobileNo, request.MailId, request.UserName, request.UserImage ,request.Password, request.Pin, request.CreatedBy )
    
#     def manipulatePostResponse(res):
#         if res[0][1] == 1:
#             username = request.UserName if request.UserName else request.MobileNo
#             insert_log(res[0][2], f"{username} User have been Created")
#         return additionalFunctionPost(res)

#     return await ApiWithProcedure(db=db, 
#                                     query=query, 
#                                     queryParams=queryParams, 
#                                     additionalFunction=manipulatePostResponse)
    
# @router.put('')
# async def userPut(request: PutUser, db:Cursor = Depends(get_cursor)):
#     query = f"""EXEC putUser @UserType=?, @CompId=?, @BranchId=?, @MobileNo=?, @MailId=?, @UserName=?, @UserImage=?, @Password=?, @Pin=?, @UpdatedBy=?, @UserId=?"""
#     queryParams = ( request.UserType, request.CompId, request.BranchId, request.MobileNo, request.MailId, request.UserName, request.UserImage ,request.Password, request.Pin, request.UpdatedBy, request.UserId )

#     return await ApiWithProcedure(db=db, 
#                                     query=query, 
#                                     queryParams=queryParams, 
#                                     additionalFunction=additionalFunctionPut)
    
# @router.delete('')
# async def userdelete(UserId: int, ActiveStatus: str, UpdatedBy: int, db:Cursor = Depends(get_cursor)):
#     query = 'EXEC deleteUser @UserId=?, @ActiveStatus=?, @UpdatedBy=?'
#     queryParams = (  UserId, ActiveStatus, UpdatedBy)

#     return await ApiWithProcedure(db=db, 
#                                     query=query, 
#                                     queryParams=queryParams, 
#                                     additionalFunction=additionalFunctionDelete)
    
    
# @router.put('/setPassword')
# async def userPutPassword(request: PutPassword, db:Cursor= Depends(get_cursor)):
#     query = f"""EXEC putUserPassword @Password=?, @UpdatedBy=?,@UserId=?"""
#     queryParams = (  request.Password,request.UpdatedBy,request.UserId )

#     return await ApiWithProcedure(db=db, 
#                                     query=query, 
#                                     queryParams=queryParams, 
#                                     additionalFunction=additionalFunctionPut)
    


# @router.put('/setPin')
# async def userPutPin(request: PutPin, db:Cursor= Depends(get_cursor)):
#     query = f"""EXEC putUserPin @Pin=?, @UpdatedBy=?,@UserId=?"""
#     queryParams = (  request.Pin,request.UpdatedBy,request.UserId )

#     return await ApiWithProcedure(db=db, 
#                                     query=query, 
#                                     queryParams=queryParams, 
#                                     additionalFunction=additionalFunctionPut)
    
# @router.put('/updateUserProfile')
# async def userPutProfile(request: PutUserProfile, db:Cursor = Depends(get_cursor)):
#     query = f"""EXEC putUserProfile @MobileNo=?, @MailId=?, @UserName=?, @UserImage=?, @UpdatedBy=?, @UserId=?"""
#     queryParams = ( request.MobileNo, request.MailId, request.UserName, request.UserImage, request.UpdatedBy, request.UserId )

#     return await ApiWithProcedure(db=db, 
#                                     query=query, 
#                                     queryParams=queryParams, 
#                                     additionalFunction=additionalFunctionPut)