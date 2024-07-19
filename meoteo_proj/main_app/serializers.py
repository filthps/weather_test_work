from rest_framework import serializers
from .models import History


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = "__all__"
    x = serializers.HiddenField()
    y = serializers.HiddenField()
