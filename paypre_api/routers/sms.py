# from ..config import SMS_API_SAFETY_KEY,SMS_URL
import requests
# from fastapi.routing import APIRouter
SMS_URL = "http://smsstreet.in/websms/sendsms.aspx"
# from routers.services.sms import sendSMS

# router=APIRouter(prefix='/sms',tags=['sms'])
# @router.post('')
def sendSMS(securitykey, MobileNumber, Message,peid,tpid):
    try:
        # assert securitykey == SMS_API_SAFETY_KEY, "Invalid Authorization!"
        querystring = {"userid": "prematix", "password": "matixpre", "sender": "PAYPRE",
                       "peid": peid, "tpid": tpid, "mobileno": MobileNumber, "msg": Message}
        headers = {'cache-control': "no-cache"}
        response = requests.request(
            "GET", SMS_URL, headers=headers, params=querystring)
        assert response.text != None, response.text 
        return {"statusCode": 1, "response": response.text}
    except Exception as e:
        return {"statusCode": 0, "response": str(e)}