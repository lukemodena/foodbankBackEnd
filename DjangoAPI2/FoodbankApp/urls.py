from FoodbankApp.views import donorApiFliter, DonorApi, collectionApiFliter, collectionApiStatus, CollectionApi, WholesaleApi, wholesaleApiFliter, ParticipantAPI, participantApiFliter, ParticipantListApi, PhotoAPI, SpreadsheetAPI
from django.urls import re_path

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    re_path(r'^donor$', DonorApi.as_view()),
    re_path(r'^donor/([0-9]+)$', DonorApi.as_view()),

    re_path(r'^wholesale$', WholesaleApi.as_view()),
    re_path(r'^wholesale/(?P<collid>.+)/$', WholesaleApi.as_view()),
    re_path(r'^wholesale/([0-9]+)$', WholesaleApi.as_view()),

    re_path(r'^searchwholesale$', wholesaleApiFliter.as_view()),
    re_path(r'^searchwholesale/(?P<collid>.+)/$', wholesaleApiFliter.as_view()),

    re_path(r'^participants$', ParticipantAPI.as_view()),
    re_path(r'^participants/(?P<collid>.+)/$', ParticipantAPI.as_view()),
    re_path(r'^participants/([0-9]+)$', ParticipantAPI.as_view()),

    re_path(r'^searchparticipants$', participantApiFliter.as_view()),
    re_path(r'^searchparticipants/(?P<collid>.+)&(?P<donid>.+)/$', participantApiFliter.as_view()),

    re_path(r'^searchdonors$', donorApiFliter.as_view()),
    re_path(r'^searchdonors/(?P<page>.+)&(?P<type>.+)&(?P<fullname>.+)&(?P<donid>.+)/$', donorApiFliter.as_view()),

    re_path(r'^collectionstatus$', collectionApiStatus.as_view()),
    re_path(r'^collectionstatus/(?P<status>.+)/$', collectionApiStatus.as_view()),

    re_path(r'^searchcollections$', collectionApiFliter.as_view()),
    re_path(r'^searchcollections/(?P<page>.+)&(?P<status>.+)&(?P<startdate>.+)&(?P<enddate>.+)&(?P<type>.+)/$', collectionApiFliter.as_view()),

    re_path(r'^collection/(?P<date>.+)/$', CollectionApi.as_view()),
    re_path(r'^collection$', CollectionApi.as_view()),
    re_path(r'^collection/([0-9]+)$', CollectionApi.as_view()),

    re_path(r'^listparticipants$', ParticipantListApi.as_view()),
    re_path(r'^listparticipants/(?P<page>.+)&(?P<collid>.+)&(?P<fullname>.+)&(?P<type>.+)/$', ParticipantListApi.as_view()),

    re_path(r'^Collection/FileHandle$', PhotoAPI.as_view()),
    re_path(r'^spreadsheet$', SpreadsheetAPI.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)