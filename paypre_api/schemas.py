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
    SmallIcon: Optional[str] = Query(None)
    CreatedBy: int

class PutConfigMaster(BaseModel):
    TypeId: int
    ConfigName: str
    AlphaNumFld: Optional[str] = Query(None)
    NumFld: Optional[float] = Query(None)
    SmallIcon: Optional[str] = Query(None)
    UpdatedBy: int
    ConfigId: int

class PostCarousel(BaseModel):
    ScreenId: int
    Carousel: str
    CreatedBy: int

class PutCarousel(BaseModel):
    ScreenId: int
    Carousel: str
    UpdatedBy: int
    CarouselId: int
    
class PostCompany(BaseModel):
    CompName: str
    CompShName: str
    BusiBrief: Optional[str] = Query(None)
    CompLogo: Optional[str] = Query(None)
    # CompAddId: Optional[int] = Query(None)
    CompGSTIN: Optional[str] = Query(None)
    Proprietor:str
    CompPOC:Optional[str] = Query(None)
    CompMobile:Optional[str] = Query(None)
    CompEmail: Optional[str] = Query(None)
    CompRegnNo: Optional[str] = Query(None)
    CreatedBy: int
    Address1: str
    Address2: Optional[str] = Query(None)
    Zip:int
    City:str
    Dist:str
    State:str
    Latitude: Optional[float] = Query(None)
    Longitude: Optional[float] = Query(None)
    
class PutCompany(BaseModel):
    CompName: str
    CompShName: str
    BusiBrief: Optional[str] = Query(None)
    CompLogo: Optional[str] = Query(None)
    CompAddId: Optional[int] = Query(None)
    CompGSTIN: Optional[str] = Query(None)
    Proprietor:str
    CompPOC:Optional[str] = Query(None)
    CompMobile:Optional[str] = Query(None)
    CompEmail: Optional[str] = Query(None)
    CompRegnNo: Optional[str] = Query(None)
    UpdatedBy: int
    Address1: str
    Address2: Optional[str] = Query(None)
    Zip:int
    City:str
    Dist:str
    State:str
    Latitude: Optional[float] = Query(None)
    Longitude: Optional[float] = Query(None)
    AddId:int
    CompId:int
    
class PostBranch(BaseModel):
    CompId: int
    BrName: str
    BrShName: str
    BrGSTIN: Optional[str] = Query(None)
    BrInCharge: str
    BrMobile: Optional[str] = Query(None)
    BrEmail:Optional[str] = Query(None)
    BrRegnNo:Optional[str] = Query(None)
    WorkingFrom:Optional[time] = Query(None)
    WorkingTo: Optional[time] = Query(None)
    CreatedBy: int
    Address1: str
    Address2: Optional[str] = Query(None)
    Zip:int
    City:str
    Dist:str
    State:str
    Latitude: Optional[float] = Query(None)
    Longitude: Optional[float] = Query(None)
    
class PutBranch(BaseModel):
    CompId: int
    BrName: str
    BrShName: str
    BrGSTIN: Optional[str] = Query(None)
    BrInCharge: str
    BrMobile: Optional[str] = Query(None)
    BrEmail:Optional[str] = Query(None)
    BrRegnNo:Optional[str] = Query(None)
    WorkingFrom:Optional[time] = Query(None)
    WorkingTo: Optional[time] = Query(None)
    UpdatedBy: int
    Address1: str
    Address2: Optional[str] = Query(None)
    Zip:int
    City:str
    Dist:str
    State:str
    Latitude: Optional[float] = Query(None)
    Longitude: Optional[float] = Query(None)
    BrId:int
    AddId:int
    
class PostUser(BaseModel):
    UserType: str
    CompId: Optional[int]= Query(None)
    BranchId: Optional[int]= Query(None)
    MobileNo: str
    MailId: Optional[str] = Query(None)
    UserName: str
    Password:str
    Pin:Optional[int]= Query(None)
    CreatedBy: int
    
class PutUser(BaseModel):
    UserType: str
    CompId: Optional[int]= Query(None)
    BranchId: Optional[int]= Query(None)
    MobileNo: str
    MailId: Optional[str] = Query(None)
    UserName: str
    Password:str
    Pin:Optional[int]= Query(None)
    UpdatedBy: int
    UserId:int
    
