from pydantic import BaseModel
from typing import List, Optional
from fastapi import Query
from datetime import date, datetime, time


class PostConfigType(BaseModel):
    TypeName: str
    CreatedBy: int
    
class PutConfigType(BaseModel):
    TypeId: int
    TypeName: str
    UpdatedBy: int

class PostConfigMaster(BaseModel):
    TypeId: int
    ConfigName: str
    AlphaNumFld: Optional[str] = Query(None)
    NumFld: Optional[float] = Query(None)
    CreatedBy: int
    
class PutConfigMaster(BaseModel):
    TypeId: int
    ConfigName: str
    AlphaNumFld: Optional[str] = Query(None)
    NumFld: Optional[float] = Query(None)
    UpdatedBy: int
    ConfigId: int
    
class PostTaxMaster(BaseModel):
    CompId:int
    TaxName:str
    TaxPercentage:Optional[float] = Query(None)
    EffectiveFrom:date
    Reference:Optional[str] = Query(None)
    CreatedBy: int
    
class PostShift(BaseModel):
    CompId: int
    ShiftName: str
    StartTime: time
    EndTime: time
    BreakStartTime: Optional[time]=Query(None)
    BreakEndTime: Optional[time]=Query(None)
    GracePeriod: int
    CreatedBy: int
 
class PutShift(BaseModel):
    CompId: int
    ShiftName: str
    StartTime: time
    EndTime: time
    BreakStartTime: Optional[time]=Query(None)
    BreakEndTime: Optional[time]=Query(None)
    GracePeriod: int
    UpdatedBy: int
    ShiftId: int
    
class PostSettings(BaseModel):
    CompId: int
    BranchId: int
    SettingId: int
    SettingValue:str
    Comments: Optional[str]=Query(None)
    CreatedBy: int
    
class PutSettings(BaseModel):
    CompId: int
    BranchId: int
    SettingId: int
    SettingValue:str
    Comments: Optional[str]=Query(None)
    UpdatedBy: int
    UniqueId: int 
    
class PostEmployee(BaseModel):
    UserId: int
    CompId: int
    BranchId: int
    # EmpCode: int
    EmpFirstName: str
    EmpLastName: str
    EmpType: int
    EmpDesig: int
    EmpDept: int
    EmpDOJ: date
    EmpPhotoLink: str
    RoleId: int
    EmpShiftId: int
    MobileAppAccess: str
    CreatedBy: int
    Address1: str
    Address2:Optional[str]=Query(None)
    Zip: int
    City: str
    Dist: str
    State: str
    Latitude:Optional[float]=Query(None)
    Longitude:Optional[float]=Query(None)
    
class PutEmployee(BaseModel):
    UserId: int
    CompId: int
    BranchId: int
    EmpCode: int
    EmpFirstName: str
    EmpLastName: str
    EmpType: int
    EmpDesig: int
    EmpDept: int
    EmpDOJ: date
    EmpPhotoLink: str
    RoleId: int
    EmpShiftId: int
    MobileAppAccess: str
    UpdatedBy: int
    Address1: str
    Address2:Optional[str]=Query(None)
    Zip: int
    City: str
    Dist: str
    State: str
    Latitude:Optional[float]=Query(None)
    Longitude:Optional[float]=Query(None)
    AddId: int
    UniqueId: int
    
class PostSupplier(BaseModel):
    CompId: int
    BranchId: int
    SuppName: str
    SuppGSTIN: Optional[str]=Query(None)
    SuppPOC: Optional[str]=Query(None)
    SuppMobile: Optional[str]=Query(None)
    SuppEmail: Optional[str]=Query(None)
    CreatedBy: int
    Address1: str
    Address2: Optional[str]=Query(None)
    Zip: int
    City: str
    Dist: str
    State: str
    Latitude:Optional[float]=Query(None)
    Longitude:Optional[float]=Query(None)
    
class PutSupplier(BaseModel):
    CompId: int
    BranchId: int
    SuppName: str
    SuppGSTIN: Optional[str]=Query(None)
    SuppPOC: Optional[str]=Query(None)
    SuppMobile: Optional[str]=Query(None)
    SuppEmail: Optional[str]=Query(None)
    UpdatedBy: int
    Address1: str
    Address2: Optional[str]=Query(None)
    Zip: int
    City: str
    Dist: str
    State: str
    Latitude:Optional[float]=Query(None)
    Longitude:Optional[float]=Query(None)
    AddId: int
    SuppId: int
    
