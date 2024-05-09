from django.db import models


class File(models.Model):
    file = models.FileField(upload_to="files/", blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    uploaded_by = models.ForeignKey(
        "accounts.UserAccount", null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return str(self.file.name)

    @property
    def is_valid(self):
        """
        We consider a file "valid" if the datetime flag has value.
        """
        return bool(self.upload_finished_at)