class PostCompAppMap(BaseModel):
    CompId: int
    BranchId: int
    AppId: int
    CreatedBy: int
    
class PutCompAppMap(BaseModel):
    CompId: int
    BranchId: int
    AppId: int
    UpdatedBy: int
    UniqueId: int
    
class PostAppMenu(BaseModel):
    AppId: int
    MenuName: str
    Level: str
    Level1Id: int
    Level2Id: int
    Level3Id: int
    CreatedBy: int
    
class putAppMenu(BaseModel):
    AppId: int
    MenuName: str
    Level: str
    Level1Id: int
    Level2Id: int
    Level3Id: int
    UpdatedBy: int
    MenuId: int
    
class PostApplication(BaseModel):
    AppName: str
    AppDescription: str
    AppLogo: Optional[str] = Query(None)
    CateId: int
    SubCateId: int
    BannerImage: str
    CreatedBy: int

class PutApplication(BaseModel):
    AppName: str
    AppDescription: str
    AppLogo: Optional[str] = Query(None)
    CateId: int
    SubCateId: int
    BannerImage: str
    UpdatedBy: int
    AppId: int

class PostFeature(BaseModel):
    FeatCat: int
    FeatName: str
    FeatDescription: str
    FeatType: int
    FeatConstraint: Optional[int]=Query(None)
    CoreAddon: str
    CreatedBy: int

class PutFeature(BaseModel):
    FeatCat: int
    FeatName: str
    FeatDescription: str
    FeatType: int
    FeatConstraint: Optional[int]=Query(None)
    CoreAddon: str
    UpdatedBy: int
    FeatId: int

class PostCurrency(BaseModel):
    CurrName: str
    CurrShName: str
    ConvRate: float
    CreatedBy: int

class PutCurrency(BaseModel):
    CurrName: str
    CurrShName: str
    ConvRate: float
    UpdatedBy: int
    CurrId: int

class PostPricingType(BaseModel):
    AppId: int
    PricingName: str 
    Price: float=Query(None)
    DisplayPrice:float = Query(None)
    PriceTag:int = Query(None)
    TaxId:int=Query(None)
    TaxAmount:float=Query(None)
    NetPrice:float =Query(None) 
    CurrId: int
    NoOfDays: int
    CreatedBy: int

class PutPricingType(BaseModel):
    AppId: int
    PricingName: str 
    Price: float=Query(None)
    DisplayPrice:float = Query(None)
    PriceTag:int = Query(None)
    TaxId:int=Query(None)
    TaxAmount:float=Query(None)
    NetPrice:float =Query(None) 
    CurrId: int
    NoOfDays: int
    UpdatedBy: int
    PricingId: int
    
class FeatDetail(BaseModel):
    FeatId: int

class PostPricingAppFeatMap(BaseModel):
    AppId: int
    PricingId: int
    FeatDetails:List[FeatDetail]=Query(None)
    # Optional
    CreatedBy: int



class PostPaymentUpiDetails(BaseModel):
    MobileNo:str
    Name: str
    UPIId:str
    UserId: Optional[int]=Query(None)
    CompId: Optional[int]=Query(None)
    BrId: Optional[int]=Query(None)
    type: Optional[str]=Query(None)
    MerchantCode: Optional[str]=Query(None)
    MerchantId: Optional[str]=Query(None)
    mode: Optional[str]=Query(None)
    orgid: Optional[str]=Query(None)
    sign: Optional[str]=Query(None)
    url: Optional[str]=Query(None)
    CreatedBy:int
    
class PutPaymentUpiDetails(BaseModel):
    MobileNo:str
    Name: str
    UPIId:str
    AdminId: Optional[int]=Query(None)
    CompId: Optional[int]=Query(None)
    BranchId: Optional[int]=Query(None)
    type: Optional[str]=Query(None)
    MerchantCode: Optional[str]=Query(None)
    MerchantId: Optional[str]=Query(None)
    mode: Optional[str]=Query(None)
    orgid: Optional[str]=Query(None)
    sign: Optional[str]=Query(None)
    url: Optional[str]=Query(None)
    UpdatedBy:int
    PaymentUPIDetailsId:int
