from rest_framework import serializers

class OwnerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    login = serializers.CharField()
    avatar_url = serializers.URLField()
    html_url = serializers.URLField()

class RepositorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    full_name = serializers.CharField()
    owner = OwnerSerializer()
    html_url = serializers.URLField()
    description = serializers.CharField()
    stargazers_count = serializers.IntegerField()
    language = serializers.CharField()
    forks_count = serializers.IntegerField()
    open_issues_count = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
