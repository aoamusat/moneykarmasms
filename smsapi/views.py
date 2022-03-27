from datetime import datetime
from smsapi.serializers import MessageSerializer
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from smsapi.auth import MessageRequestThrotlle, SMSAPIAuthentication
from smsapi.validators import *
from smsapi.models import PhoneNumber
from django.core.cache import cache

prefix = "THROTTLE_"

# Create your views here.
class IndexView(APIView):
    authentication_classes = [SMSAPIAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            "message": "You probably shouldn't be here, but...",
            "service": "MoneyKarma SMS API",
            "version": "1.0",
        }

        return JsonResponse(data=data, status=status.HTTP_200_OK)


class OutboundSMSView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SMSAPIAuthentication]
    throttle_classes = [MessageRequestThrotlle]

    def post(self, request):
        payload = {
            "frm": request.data.get("from"),
            "to": request.data.get("to"),
            "text": request.data.get("text"),
        }
        serializer = MessageSerializer(data=payload)

        if serializer.is_valid():
            to = request.data.get("to")
            text = request.data.get("text")
            frm = request.data.get("from")
            phone = PhoneNumber.objects.filter(account=request.user).filter(number=frm)

            if phone:
                if cache.get(to) is not None:
                    if cache.get(to) == frm:
                        return JsonResponse(
                            {
                                "message": f"SMS from {to} to {frm} blocked by STOP request"
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                if cache.get(prefix + frm) is not None:
                    prev_count = cache.get(prefix + frm).get("count")
                    prev_timestamp = cache.get(prefix + frm).get("created_at")
                    cache.set(
                        prefix + frm,
                        {"created_at": prev_timestamp, "count": prev_count + 1},
                        timeout=3600 * 24,
                    )
                else:
                    cache.set(
                        prefix + frm,
                        {
                            "created_at": datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
                            "count": 1,
                        },
                        timeout=3600 * 24,
                    )
                return JsonResponse({"message": "Outbound SMS Ok!"})
            else:
                return JsonResponse(
                    {
                        "message": "<from> parameter not found for user: "
                        + request.user.username
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InboundSMSView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SMSAPIAuthentication]

    def post(self, request):
        payload = {
            "frm": request.data.get("from"),
            "to": request.data.get("to"),
            "text": request.data.get("text"),
        }

        serializer = MessageSerializer(data=payload)

        if serializer.is_valid():
            to = request.data.get("to")
            text = request.data.get("text")
            frm = request.data.get("from")
            phone = PhoneNumber.objects.filter(account=request.user).filter(number=to)
            if phone:
                if text in ["STOP", "STOP\n", "STOP\r", "STOP\r\n"]:
                    cache.set(frm, to, timeout=3600 * 4)
                return JsonResponse({"message": "Inbound SMS Ok!"})
            else:
                return JsonResponse(
                    {
                        "message": "<to> parameter not found for user: "
                        + request.user.username
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
