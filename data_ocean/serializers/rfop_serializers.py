from rest_framework import serializers

class RfopSerializer(serializers.Serializer):
    id = serializers.CharField()
    state_id = serializers.CharField()
    state = serializers.CharField()
    kved_id = serializers.CharField()
    kved = serializers.CharField()
    fullname = serializers.CharField()
    address = serializers.CharField()