class PostEmpAccessDetails(BaseModel):
    MenuId: int
    ReadAccess: str
    AddAccess: str
    UpdateAccess: str
    DeleteAccess: str
    
class PostEmpAccess(BaseModel):
    EmpId: int
    CompId: int
    BranchId: int
    AppId: int
    CreatedBy: int
    EmpAccessDetails:Optional[List[PostEmpAccessDetails]]=Query(None)

class PutEmpAccessDetails(BaseModel):
    MenuId: int
    ReadAccess: str
    AddAccess: str
    UpdateAccess: str
    DeleteAccess: str
    AccessId: int
    
class PutEmpAccess(BaseModel):
    EmpId: int
    CompId: int
    BranchId: int
    AppId: int
    UpdatedBy: int
    EmpAccessDetails:List[PutEmpAccessDetails]
    
class PutInwardDtl(BaseModel):
    InwardId: int
    ProdId: int
    BatchRef: Optional[str]=Query(None)
    ReceivedQty: Optional[float]=Query(None)
    AcceptedQty: Optional[float]=Query(None)
    RejectedQty: Optional[float]=Query(None)
    RejectionReason: Optional[str]=Query(None)
    IssuedQty: Optional[float]=Query(None)
    BalanceQty: Optional[float]=Query(None)
    InwardPrice: Optional[float]=Query(None)
    MRP: Optional[float]=Query(None)
    SellPrice: Optional[float]=Query(None)
    WhSalePrice: Optional[float]=Query(None)
    OfferPrice: Optional[float]=Query(None)
    ACSellPrice: Optional[float]=Query(None)
    InwardDtlId: int
    
class PutSalesHdr(BaseModel):
    SalesId: int
    ActiveStatus: str
    UpdatedBy: int
    
class PostProductTaxDetails(BaseModel):
    TaxId: int
    Cess: int
    
class PostProduct(BaseModel):
    CompId: int
    BranchId : int
    ProdType: int
    UOM: int
    ProdCat: int
    ProdSubCat:int
    ProdName:str
    Brand: Optional[int]=Query(None)
    Size: Optional[int]=Query(None)
    HSNCode: Optional[str]=Query(None)
    Rack: Optional[int]=Query(None)
    OpeningQty: Optional[float]=Query(None)
    QtyBasedPrice: str
    AvailableFrom: Optional[time]=Query(None)
    AvailableTo: Optional[time]=Query(None)
    QRCode: Optional[str]=Query(None)
    CreatedBy: int
    ProductTaxDetails:Optional[List[PostProductTaxDetails]]=Query(None)
    
class PutProductTaxDetails(BaseModel):
    TaxId: int
    Cess: int
    UniqueId: int
    
class PutProduct(BaseModel):
    CompId: int
    BranchId : int
    ProdType: int
    UOM: int
    ProdCat: int
    ProdSubCat:int
    ProdName:str
    Brand: Optional[int]=Query(None)
    Size: Optional[int]=Query(None)
    HSNCode: Optional[str]=Query(None)
    Rack: Optional[int]=Query(None)
    OpeningQty: Optional[float]=Query(None)
    QtyBasedPrice: str
    AvailableFrom: Optional[time]=Query(None)
    AvailableTo: Optional[time]=Query(None)
    QRCode: Optional[str]=Query(None)
    UpdatedBy: int
    ProdId: int
    ProductTaxDetails:Optional[List[PutProductTaxDetails]]=Query(None)
    
class PostInwardDtlDetails(BaseModel):
    ProdId: int
    BatchRef: str
    ReceivedQty: float
    AcceptedQty: float
    RejectedQty: float
    RejectionReason: str
    IssuedQty: float
    BalanceQty: float
    InwardPrice: float
    MRP: float
    SellPrice: float
    WhSalePrice: float
    OfferPrice: float
    ACSellPrice: float
    
class PostInwardHdr(BaseModel):
    CompId: int
    BranchId: int
    InwardDate: date
    SuppId: int
    Reference: Optional[str]=Query(None)
    CreatedBy: int
    InwardDtlDetails:Optional[List[PostInwardDtlDetails]]=Query(None)
    
