from django.core.mail import EmailMessage

email = EmailMessage(
    'Subject',
    'Body goes here',
    'from@example.com',
    ['to@example.com'],
)
email.send()