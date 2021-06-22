from .models import CustomFilters
from rest_framework import serializers


class CustomFiltersSerializer(serializers.ModelSerializer):

    class Meta():
        model = CustomFilters
        read_only_fields = ('id',)
        fields = ('id', 'name', 'action', 'is_active', 'user')
