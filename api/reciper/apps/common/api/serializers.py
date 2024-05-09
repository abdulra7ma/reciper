from rest_framework import serializers

from reciper.apps.common.models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = [
            "id",
            "file",
        ]

    def save(self, **kwargs):
        kwargs.update({"uploaded_by": self.context.get("request").user})
        return super().save(**kwargs)
