from random import randint
from django.core.mail import send_mail

def generate_otp():
    return str(randint(100000, 999999)) 

def send_otp_email(email, otp):
    subject = "Your OTP for Login"
    message = f"Your OTP for Login is -> {otp}"
    send_mail(
        subject,
        message,
        'heruko299@gmail.com', 
        [email]
    )