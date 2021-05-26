import time
import time
import math
import traceback  # dung cho tinh toan noi suy
import sys  # dung cho tinh toan noi suy
from builtins import property
from datetime import datetime
import numpy as np
from dateutil.relativedelta import relativedelta
from pathlib import _Selector
# from rbi import MYSQL_CAL as DAL_CAL
# from pyglet.input.carbon_hid import Self

from django.core.mail import EmailMessage
from cloud import models
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SendEmail:
    # def config_send_email(self,receiver_email,subject,content):
    #     try:
    #         port = 465  # For SSL
    #         smtp_server = "sg1-ss16.a2hosting.com"
    #         sender_email = "nguyenthihai@cortekrbi.com"  # Enter your address
    #         # receiver_email = "luongvancuongkmhd1998@gmail.com"  # Enter receiver address
    #         password = "nguyenthihai"
    #         # content="Thong tin du lieu yeu cau cua ban ghi nay da duoc gui di"
    #         # subject= "Da gui yeu cau thanh cong"
    #         message = """From: From CortekRBI <nguyenthihai@cortekrbi.com>
    #         To: To Person <"""+receiver_email+""">
    #         MIME-Version: 1.0
    #         Content-type: text/html
    #         Subject: """ + subject + """
    #         Du lieu da duoc cap nhat
    #         <b>Phia doi tac can cung cap them du lieu</b>
    #         <h1>Kiem thu</h1>
    #         """ + content
    #         print(receiver_email)
    #         # context = ssl.create_default_context()
    #         server =  smtplib.SMTP_SSL(smtp_server, port)
    #         server.login(sender_email, password)
    #         print("go here")
    #         server.sendmail(sender_email, receiver_email, message)
    #         print("done done")
    #     except Exception as e:
    #         print("error in config",e)
    def email_for_post(self, request, postID):
        try:
            id_user = models.ZPosts.objects.all().filter(id=postID)[0].id_user  # Lấy ID người đăng bài
            title_post = models.ZPosts.objects.all().filter(id=postID)[0].title
            to_email = models.ZUser.objects.get(id=id_user).email_service
            try:
                if request.session['id'] != id_user:
                    UserID = models.Sites.objects.filter(userID_id=request.session['id'])[0].userID_id
                    nameUserComment = models.ZUser.objects.get(id=UserID).name
                    # subject = "Thong bao tu dich vu RBI-Cloud Forum"
                    # message = str(nameUserComment) + " da phan hoi bai viet " + "'"+str(title_post)+"'"
                    gmail_user = 'nguyenthihai@cortekrbi.com'
                    gmail_pass = 'nguyenthihai2104'
                    sent_from = gmail_user
                    to = to_email
                    print('qq', to)
                    subject = " Notification from the RBI-Cloud Forum service"
                    body = str(nameUserComment) + " have responded to the post " + "'" + str(title_post) + "'"
                    msg = MIMEMultipart()
                    msg['To'] = to_email
                    msg['From'] = gmail_user
                    msg['subject'] = subject
                    msg.attach(MIMEText(body, 'plain'))
                    message = msg.as_string()
                    email_text = """\
                               From: %s
                               To: %s
                               Subject: %s

                               %s
                               """ % (sent_from, ", ".join(to), subject, body)
                    server = smtplib.SMTP_SSL('sg1-ss16.a2hosting.com', 465)
                    server.ehlo()
                    server.login(gmail_user, gmail_pass)
                    server.sendmail(sent_from, to, message)
                    server.close()
                    # print(message,to_email)
                    # Email = EmailMessage(subject, message, to=[to_email])
                    # Email.send()
                    print("sent mail")
            except Exception as e:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        except Exception as e:
            print("error in email_for_post", e)

    def email_for_request(self, proposalID, componentID, equipmentID, siteID):
        try:
            componentName = models.ComponentMaster.objects.get(componentid=componentID).componentnumber
            equipName = models.EquipmentMaster.objects.get(equipmentid=equipmentID)
            facilityName = models.Facility.objects.get(facilityid=equipName.facilityid_id)
            site = models.Sites.objects.get(siteid=siteID)
            to_email = models.ZUser.objects.get(id=site.userID_id).email_service
            print('tt', to_email)
            gmail_user = 'nguyenthihai@cortekrbi.com'
            gmail_pass = 'nguyenthihai2104'
            sent_from = gmail_user
            to = to_email
            subject = " Notification from Regulatory Authority, Inspection requirement "
            body = "Requiment Factory to reinspection the Component " + "'" + str(
                componentName) + "'" + "\n belong to Equipment : " + str(
                equipName.equipmentnumber) + "," + " \n belong to Facility: " + str(facilityName.facilityname)
            # subject="Thong bao tu Co Quan Quan Li, yeu cau kiem dinh"
            # message = "Yeu cau co so nha may kiem dinh lai Component "+"'"+str(componentName)+"'"+" \n thuoc thiet bi :"+str(equipName.equipmentnumber)+","+" \n co so nha may: "+ str(facilityName.facilityname)
            # Email = EmailMessage(subject, message, to=[to_email])
            # Email.send()
            msg = MIMEMultipart()
            msg['To'] = to_email
            msg['From'] = gmail_user
            msg['subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            message = msg.as_string()
            email_text = """\
                                           From: %s
                                           To: %s
                                           Subject: %s

                                           %s
                                           """ % (sent_from, ", ".join(to), subject, body)
            server = smtplib.SMTP_SSL('sg1-ss16.a2hosting.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_pass)
            server.sendmail(sent_from, to, message)
            server.close()
        except Exception as e:
            print(e)

    def email_for_response(self, request, faclityID, reportID, comID, equipID):
        try:
            print("cuong1")
            facilityName = models.Facility.objects.get(facilityid=faclityID)
            equipName = models.EquipmentMaster.objects.get(equipmentid=equipID)
            comName = models.ComponentMaster.objects.get(componentid=comID)
            to_email = models.ZUser.objects.filter(kind="manager")[0].email_service
            gmail_user = 'nguyenthihai@cortekrbi.com'
            gmail_pass = 'nguyenthihai2104'
            sent_from = gmail_user
            to = to_email
            subject = "Factory inspection require report: " + str(facilityName.facilityname)
            body = "Report : Data and inspection results for Component " + "'" + str(
                comName.componentnumber) + "'" + " \n belong to Equipment " + "'" + str(
                equipName.equipmentnumber) + "'," + "\n belong to Facility:" + str(facilityName.facilityname)
            # subject = "Bao cao yeu cau kiem dinh tu nha may: " + str(facilityName.facilityname)
            # message = "Bao Cao: Du lieu va ket qua kiem dinh cho thanh phan" + "'"+str(comName.componentnumber) +"'"+ " \n thuoc thiet bi" + "'"+str(equipName.equipmentnumber)+"',"+"\nthuoc co so nha may:"+str(facilityName.facilityname)
            # Email = EmailMessage(subject, message, to=[to_email])
            # Email.send()
            msg = MIMEMultipart()
            msg['To'] = to_email
            msg['From'] = gmail_user
            msg['subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            message = msg.as_string()
            email_text = """\
                                                       From: %s
                                                       To: %s
                                                       Subject: %s

                                                       %s
                                                       """ % (sent_from, ", ".join(to), subject, body)
            server = smtplib.SMTP_SSL('sg1-ss16.a2hosting.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_pass)
            server.sendmail(sent_from, to, message)
            server.close()
        except Exception as e:
            print(e)