# class PostPaymentUpiDetails(BaseModel):
#     MobileNo:str
#     Name: str
#     UPIId:str
#     UserId: Optional[int]=Query(None)
#     CompId: Optional[int]=Query(None)
#     BrId: Optional[int]=Query(None)
#     type: Optional[str]=Query(None)
#     MerchantCode: str
#     MerchantId: str
#     mode: Optional[str]=Query(None)
#     orgid: Optional[str]=Query(None)
#     sign: Optional[str]=Query(None)
#     url: Optional[str]=Query(None)
#     CreatedBy:int
    
# class PutPaymentUpiDetails(BaseModel):
#     MobileNo:str
#     Name: str
#     UPIId:str
#     AdminId: Optional[int]=Query(None)
#     CompId: Optional[int]=Query(None)
#     BranchId: Optional[int]=Query(None)
#     type: Optional[str]=Query(None)
#     MerchantCode: str
#     MerchantId: str
#     mode: Optional[str]=Query(None)
#     orgid: Optional[str]=Query(None)
#     sign: Optional[str]=Query(None)
#     url: Optional[str]=Query(None)
#     UpdatedBy:int
#     PaymentUPIDetailsId:int

    
   
class ModuleDetails(BaseModel):
    AppId: int
    CompId: int
    BranchId: int
     
    
class PostAppAccess(BaseModel):
    UserId:int
    ModuleDetails:List[ModuleDetails]
    CreatedBy: int
    
    

class PostAppImage(BaseModel):
    AppId: int
    ImageType: str
    ImageName: str
    ImageLink: str
    CreatedBy: int

class PutAppImage(BaseModel):
    AppId: int
    ImageType: str
    ImageName: str
    ImageLink: str
    updatedBy: int
    ImageId: int

class PostUserAppMap(BaseModel):
    UserId:int
    AppId: int
    PricingId: int
    CompId: Optional[int]=Query(None)
    PurDate: datetime
    PaymentMode: int
    PaymentStatus: str
    LicenseStatus: str
    Price: Optional[float]=Query(None)
    TaxId: Optional[int]=Query(None)
    TaxAmount: Optional[float]=Query(None)
    NetPrice: Optional[float]=Query(None)
    ValidityStart: datetime
    ValidityEnd: datetime
    CreatedBy: int
    NoofDays:int

class PutUserAppMapPayment(BaseModel):
    PaymentStatus: str
    UpdatedBy: int
    UniqueId: int

class PostCompAppMap(BaseModel):
    CompId: int
    BranchId: int
    AppId: int
    CreatedBy: int
    
class PutCompAppMap(BaseModel):
    CompId: int
    BranchId: int
    AppId: int
    UpdatedBy: int
    UniqueId: int
    
class PostAppMenu(BaseModel):
    AppId: int
    MenuName: str
    Level: str
    Level1Id: Optional[int] = Query(None)
    Level2Id: Optional[int] = Query(None)
    # Level3Id: int
    CreatedBy: Optional[int] = Query(None)
    
class putAppMenu(BaseModel):
    AppId: int
    MenuName: str
    Level: str
    Level1Id: int
    Level2Id: int
    # Level3Id: int
    UpdatedBy: int
    MenuId: int

class PostCompany(BaseModel):
    CompName: str
    CompShName: str
    BusiBrief: Optional[str] = Query(None)
    CompLogo: Optional[str] = Query(None)
    UserId: Optional[int] = Query(None)
    # CompAddId: Optional[int] = Query(None)
    CompGSTIN: Optional[str] = Query(None)
    Proprietor:str
    CompPOC:Optional[str] = Query(None)
    CompMobile:Optional[str] = Query(None)
    CompEmail: Optional[str] = Query(None)
    CompRegnNo: Optional[str] = Query(None)
    CreatedBy: int
    Address1: Optional[str] = Query(None)
    Address2: Optional[str] = Query(None)
    Zip:Optional[int] = Query(None)
    City:Optional[str] = Query(None)
    Dist:Optional[str] = Query(None)
    State:Optional[str] = Query(None)
    Latitude: Optional[float] = Query(None)
    Longitude: Optional[float] = Query(None)
    UserId: Optional[int] = Query(None)
    AppId: Optional[int] = Query(None)
    
