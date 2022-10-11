from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets

from .serializers import IssueSerializer
from permissions import IsContributorOrAuthor
from .models import Issue
from project.models import Project


# ================================================== ISSUE VIEW SECTION


class IssueViewSet(viewsets.ModelViewSet):
    """
    Create, retrieve, update and delete issue of a project.
    """
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsContributorOrAuthor]

    def get_project(self):
        lookup_field = self.kwargs['id']
        return get_object_or_404(Project, id=lookup_field)

    def get_queryset(self):
        id_project = get_object_or_404(Project, pk=self.kwargs['id'])
        return Issue.objects.filter(project_id=id_project)

    def perform_create(self, serializer):
        id_project = get_object_or_404(Project, pk=self.kwargs['id'])
        serializer.save(author_user_id=self.request.user, project_id=id_project)

    def destroy(self):
        instance = self.get_object()
        if instance:
            self.perform_destroy(instance)
            return Response(
                {'message': "this issue is successfully deleted"},
                status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)