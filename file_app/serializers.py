
from rest_framework import serializers
from file_app.models import File, FileHashtags, Hashtag


class FileSerializer(serializers.ModelSerializer):

    class Meta():
        model = File
        read_only_fields = ('processed_image',)
        fields = ('custom_filter', 'file', 'file2', 'file3', 'action',
                  'timestamp', 'processed_image',)


class HashtagSerializer(serializers.ModelSerializer):

    class Meta():
        model = Hashtag
        fields = ('name',)
