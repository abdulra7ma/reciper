from django.db import models


class Tip(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ForeignKey('common.File', on_delete=models.SET_NULL, null=True, related_name='tips')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('accounts.UserAccount', on_delete=models.SET_NULL, null=True, related_name='tips')
    can_by_public = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class FavoriteTip(models.Model):
    user = models.ForeignKey('accounts.UserAccount', on_delete=models.CASCADE, related_name='favorite_tips')
    tip = models.ForeignKey(Tip, on_delete=models.CASCADE, related_name='users')

    def __str__(self):
        return f"{self.user.username} likes {self.tip.title}"

    class Meta:
        unique_together = ('user', 'tip')
