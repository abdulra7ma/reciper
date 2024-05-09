from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy

from reciper.apps.common import models as core_models
from reciper.apps.common.models import CoreModel


class UserManager(core_models.CoreManager, BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must give an email address")

        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class UserAccount(PermissionsMixin, CoreModel, AbstractBaseUser):
    email = models.EmailField(verbose_name=gettext_lazy("email address"), unique=True)
    username = models.CharField(verbose_name=gettext_lazy("username"), max_length=150, unique=True)
    first_name = models.CharField(verbose_name=gettext_lazy("first name"), max_length=150, blank=True)
    last_name = models.CharField(verbose_name=gettext_lazy("last name"), max_length=150, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(blank=True)
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    is_staff = models.BooleanField(
        gettext_lazy("staff status"),
        default=False,
        help_text=gettext_lazy("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        gettext_lazy("active"),
        default=True,
        help_text=gettext_lazy(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ("first_name", "last_name")

    def __str__(self):
        return self.email

    def get_short_name(self) -> str:
        return str(self.email)

    def get_full_name(self) -> str:
        if self.first_name and self.last_name:
            full_name = f"{self.first_name} {self.last_name} <{self.email}>"
        else:
            full_name = self.get_short_name()
        return full_name

    @property
    def notification_salutation(self):
        if self.first_name and self.last_name:
            salutation = f"{self.first_name} {self.last_name}"
        else:
            salutation = gettext_lazy("Dear client")
        return salutation


class Follower(models.Model):
    follower = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="followers")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name='unique_followers')
        ]

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
