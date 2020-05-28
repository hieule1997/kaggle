import smtplib,ssl
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import COMMASPACE, formatdate
from email import encoders
import base64

sender_email = "hoangcongsonbsoft@gmail.com"
receiver_email = "hieulm@vivas.vn"
password = 'hoangcongson'

def send_email():
    message = MIMEMultipart("alternative")
    message["Subject"] = "Report Anomaly"
    message["From"] = sender_email
    message["To"] = receiver_email

    msgAlternative = MIMEMultipart('alternative')
    message.attach(msgAlternative)

    html = """
    <p>Dear anh/chị!</p>
    <p>Kính gửi anh/chị báo cáo dịch vụ {} ngày {}</p>
    <p>Biểu đồ thể hiện bất thường doanh thu theo ngày: </p>
    <br>
    <img src="cid:image1" width="600" height="300">
    """.format('Vgame','11-02-2020')
    msgText = MIMEText(html, 'html')
    msgAlternative.attach(msgText)

    fp = open('vgame_DAILY_REVENUE.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    msgImage.add_header('Content-ID', '<image1>')
    message.attach(msgImage)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

if __name__ == "__main__":
    send_email()