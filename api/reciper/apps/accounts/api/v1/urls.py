from django.urls import path

from reciper.apps.accounts.api.v1.views.login import LoginView, LogoutView
from reciper.apps.accounts.api.v1.views.password import (
    ChangePasswordAPIView,
    ConfirmResetPasswordAPIView,
    ResetPasswordAPIView,
)
from reciper.apps.accounts.api.v1.views.registration import RegistrationAPIView
from reciper.apps.accounts.api.v1.views.social_inter import UnfollowUserView, ListFollowersView, ListFollowingView, \
    FollowUserView
from reciper.apps.accounts.api.v1.views.user_profile import UserProfileAPIView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", UserProfileAPIView.as_view(), name="user-profile"),
    path("password/", ChangePasswordAPIView.as_view(), name="change-password"),
    path("password/confirm/", ConfirmResetPasswordAPIView.as_view(), name="confirm-reset-password"),
    path("password/reset/", ResetPasswordAPIView.as_view(), name="reset-password"),
    path("registration/", RegistrationAPIView.as_view(), name="registration"),
    path('<uuid:user_id>/follow/', FollowUserView.as_view(), name='follow-user'),
    path('<uuid:user_id>/unfollow/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('<uuid:user_id>/followers/', ListFollowersView.as_view(), name='list-followers'),
    path('<uuid:user_id>/following/', ListFollowingView.as_view(), name='list-following'),
]
