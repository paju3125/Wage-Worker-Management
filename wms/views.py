from email import message
from http.client import HTTPResponse
from pyexpat import model
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.db import connection
from admin_app import models
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import random
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def index(request):
    if request.session.has_key('loginData'):
        all_data = models.Users.objects.filter(
            email=request.session['loginData'][0], password=request.session['loginData'][1]).values()

        if all_data[0]['designation'] == 'Security':
            return redirect("/project/security")
        elif all_data[0]['designation'] == 'Supervisor':
            return redirect("/project/supervisor")
        if all_data[0]['designation'] == 'Plant head':
            return redirect("/project/plantHead")
        else:
            return redirect("/admin")

    else:
        if request.session.has_key('messages'):
            del request.session['messages']
        return render(request, "index.html")


def login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        all_data = models.Users.objects.filter(
            email=email, password=password).values()

        try:
            del request.session['messages']
        except KeyError:
            pass
        
        if len(all_data) == 0:
            # messages.error(request, 'Invalid Credintials')
            return redirect('index')

        else:
            messages.success(request, 'You are logged in successfully')
            try:
                del request.session['loginData']
            except KeyError:
                pass

            request.session['loginData'] = [
                email, password, all_data[0]['designation']]

            if all_data[0]['designation'] == "Supervisor":
                return redirect("/project/supervisor")

            elif all_data[0]['designation'] == "Plant head":
                return redirect("/project/plantHead")

            elif all_data[0]['designation'] == "Security":
                return redirect("/project/security")
                # return render(request, "security.html")

            else:
                return redirect("/admin/")


# To log out the user
def logout(request):
    try:
        del request.session['loginData']
        # del request.session['messages']
        return redirect('/')
    except KeyError:
        pass


# To verify email and send OTP for change passsword request
def verifyOTP(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        email = request.GET.get('email')
        data = models.Users.objects.filter(email=email)
        if list(data) != []:
            otp = random.randrange(100000,999999)
            
            sender_email = "prajvalgandhi@gmail.com"
            password = "eyitiqdjkbqyxfjd"
            receiver_email = email

            message = MIMEMultipart("alternative")
            message["Subject"] = "Wage Worker Management System : Password change"
            message["From"] = sender_email
            message["To"] = receiver_email

            # Create the plain-text and HTML version of your message
            text = """\
            Verify your Email address to change password"""
            html = f"""\
            <html>
            <body>
                <h3>Verify your Email address to change password</h3>
                <br>
                <h3>OTP : {otp}</h3>
            </body>
            </html>
            """

            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")

            message.attach(part1)
            message.attach(part2)

            # Create secure connection with server and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(
                    sender_email, receiver_email, message.as_string()
                )
    
            return JsonResponse({'status': True,'OTP':otp,'email':email})

        else:
            return JsonResponse({'status':False})
    return JsonResponse({'status':False})
    
    
# To change password
def changePassword(request):
   if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
       email = request.GET.get('email') 
       password = request.GET.get('password')
       
       user = models.Users.objects.get(email = email)
       user.password = password
       user.save()
       return JsonResponse({'status':True})
   return JsonResponse({'status':False})