class PostSalesDtlDetails(BaseModel):
    ProdId: int
    InwardDtlId: int
    SalesQty: float
    Rate: float
    TotalAmt: float
    TaxAmt: float
    
class PostSalesTaxDtlDetails(BaseModel):
    ProdId: int
    InwardDtlId: int
    TaxId: int
    TaxAmt: float
    
class PostSalesTableLinkDetails(BaseModel):
    TableId: int
    ChairId: int
    
class PostSalesHdr(BaseModel):
    CompId: int
    BranchId: int
    SalesDate: date
    UserId: Optional[int]=Query(None)
    OrderId: Optional[int]=Query(None)
    AddlInfo: Optional[str]=Query(None)
    BillAmount: float
    OverallDisc: Optional[float]=Query(None)
    TaxAmount: Optional[float]=Query(None)
    VatAmount: Optional[float]=Query(None)
    NetAmount: float
    PaymentType: str
    GivenAmt: Optional[float]=Query(None)
    BalGiven: Optional[float]=Query(None)
    ActiveStatus: str
    BookingMedia: str
    PaymentStatus: str
    CreatedBy: int
    SalesDtlDetails: Optional[List[PostSalesDtlDetails]]=Query(None)
    SalesTaxDtlDetails: Optional[List[PostSalesTaxDtlDetails]]=Query(None)
    SalesTableLinkDetails:Optional[List[PostSalesTableLinkDetails]]=Query(None)
    
class PostOrderDtlDetails(BaseModel):
    ProdId: int
    Type: str
    OrderQty: float
    OrderRate: float
    
class PostOrderHdr(BaseModel):
    CompId: int
    BranchId: int
    OrderDate: date
    OrderType: str
    CustSuppId: int
    Reference: str
    BookingType: Optional[int]=Query(None)
    ServiceProvider: Optional[int]=Query(None)
    ActiveStatus: str
    CreatedBy: int
    OrderDtlDetails: Optional[List[PostOrderDtlDetails]] = Query(None)
    
class PutOrderHdr(BaseModel):
    OrderId:int
    ActiveStatus: str
    UpdatedBy: int
    
class PostDiningTable(BaseModel):
    CompId: int
    BranchId: int
    TableName: str
    ChairCount: int
    ChairLevelSer: str
    DineInType: int
    CreatedBy: int
    
class PutDiningTable(BaseModel):
    CompId: int
    BranchId: int
    TableName: str
    ChairCount: int
    ChairLevelSer: str
    DineInType: int
    UpdatedBy: int
    TableId : int
    
class PostDiningChair(BaseModel):
    CompId: int
    BranchId: int
    TableId: int
    ChairName: str
    CreatedBy: int
    
class PutDiningChair(BaseModel):
    CompId: int
    BranchId: int
    ChairName: str
    UpdatedBy: int
    TableId: int
    ChairId: int
    
class PostComboDtlDetails(BaseModel):
    ProdId: int
    ComboQty: float
    
class PostComboHdr(BaseModel):
    CompId: int
    BranchId: int
    OfferPrice: float
    ValidFrom: datetime
    ValidTo: datetime
    CreatedBy: int
    ComboDtlDetails: Optional[List[PostComboDtlDetails]]=Query(None)
    
class PostCustomer(BaseModel):
    UserId: int
    CompId: int
    BranchId: int
    CustName: str
    CustGSTIN: Optional[str]=Query(None)
    CustMobile: Optional[str]=Query(None)
    CustEmail: Optional[str]=Query(None)
    CreatedBy: int
    Address1: str
    Address2: Optional[str]=Query(None)
    Zip: int
    City: str
    Dist: str
    State: str
    Latitude:Optional[float]=Query(None)
    Longitude:Optional[float]=Query(None)
    
class PutCustomer(BaseModel):
    UserId: int
    CompId: int
    BranchId: int
    CustName: str
    CustGSTIN: Optional[str]=Query(None)
    CustMobile: Optional[str]=Query(None)
    CustEmail: Optional[str]=Query(None)
    UpdatedBy: int
    Address1: str
    Address2: Optional[str]=Query(None)
    Zip: int
    City: str
    Dist: str
    State: str
    Latitude:Optional[float]=Query(None)
    Longitude:Optional[float]=Query(None)
    AddId: int 
    CustId: int   

    







