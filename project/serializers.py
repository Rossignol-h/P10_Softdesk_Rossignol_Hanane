from rest_framework.serializers import ModelSerializer
from .models import Project, Contributor

# ================================================== PROJECT SERIALIZER


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['author_user_id']

# ================================================== CONTRIBUTOR SERIALIZER


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = '__all__'
        read_only_fields = ['project_id', 'permission', 'role']
