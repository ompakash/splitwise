import logging
from SplitExpense.views import ShowDetails
from SplitExpense.models import *
logger = logging.getLogger(__name__)
from django.core.mail import send_mail
from django.conf import settings


def send_mail_weekly():
    show_details = ShowDetails()
    all_users = User.objects.all()
    list1 = []
    for user in all_users:
        details = show_details.show(user)
        list1.append(details)
        user_email = []
        user_email.append(str(user.email))
        try:
            send_mail("Expense Notification",str(details),settings.EMAIL_HOST_USER,user_email,fail_silently=False)
        except Exception as e:
            print(e)
    print(list1)