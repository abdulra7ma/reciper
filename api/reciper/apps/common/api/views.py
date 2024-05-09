from drf_spectacular.utils import extend_schema

from reciper.apps.common.models import File

from rest_framework import renderers
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FileUploadParser

from reciper.apps.common.api.serializers import FileSerializer


@extend_schema(tags=["Documents"], responses={200: FileSerializer})
class CreateFileView(CreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser, FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)

    def perform_create(self, serializer):
        serializer.save()
