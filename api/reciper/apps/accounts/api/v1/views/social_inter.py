from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from reciper.apps.accounts.api.v1.serializers.user_profile import UserProfileSerializer
from reciper.apps.accounts.models import UserAccount
from reciper.apps.accounts.models.user_account import Follower


@extend_schema_view(
    post=extend_schema(summary="Follow a user", tags=["Social Interactions"]),
)
class FollowUserView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_follow = UserAccount.objects.get(id=user_id)
            if Follower.objects.filter(follower=request.user, following=user_to_follow).exists():
                return Response({'error': 'Already following'}, status=status.HTTP_409_CONFLICT)
            Follower.objects.create(follower=request.user, following=user_to_follow)
            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        except UserAccount.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@extend_schema_view(
    delete=extend_schema(summary="Unfollow a user", tags=["Social Interactions"]),
)
class UnfollowUserView(views.APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        try:
            user_to_unfollow = UserAccount.objects.get(id=user_id)
            follow_instance = Follower.objects.filter(follower=request.user, following=user_to_unfollow)
            if not follow_instance.exists():
                return Response({'error': 'Not following'}, status=status.HTTP_404_NOT_FOUND)
            follow_instance.delete()
            return Response({'status': 'success'}, status=status.HTTP_204_NO_CONTENT)
        except UserAccount.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@extend_schema_view(
    get=extend_schema(summary="List followers of a user", tags=["Social Interactions"]),
)
class ListFollowersView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = UserAccount.objects.filter(id=user_id).first()
        if user:
            followers = Follower.objects.filter(following=user)
            serializer = UserProfileSerializer([follower.follower for follower in followers], many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@extend_schema_view(
    get=extend_schema(summary="List users a user is following", tags=["Social Interactions"]),
)
class ListFollowingView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = UserAccount.objects.filter(id=user_id).first()
        if user:
            following = Follower.objects.filter(follower=user)
            serializer = UserProfileSerializer([following.following for following in following], many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
