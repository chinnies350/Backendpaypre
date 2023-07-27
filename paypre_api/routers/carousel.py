from fastapi.routing import APIRouter
from schemas import PostCarousel, PutCarousel
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete



router = APIRouter(prefix='/carousel', tags=['Carousel'])

@router.get('')
async def carouselGet(ScreenId:Optional[int]=Query(None), ActiveStatus:Optional[str]=Query(None), CarouselId:Optional[int]=Query(None), db:Cursor= Depends(get_cursor)):
    query = 'EXEC getCarousel @ScreenId=?, @ActiveStatus=?, @CarouselId=?'
    queryParams = ( ScreenId, ActiveStatus, CarouselId)

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)

@router.post('')
async def carouselPost(request: PostCarousel, db:Cursor= Depends(get_cursor)):
    query = 'EXEC postCarousel @ScreenId=?, @Carousel=?,@CreatedBy=?'
    queryParams = ( request.ScreenId, request.Carousel,request.CreatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPost)

@router.put('')
async def carouselPut(request: PutCarousel, db:Cursor = Depends(get_cursor)):
    query = 'EXEC putCarousel @ScreenId=?, @Carousel=?, @UpdatedBy=?, @CarouselId=?'
    queryParams = ( request.ScreenId, request.Carousel, request.UpdatedBy, request.CarouselId)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionPut)

@router.delete('')
async def carouselPut(UpdatedBy: int, CarouselId: int, ActiveStatus: str,db:Cursor = Depends(get_cursor)):
    query = 'EXEC deleteCarousel @UpdatedBy=?, @CarouselId=?, @ActiveStatus=?'
    queryParams = (  UpdatedBy, CarouselId, ActiveStatus)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)




