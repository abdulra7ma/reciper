from rest_framework import serializers

from reciper.apps.accounts.models import UserAccount
from reciper.apps.accounts.models.user_account import Follower


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    def get_followers(self, obj):
        return Follower.objects.filter(following=obj).count()

    def get_following(self, obj):
        return Follower.objects.filter(follower=obj).count()

    class Meta:
        model = UserAccount
        fields = ('id', "email", "first_name", "last_name", "followers", "following")
