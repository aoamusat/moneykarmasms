from smsapi.views import InboundSMSView, IndexView, OutboundSMSView
from django.urls import path

urlpatterns = [
    path("", IndexView.as_view(), name="api.index"),
    path("inbound/sms", InboundSMSView.as_view()),
    path("outbound/sms", OutboundSMSView.as_view()),
]
