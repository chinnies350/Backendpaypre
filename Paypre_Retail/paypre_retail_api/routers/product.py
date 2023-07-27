from fastapi.routing import APIRouter
from schemas import PostProduct,PutProduct
from aioodbc.cursor import Cursor
from routers.config import get_cursor
from fastapi import Depends
from typing import Optional
from fastapi import Query
from typing import Tuple,Dict,List
import json
from joblib import Parallel, delayed
from routers.utils.apiCommon import ApiWithProcedure, ApiWithProcedureTrans, ApiWithProcedureGet,additionalFunctionPost, additionalFunctionPut, additionalFunctionDelete

router = APIRouter(prefix='/product', tags=['Product'])

def callFunction(i):
    return i.dict()

@router.get('')
async def productGet(ProdId:Optional[int] = Query(None), ActiveStatus:Optional[str] = Query(None), db:Cursor= Depends(get_cursor))->Dict:
    query :str = 'EXEC getProduct @ProdId=?, @ActiveStatus=?'
    queryParams :Tuple = ( ProdId, ActiveStatus )

    return await ApiWithProcedureGet(db=db, 
                                        query=query, 
                                        queryParams=queryParams)
    
    
@router.post('')
async def productPost(request:PostProduct, db:Cursor= Depends(get_cursor))-> Dict:
    query :str= f"""EXEC postProduct @CompId=?, @BranchId=?, @ProdType=?, @UOM=?, @ProdCat=?, @ProdSubCat=?, @ProdName=?, @Brand=?,
        @Size=?, @HSNCode=?, @Rack=?, @OpeningQty=?, @QtyBasedPrice=?, @AvailableFrom=?, @AvailableTo=?, @QRCode=?, @CreatedBy=?, @ProductTaxDetails=?"""
    
    def transformFunction(request:PostProduct):
        ProductTaxDetails: str | None | List = None
        
        if request.ProductTaxDetails != None:
            ProductTaxDetails = Parallel(
                n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.ProductTaxDetails)
            ProductTaxDetails = json.dumps(ProductTaxDetails,indent=4, sort_keys=True, default=str)
        else:
            ProductTaxDetails = None
        return (request.CompId, request.BranchId, request.ProdType, request.UOM, request.ProdCat, request.ProdSubCat, request.ProdName, request.Brand,
                request.Size, request.HSNCode, request.Rack, request.OpeningQty, request.QtyBasedPrice, request.AvailableFrom, request.AvailableTo, request.QRCode, request.CreatedBy, ProductTaxDetails)

    return await ApiWithProcedureTrans(db=db, 
                                    query=query,
                                    request=request, 
                                    transformParam=transformFunction, 
                                    additionalFunction=additionalFunctionPost)
    
    
@router.put('')
async def productPut(request:PutProduct, db:Cursor= Depends(get_cursor))-> Dict:
    query :str= f"""EXEC putProduct @CompId=?, @BranchId=?, @ProdType=?, @UOM=?, @ProdCat=?, @ProdSubCat=?, @ProdName=?, @Brand=?,
        @Size=?, @HSNCode=?, @Rack=?, @OpeningQty=?, @QtyBasedPrice=?, @AvailableFrom=?, @AvailableTo=?, @QRCode=?, @UpdatedBy=?, @ProdId=?,  @ProductTaxDetails=?"""
    
    def transformFunction(request:PutProduct):
        ProductTaxDetails: str | None | List = None
        
        if request.ProductTaxDetails != None:
            ProductTaxDetails = Parallel(
                n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.ProductTaxDetails)
            ProductTaxDetails = json.dumps(ProductTaxDetails,indent=4, sort_keys=True, default=str)
        else:
            ProductTaxDetails = None
        return (request.CompId, request.BranchId, request.ProdType, request.UOM, request.ProdCat, request.ProdSubCat, request.ProdName, request.Brand,
                request.Size, request.HSNCode, request.Rack, request.OpeningQty, request.QtyBasedPrice, request.AvailableFrom, request.AvailableTo, request.QRCode, request.UpdatedBy, request.ProdId, ProductTaxDetails)

    return await ApiWithProcedureTrans(db=db, 
                                    query=query,
                                    request=request, 
                                    transformParam=transformFunction, 
                                    additionalFunction=additionalFunctionPut)
    

@router.delete('')
async def productDelete(ProdId: int, ActiveStatus: str, UpdatedBy: int,db:Cursor = Depends(get_cursor))->Dict:
    query :str = 'EXEC deleteProduct @ProdId=?, @ActiveStatus=?, @UpdatedBy=?'
    queryParams :Tuple = ( ProdId, ActiveStatus, UpdatedBy)

    return await ApiWithProcedure(db=db, 
                                    query=query, 
                                    queryParams=queryParams, 
                                    additionalFunction=additionalFunctionDelete)