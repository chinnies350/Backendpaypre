from fastapi.routing import APIRouter
from schemas import PostMessagetemplate, PutMessagetemplate
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete

router = APIRouter(prefix='/messagetemplates', tags=['MessageTemplates'])


@router.get('')
async def messagetemplateGet(MessageHeader:Optional[str]=Query(None), Subject:Optional[str]=Query(None), TemplateType:Optional[str]=Query(None), UniqueId:Optional[int]=Query(None), db:Cursor= Depends(get_cursor)):
    query = 'EXEC getMessagetemplate @MessageHeader=?, @Subject=?, @TemplateType=?,@UniqueId=?'
    queryParams = ( MessageHeader, Subject, TemplateType, UniqueId )

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)


@router.post('')
async def messagetemplatePost(request: PostMessagetemplate, db:Cursor= Depends(get_cursor)):
    query = 'EXEC postMessageTemplates @MessageHeader=?, @Subject=?,@MessageBody=?,@TemplateType=?,@Peid=?,@Tpid=?,@CreatedBy=?'
    queryParams = ( request.MessageHeader,request.Subject,request.MessageBody,request.TemplateType,request.Peid,request.Tpid,request.CreatedBy)
    
    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPost)
    
@router.put('')
async def messagetemplatePut(request: PutMessagetemplate, db:Cursor = Depends(get_cursor)):
    query = 'EXEC putMessageTemplates @MessageHeader=?, @Subject=?,@MessageBody=?,@TemplateType=?,@Peid=?,@Tpid=?,@UpdatedBy=?,@UniqueId=?'
    queryParams = ( request.MessageHeader,request.Subject,request.MessageBody,request.TemplateType,request.Peid,request.Tpid,request.UpdatedBy, request.UniqueId)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)