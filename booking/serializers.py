from rest_framework import serializers

from .models import *


class AudiencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audiences
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    audiences = AudiencesSerializer(read_only=True, many=True)

    class Meta:
        model = Booking
        fields = "__all__"

