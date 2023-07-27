from fastapi.routing import APIRouter
from schemas import GmailLogin,UpdatePassWord
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
import json
from random import randint
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete


router = APIRouter(prefix='/gmailLogin', tags=['GmailLogin'])

def generate_otp():
    return randint(100000, 999999)

# def row_to_dict(row):
#     return dict(zip(row.keys(), row))
# @router.post('')
# async def adminTaxPost(request: GmailLogin, db:Cursor= Depends(get_cursor)):
#     query = 'EXEC gmailLogin @UserName=?'
#     queryParams = (request.UserName)

#     return await ApiWithProcedure(db=db, 
#                                     query=query, 
#                                     queryParams=queryParams, 
#                                     additionalFunction=additionalFunctionPost)

@router.post("/register")
async def register_user(request: GmailLogin, db: Cursor = Depends(get_cursor)):
    query = "SELECT * FROM [User] WHERE (MailId = ? OR MobileNo=?)"
    queryParams = (request.UserName,request.UserName)
    result = await db.execute(query, queryParams)
    row = await result.fetchone()
    print('row',row)
    if row != None:
        return {"statusCode": 1,"response": "Data Found","data":dict(zip([column[0] for column in result.description], row))}
    otp = generate_otp()
    query = f"""INSERT INTO [User](UserType,MobileNo,MailId,UserName,Password,ActiveStatus ,CreatedBy, CreatedDate) 
			VALUES ('P','0123456789',?,?,'123','A', 1, GETDATE())"""
    queryParams = (request.UserName, request.UserName)
    print("Query:", query)
    print("Params:", queryParams)
    await db.execute(query, queryParams)
    await db.commit()
    return {"statusCode": 1, "response": "Please verify your email with the OTP sent to your registered email address", "OTP":otp}


@router.post("/password_setup")
async def password_setup(request: UpdatePassWord, db: Cursor = Depends(get_cursor)):
    query = "SELECT * FROM [User] WHERE (MailId = ? OR MobileNo=?)"
    queryParams = (request.MailId, request.MobileNo)
    db.execute(query, queryParams)
    user = db.fetchone()
    if user is None:
        return {"statusCode": 0,"response":"User does not exist"}
    # Verify the OTP
    # if request.otp != generate_otp():
    #     return {"statusCode": 0,"response":"Invalid OTP"}
    # Prompt user to set a new password
    query = "UPDATE [User] SET UserName=?,Password = ?, MobileNo=?, UpdatedBy=?, UpdatedDate=GETDATE() WHERE MailId = ?"
    queryParams = (request.UserName, request.password, request.MobileNo, request.UpdatedBy, request.MailId)
    await db.execute(query, queryParams)
    await db.commit()
    return {"statusCode": 1,"response":"Password set successfully"}