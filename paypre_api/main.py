from fastapi import FastAPI
from routers.utils.responseMessages import WELCOME_MESSAGE
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status,Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError

from routers import configType, configMaster, carousel, applicationMaster, feature, currency, pricingType, PricingAppFeatMap, appImage, UserAppMap, company,branch,user,compAppMap,appMenu,adminTax,forgotpassword,changepassword,login,verifyOTP,gmailLogin,appAccess,UPIpmtStatus,MessageTemplates,paymentUpi,logs,getFeatureMapping




app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "statusCode": "0","response":"Invalid Data"}),
    )


origins = ['*']




app.add_middleware(CORSMiddleware, 
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

@app.get('/')
def home():
    return WELCOME_MESSAGE



app.include_router(configType.router)
app.include_router(configMaster.router)
app.include_router(carousel.router)
app.include_router(company.router)
app.include_router(branch.router)
app.include_router(user.router)
app.include_router(compAppMap.router)
app.include_router(appMenu.router)
app.include_router(applicationMaster.router)
app.include_router(feature.router)
app.include_router(currency.router)
app.include_router(pricingType.router)
app.include_router(PricingAppFeatMap.router)
app.include_router(appImage.router)
app.include_router(UserAppMap.router)
app.include_router(adminTax.router)
app.include_router(forgotpassword.router)
app.include_router(changepassword.router)
app.include_router(login.router)
app.include_router(verifyOTP.router)
app.include_router(gmailLogin.router)
app.include_router(appAccess.router)
app.include_router(UPIpmtStatus.router)
app.include_router(MessageTemplates.router)
app.include_router(paymentUpi.router)
app.include_router(logs.router)
app.include_router(getFeatureMapping.router)




origins = ['*']

app.add_middleware(CORSMiddleware, 
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

