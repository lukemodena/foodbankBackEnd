from rest_framework.parsers import JSONParser
from rest_framework import generics
from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

from django.core.mail import EmailMessage
# Create your views here.

class emailApi(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.method == 'POST':
            email_data=JSONParser().parse(request)
            subject = email_data['Subject']
            emailFrom = settings.EMAIL_HOST_USER
            body = email_data['Body']
            emailTo = email_data['Emails']

            try:
                emailMessage = EmailMessage(subject, body, emailFrom, bcc=emailTo)

                emailMessage.send()
                

                return JsonResponse("Email sent successfully!", safe=False)

            except Exception as err:

                return JsonResponse(f"Failed to send email, due to unexpected {err=}, {type(err)=}", safe=False)
        else:
            return JsonResponse("Failed to send email, due to invalid request type (must be a POST request)", safe=False)