class PutCompany(BaseModel):
    
    CompName: str
    CompShName: str
    BusiBrief: Optional[str] = Query(None)
    CompLogo: Optional[str] = Query(None)
    CompAddId: Optional[int] = Query(None)
    CompGSTIN: Optional[str] = Query(None)
    Proprietor:str
    CompPOC:Optional[str] = Query(None)
    CompMobile:Optional[str] = Query(None)
    CompEmail: Optional[str] = Query(None)
    CompRegnNo: Optional[str] = Query(None)
    UpdatedBy: int
    Address1: Optional[str] = Query(None)
    Address2: Optional[str] = Query(None)
    Zip:Optional[int] = Query(None)
    City:Optional[str] = Query(None)
    Dist:Optional[str] = Query(None)
    State:Optional[str] = Query(None)
    Latitude: Optional[float] = Query(None)
    Longitude: Optional[float] = Query(None)
    AddId:Optional[int] = Query(None)
    CompId:int
    # UserId: Optional[int] = Query(None)
    
class PostBranch(BaseModel):
    CompId: int
    BrName: str
    BrShName: str
    BrGSTIN: Optional[str] = Query(None)
    BrInCharge: Optional[str] 
    BrMobile: Optional[str] = Query(None)
    BrEmail:Optional[str] = Query(None)
    BrRegnNo:Optional[str] = Query(None)
    WorkingFrom:Optional[time] = Query(None)
    WorkingTo: Optional[time] = Query(None)
    CreatedBy: int
    Address1: str
    Address2: Optional[str] = Query(None)
    Zip:int
    City:str
    Dist:str
    State:str
    Latitude: Optional[float] = Query(None)
    Longitude: Optional[float] = Query(None)
    AppId:int
    UserId: int
    
class PutBranch(BaseModel):
    CompId: int
    BrName: str
    BrShName: str
    BrGSTIN: Optional[str] = Query(None)
    BrInCharge: Optional[str] = Query(None)
    BrMobile: Optional[str] = Query(None)
    BrEmail:Optional[str] = Query(None)
    BrRegnNo:Optional[str] = Query(None)
    WorkingFrom:Optional[time] = Query(None)
    WorkingTo: Optional[time] = Query(None)
    UpdatedBy: int
    Address1: Optional[str] = Query(None)
    Address2: Optional[str] = Query(None)
    Zip:Optional[int] = Query(None)
    City:Optional[str] = Query(None)
    Dist:Optional[str] = Query(None)
    State:Optional[str] = Query(None)
    Latitude: Optional[float] = Query(None)
    Longitude: Optional[float] = Query(None)
    BrId:int
    AddId:Optional[int] = Query(None)


class PostUser(BaseModel):
    UserType: str
    CompId: Optional[int]= Query(None)
    BranchId: Optional[int]= Query(None)
    MobileNo: str
    MailId: Optional[str] = Query(None)
    UserName: str
    UserImage: Optional[str] = Query(None)
    Password:str
    Pin:Optional[int]= Query(None)
    CreatedBy: int
    AppId:Optional[int]= Query(None)
    
class PutPassword(BaseModel):
    Password:str
    UpdatedBy: int
    UserId:int

class PutPin(BaseModel):
    Pin:str
    UpdatedBy: int
    UserId:int
    
class PutUserProfile(BaseModel):
    MobileNo: str
    MailId: Optional[str] = Query(None)
    UserName: str
    UserImage: Optional[str] = Query(None)
    UpdatedBy: int
    UserId:int
    
class PutUser(BaseModel):
    UserType: str
    # CompId: Optional[int]= Query(None)
    # BranchId: Optional[int]= Query(None)
    MobileNo: str
    MailId: Optional[str] = Query(None)
    UserName: Optional[str]
    UserImage: Optional[str] = Query(None)
    Password:Optional[str]
    Pin:Optional[int]= Query(None)
    UpdatedBy: int
    UserId:int
# class PostUser(BaseModel):
#     UserType: str
#     CompId: Optional[int]= Query(None)
#     BranchId: Optional[int]= Query(None)
#     MobileNo: str
#     MailId: Optional[str] = Query(None)
#     UserName: str
#     UserImage: Optional[str] = Query(None)
#     Password:str
#     Pin:Optional[int]= Query(None)
#     CreatedBy: int
    
