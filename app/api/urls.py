from django.conf.urls import url

from .views import StartWork, StoptWork, ReportWork, Registration

urlpatterns = [
    url(r'register', Registration.as_view(), name='registration'),
    url(r'start-work', StartWork.as_view(), name='start_work'),
    url(r'stop-work', StoptWork.as_view(), name='stop_work'),
    url(r'report', ReportWork.as_view(), name='report'),
]
