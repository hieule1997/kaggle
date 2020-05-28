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

message = MIMEMultipart("alternative")
message["Subject"] = "Report Anomaly"
message["From"] = sender_email
message["To"] = receiver_email


# msg = MIMEImage(open("logo_dfs.jpg", "rb").read())

with open("logo_dfs.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
# part = MIMEBase('application', "octet-stream")
# part.set_payload(open("logo_dfs.jpg", "rb").read())
# encoders.encode_base64(msg)
# print(encoded_string.decode("utf-8"))
#    <img src="data:image/jpg;base64,{}" width="100" height="50" alt="base64 test"/>
    # <p class="MsoNormal"><img width="600" height="300" src="{}"></p>


# msg.add_header('Content-Disposition', 'attachment; filename="logo_dfs.jpg"')

# message.attach(msg)
# Turn these into plain/html MIMEText objects
# part1 = MIMEText(text, "plain")
msgAlternative = MIMEMultipart('alternative')
message.attach(msgAlternative)

msgText = MIMEText('This is the alternative plain text message.')
msgAlternative.attach(msgText)

# We reference the image in the IMG SRC attribute by the ID we give it below

html = """
<p>Dear anh/chị!</p>
<p>Kính gửi anh/chị báo cáo dịch vụ {} ngày {}</p>
<p>Biểu đồ thể hiện bất thường doanh thu theo ngày: </p>
<br>
<img src="cid:image1" width="600" height="300">
""".format('Vgame','11-02-2020')
msgText = MIMEText(html, 'html')
msgAlternative.attach(msgText)

# This example assumes the image is in the current directory
fp = open('vgame_DAILY_REVENUE.png', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()

# Define the image's ID as referenced above
msgImage.add_header('Content-ID', '<image1>')
message.attach(msgImage)

# part2 = MIMEText(html, "html")
# message.attach(part2)
# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
# message.attach(part2)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )