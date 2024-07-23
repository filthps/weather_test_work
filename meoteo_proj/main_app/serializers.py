from rest_framework import serializers
from .models import History


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = History
        exclude = ("user",)
    city_name = serializers.CharField(label="", help_text="Начните вводить название города")
    x = serializers.HiddenField(default="")
    y = serializers.HiddenField(default="")

    def create(self, validated_data):
        user_id = getattr(self, "user", None)  # Из view
        if user_id is None:
            raise ValueError("Передайте в валидатор ")
        validated_data.update({"user": user_id})
        return super().create(validated_data)
