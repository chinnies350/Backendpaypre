from fastapi.routing import APIRouter
from schemas import PostPricingAppFeatMap
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from typing import Tuple,Dict, List
import json
from joblib import Parallel, delayed
from routers.utils.apiCommon import ApiWithProcedure,ApiWithProcedureTrans, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete

from time import time


router = APIRouter(prefix='/pricingAppFeatMap', tags=['PricingAppFeatMap'])
def callFunction(i):
    return i.dict()

@router.get('')
async def pricingAppFeatMapGet(ActiveStatus:Optional[str]=Query(None), AppId:Optional[int]=Query(None),UserId:Optional[int]=Query(None),Type:Optional[str]=Query(None),db:Cursor= Depends(get_cursor)):
    query = 'EXEC getPricingAppFeatMap @ActiveStatus=?, @AppId=?,@UserId=?,@Type=?'
    queryParams = ( ActiveStatus, AppId,UserId,Type)
    

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)

@router.post('')
async def pricingAppFeatMapPost(request: PostPricingAppFeatMap, db:Cursor= Depends(get_cursor)):
    # print(request.FeatDetails,"request.FeatDetails")
    query = 'EXEC postPricingAppFeatMap @AppId=?,@PricingId =?,@FeatDetails =?, @CreatedBy=?'
    # print(request,"requestrequest")
    
    def transformFunction(request: PostPricingAppFeatMap) -> Tuple:
        formattedData = []
        if request.FeatDetails:
            featIds = list(set([data.FeatId for data in request.FeatDetails]))
            formattedData = [{"FeatId": featId} for featId in featIds]
            
        return (request.AppId, request.PricingId,json.dumps(formattedData), request.CreatedBy)
    
    # def transformFunction(request:PostPricingAppFeatMap):
    #     FeatDetails: str | None | List = None
    #     if request.FeatDetails != None:
    #         r = Parallel(n_jobs=-2, verbose=True)(delayed(callFunction)(i) for i in request.FeatDetails)
    #         FeatDetails=json.dumps(r)
            # 
            # h=(delayed(callFunction)(i) for i in request.FeatDetails)
            # print(h,"hello")
            # FeatDetails = Parallel(
            #     n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.FeatDetails)
            # FeatDetails = json.dumps(FeatDetails,indent=4, sort_keys=True, default=str)
        # else:
        #     FeatDetails = None
        # return (request.AppId, request.PricingId,FeatDetails, request.CreatedBy)
    
    
    return await ApiWithProcedureTrans(db=db, 
                                    query=query,
                                    request=request, 
                                    transformParam=transformFunction, 
                                    additionalFunction=additionalFunctionPost)
    




@router.delete('')
async def pricingAppFeatMapDelete(UpdatedBy: int, AppId: int,PricingId:int, ActiveStatus: str,db:Cursor = Depends(get_cursor)):
    query = 'EXEC deletePricingAppFeatMap @UpdatedBy=?, @AppId =?,@PricingId=?, @ActiveStatus=?'
    queryParams = (  UpdatedBy, AppId,PricingId , ActiveStatus)
    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)




