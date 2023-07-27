import json
from routers.config import get_cursor
from routers.services.sms import sendSMS
from routers.services.mail import sendEmail
from aioodbc.cursor import Cursor


def putBookingDateTimeExtendNotifications(message):
    for i in message['tempData']:
        if i["templateType"] == 'M' and message['userData'][0].get('emailId'):
            Message_str = i["messageBody"].replace("[Name]", message['userData'][0]['userName']).replace(
                "[Vehicle type parking]", message['userData'][0]['vehicleTypeName']).replace("[parking name]", message['userData'][0]['parkingName'])
            Data = {"subject": i["subject"].replace(
                "[Vehicle type parking]", message['userData'][0]['vehicleTypeName']), "contact": message['userData'][0]['emailId'], "mail_content": Message_str}
            sendEmail(Data)
        # elif i["templateType"] == 'S' and message['userData'][0].get('phoneNumber'):
        #     sendSMS(
        #         "smart-parking", message['userData'][0]['phoneNumber'], i["messageBody"], i["peid"], i["tpid"])
async def Otp(MobileNo):
    print("datafetching")
    db=Cursor
    msgquery = 'EXEC getMessagetemplate @MessageHeader=?'
    msgqueryParams = ('OTP')
    await db.execute(f"""{msgquery}""", msgqueryParams)
    msgres = await db.fetchall()
    print(msgres[0][0],len(msgres),"messagetemplate")
    #     if (len(msgres)>0):
    
    # for i in message['tempData']:
    #     if i["templateType"] == 'M' and message['userData'][0].get('emailId'):
    #         Message_str = i["messageBody"].replace("[Name]", message['userData'][0]['userName']).replace(
    #             "[Vehicle type parking]", message['userData'][0]['vehicleTypeName']).replace("[parking name]", message['userData'][0]['parkingName'])
    #         Data = {"subject": i["subject"].replace(
    #             "[Vehicle type parking]", message['userData'][0]['vehicleTypeName']), "contact": message['userData'][0]['emailId'], "mail_content": Message_str}
    #         sendEmail(Data)
        # elif i["templateType"] == 'S' and message['userData'][0].get('phoneNumber'):
        #     sendSMS(
        #         "smart-parking", message['userData'][0]['phoneNumber'], i["messageBody"], i["peid"], i["tpid"])

        
    
callbackDic = {
    'putBookingDateTimeExtend':putBookingDateTimeExtendNotifications,
    'Otp':Otp
}    


def callback(message):
    message = json.loads(message)
    callbackDic[message['action']](message['body'])