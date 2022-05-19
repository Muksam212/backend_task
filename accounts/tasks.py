from accounts.models import Account
from django.core.mail import send_mail

from backend_task import settings
from celery import shared_task


@shared_task(bind=True)
def send_mail_func(self):
	users = Account.objects.all()
	print(users,'----------------')
	for user in users:
		if user.birthday == '2022-5-18':
			mail_subject="Birthday Wish"
			message="Happy Birthday Sachin. Wish you a good success life ahead"

			to_email=user.email
			send_mail(
					subject=mail_subject,
					message=message,
					from_email=settings.EMAIL_HOST_USER,
					recipient_list=[to_email],
					fail_silently=True,
				)
		else:
			return HttpResponse("Failed to send")
	return "Done"