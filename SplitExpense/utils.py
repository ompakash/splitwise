import asyncio
from django.core.mail import send_mail
from django.conf import settings
from asgiref.sync import sync_to_async

# def send_mail_to_user():
#     send_mail(
#         'contact form',
#         'this is message',
#         'setting.EMAIL_HOST_USER',
#         ['opytc2@gmail.com','ompsofficial@gmail.com'],
#         fail_silently=False
#     )
  
# async def send_mail_to_user_async(contact_form, message, email_list):
#     send_mail(
#         contact_form,
#         message,
#         settings.EMAIL_HOST_USER, 
#         email_list,
#         fail_silently=False
#     )

# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(send_mail_to_user_async())
