import json
from routers.config import get_cursor
from routers.services.sms import sendSMS
from routers.services.mail import sendEmail,sendAttachMent,sendPdf


def bookingNotifications(message):
    try:
        for i in message['tempData']:
            if i["TemplateType"] == 'M' and message['userData'][0].get('MailId'):
                subject_str=i["Subject"]
                Message_str = i["MessageBody"].replace(
                    "[customerName]", message['userData'][0]['UserName'])
                gettingData={'AppName': message['AppName'],
                            'GuestName':message['userData'][0]['UserName'],
                            'BookingId':message['BookingId'],
                            'PaymentDate':message['PaymentDate'],
                            'totalAmount':message['totalAmount'],
                            'taxAmount':message['taxAmount'],
                            'paymenttype':message['paymenttype']
                                }
                attachMent=sendAttachMent(gettingData)
                pdf=sendPdf({'AppName': message['AppName'],
                            'GuestName':message['userData'][0]['UserName'],
                            'BookingId':message['BookingId'],
                            'PaymentDate':message['PaymentDate'],
                            'totalAmount':message['totalAmount'],
                            'taxAmount':message['taxAmount'],
                            'paymenttype':message['paymenttype']
                                })
                Data = {"subject": subject_str, "contact": message['userData'][0]
                        ['MailId'],"mail_content": Message_str,"html":attachMent,"pdf":pdf}
                sendEmail(Data)
            # else:
            #     if i["TemplateType"] == 'S' and message['userData'][0].get('MobileNo'):
            #         sendSMS(
            #         "paypre", message['userData'][0]['MobileNo'], i["MessageBody"].replace("[Link]",str(message['Link'])), i["Peid"], i["Tpid"])
    except Exception as e:
        print('error', str(e))
        
def otp(message):
    try:
        for i in message['tempData']:
            # if i["templateType"] == 'M' and message['userData'][0].get('emailId'):
            #     Message_str = i["messageBody"].replace("[Name]", message['userData'][0]['userName']).replace(
            #         "[Vehicle type parking]", message['userData'][0]['vehicleTypeName']).replace("[parking name]", message['userData'][0]['parkingName'])
            #     Data = {"subject": i["subject"].replace(
            #         "[Vehicle type parking]", message['userData'][0]['vehicleTypeName']), "contact": message['userData'][0]['emailId'], "mail_content": Message_str}
            #     sendEmail(Data)
            if i["TemplateType"] == 'S' and message['MobileNo']!=None:
                sendSMS(i["Subject"], message['MobileNo'],i["MessageBody"].replace("[OTP]",str(message['OTP'])), i["Peid"], i["Tpid"])
    except Exception as e:
        print('error', str(e))
        
def paymentLink(message):
    try:
        for i in message['tempData']:
            # if i["templateType"] == 'M' and message['userData'][0].get('emailId'):
            #     Message_str = i["messageBody"].replace("[Name]", message['userData'][0]['userName']).replace(
            #         "[Vehicle type parking]", message['userData'][0]['vehicleTypeName']).replace("[parking name]", message['userData'][0]['parkingName'])
            #     Data = {"subject": i["subject"].replace(
            #         "[Vehicle type parking]", message['userData'][0]['vehicleTypeName']), "contact": message['userData'][0]['emailId'], "mail_content": Message_str}
            #     sendEmail(Data)
            if i["TemplateType"] == 'S' and message['MobileNo']!=None:
                sendSMS(i["Subject"], message['MobileNo'],i["MessageBody"].replace("[Link]",str(message['Link'])), i["Peid"], i["Tpid"])
    except Exception as e:
        print('error', str(e))
       
        
    
callbackDic = {
    'booking': bookingNotifications,
    'otp':otp,
    'paymentLink':paymentLink
}    


def callback(message):
    # pass
    # try:
    message = json.loads(message)
    print('mes', message)
    callbackDic[message['action']](message['body'])
    # except Exception as e:
    #     print('key error', str(e))