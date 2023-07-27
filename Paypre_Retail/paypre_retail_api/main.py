from fastapi import FastAPI
from routers.utils.responseMessages import WELCOME_MESSAGE

from routers import configType, configMaster, tax, shift, settings, employee, supplier, empAccess, product, inwardHdr, inwardDtl, salesHdr, orderHdr, diningTable, diningChair, comboHdr, customer

app = FastAPI()


@app.get('/')
def home():
    return WELCOME_MESSAGE


app.include_router(configType.router)
app.include_router(configMaster.router)
app.include_router(tax.router)
app.include_router(shift.router)
app.include_router(settings.router)
app.include_router(employee.router)
app.include_router(supplier.router)
app.include_router(empAccess.router)
app.include_router(product.router)
app.include_router(inwardHdr.router)
app.include_router(inwardDtl.router)
app.include_router(salesHdr.router)
app.include_router(orderHdr.router)
app.include_router(diningTable.router)
app.include_router(diningChair.router)
app.include_router(comboHdr.router)
app.include_router(customer.router)

