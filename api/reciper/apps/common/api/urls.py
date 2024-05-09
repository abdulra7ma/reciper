from django.urls import path

from reciper.apps.common.api.views import CreateFileView

urlpatterns = [
    path("files/upload/", CreateFileView.as_view(), name="create-file"),
]
