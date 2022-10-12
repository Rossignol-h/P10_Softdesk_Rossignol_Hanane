from rest_framework import serializers
from .models import Issue, Comment

# =================================================== ISSUE SERIALIZE SECTION


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = "__all__"
        read_only_fields = ('project_id', 'author_user_id')

# =================================================== COMMENT SERIALIZE SECTION


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ('issue_id', 'author_user_id')