# class PutPassword(BaseModel):
#     Password:str
#     UpdatedBy: int
#     UserId:int

# class PutPin(BaseModel):
#     Pin:str
#     UpdatedBy: int
#     UserId:int
    
# class PutUserProfile(BaseModel):
#     MobileNo: str
#     MailId: Optional[str] = Query(None)
#     UserName: str
#     UserImage: Optional[str] = Query(None)
#     UpdatedBy: int
#     UserId:int
    
# class PutUser(BaseModel):
#     UserType: str
#     CompId: Optional[int]= Query(None)
#     BranchId: Optional[int]= Query(None)
#     MobileNo: str
#     MailId: Optional[str] = Query(None)
#     UserName: Optional[str] = Query(None)
#     UserImage: Optional[str] = Query(None)
#     Password:Optional[str] = Query(None)
#     Pin:Optional[int]= Query(None)
#     UpdatedBy: int
#     UserId:int
    
class PostAdminTax(BaseModel):
    TaxName:str
    TaxPercentage:Optional[float]= Query(None)
    EffectiveFrom:date
    Reference:Optional[str]= Query(None)
    CreatedBy:int
    
class Forgotpassword(BaseModel):
    password:str
    username:str
    
class Changepassword(BaseModel):
    UserId:int
    Oldpassword:str
    Newpassword:str


class VerifyOTP(BaseModel):
    UserName:Optional[str]
    
class GetOTP(BaseModel):
    UserName:Optional[str]
    Type:str

class SendLink(BaseModel):
    MobileNo:Optional[str]
    MessageHeader:Optional[str]
    Link:Optional[str]

# class VerifyOTP(BaseModel):
#     UserName:Optional[str]
    
# class GetOTP(BaseModel):
#     UserName:Optional[str]
#     Type:str

# class SendLink(BaseModel):
#     MobileNo:Optional[str]
#     MessageHeader:Optional[str]
#     Link:Optional[str]
    
class GmailLogin(BaseModel):
    UserName:str
    
class UpdatePassWord(BaseModel):
    UserName: str
    MailId: str
    MobileNo: Optional[str]=Query(None)
    password: str
    UpdatedBy: int
    # otp: int
    
class PostconfigMasterDetails(BaseModel):
    TypeId: int
    ConfigName: str
    AlphaNumFld: Optional[str] = Query(None)
    NumFld: Optional[float] = Query(None)
    SmallIcon: Optional[str] = Query(None)
    
class PostBulkUpload(BaseModel):
   ConfigMasterDetails:Optional[List[PostconfigMasterDetails]]=Query(None)
   
class PostFreeOption(BaseModel):
    UserId:int
    AppId: int
    PricingId: int
    CompId: Optional[int]=Query(None)
    PurDate: datetime
    PaymentMode: int
    PaymentStatus: str
    LicenseStatus: str
    Price: Optional[float]=Query(None)
    TaxId: Optional[int]=Query(None)
    TaxAmount: Optional[float]=Query(None)
    NetPrice: Optional[float]=Query(None)
    ValidityStart: datetime
    ValidityEnd: datetime
    CreatedBy: int
    
class PutUPIPmtStatus(BaseModel):
    paymentStatus: str
    transactionId: Optional[str]=Query(None)
    bankName:Optional[str]=Query(None)
    bankReferenceNumber: str
    UpdatedBy: int
    bookingId: int
    
class PostMessagetemplate(BaseModel):
    MessageHeader: str
    Subject: str
    MessageBody:str
    TemplateType:str
    Peid: Optional[str]=Query(None)
    Tpid: Optional[str]=Query(None)
    CreatedBy: int
    
class PutMessagetemplate(BaseModel):
    MessageHeader: str
    Subject: str
    MessageBody:str
    TemplateType:str
    Peid: Optional[str]=Query(None)
    Tpid: Optional[str]=Query(None)
    UpdatedBy: int
    UniqueId: int
    
class PostInvoicedetails(BaseModel):
    UniqueId: Optional[int]=Query(None)
    MailId:Optional[str]=Query(None)
    Link: Optional[str]=Query(None)
    
class PutBranchDefault(BaseModel):
    DefaultBranch:str
    CompId:int
    BranchId: int
    UserId: int
    


    





