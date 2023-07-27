from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from pybars import Compiler
from xhtml2pdf import pisa 


def sendEmail(Data):
    print("mail Data",Data["subject"],Data["contact"])
    sender_address = 'prematixdev@gmail.com'
    sender_pass = 'yunvuhkngyjzirob'
    receiver_address = Data["contact"]
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = Data["subject"]
    message.attach(MIMEText(Data["mail_content"], 'plain'))
    if Data.get('html'):
        message.attach(MIMEText(Data["html"], 'html'))
    if Data.get('pdf'):
        result_file = open('invoice.pdf', "w+b") # w+b to write in binary mode.

        # convert HTML to PDF
        pisa_status = pisa.CreatePDF(
                Data["pdf"],                   # the HTML to convert
                dest=result_file           # file handle to recieve result
        )           

        # close output file
        result_file.close()

        result = pisa_status.err
        if not result:
           pdfname = 'invoice.pdf'

            # open the file in bynary
           binary_pdf = open(pdfname, 'rb')

           payload = MIMEBase('application', 'octate-stream', Name=pdfname)
           payload.set_payload((binary_pdf).read())

           # enconding the binary into base64
           encoders.encode_base64(payload)

           # add header with pdf name
           payload.add_header('Content-Decomposition', 'attachment', filename=pdfname)
           message.attach(payload) 
        
    session = smtplib.SMTP('smtp.gmail.com',587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()

    return {"statusCode": 1, "response": "E-Mail Sent Sucessfully!"}



def sendAttachMent(Data):
    compiler = Compiler()

    # Compile the template

    with open("routers/services/receipt.html", "r") as f:
        source= f.read()

    template = compiler.compile(source)

    # Render the template
    
    output = template({
        'PaymentDate': Data['PaymentDate'],
        'BookingId':Data['BookingId'],
        'AppName':Data['AppName'],
        'totalAmount':Data['totalAmount'],
        'taxAmount':Data['taxAmount'],
        'paymenttype':Data['paymenttype'],
        'GuestName':Data['GuestName']
        })

    return output

def sendPdf(Data):
    compiler = Compiler()

    # Compile the template

    with open("routers/services/invoice.html", "r") as f:
        source= f.read()

    template = compiler.compile(source)

    # Render the template
    
    output = template({
        'PaymentDate': Data['PaymentDate'],
        'BookingId':Data['BookingId'],
        'AppName':Data['AppName'],
        'Amount':Data['totalAmount'],
        'GuestName':Data['GuestName']
        })

    return output