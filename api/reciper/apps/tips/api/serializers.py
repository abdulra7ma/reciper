from rest_framework import serializers

from reciper.apps.tips.models import Tip, FavoriteTip


class TipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tip
        fields = ['id', 'title', 'content', 'image', 'created_at']


class FavoriteTipSerializer(serializers.ModelSerializer):
    tip = TipSerializer(read_only=True)
    tip_id = serializers.PrimaryKeyRelatedField(
        queryset=Tip.objects.all(), write_only=True, source='tip'
    )

    class Meta:
        model = FavoriteTip
        fields = ['id', 'tip', 'tip_id']

    def create(self, validated_data):
        # Ensure we do not duplicate favorite tips
        favorite_tip, created = FavoriteTip.objects.get_or_create(
            user=self.context['request'].user, **validated_data)
        return favorite_tip
