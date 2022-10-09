from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.conf import settings

from .serializers import ProjectSerializer
from .models import Project, Contributor

User = settings.AUTH_USER_MODEL

# =========================================================== PROJECT VIEW


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Create, retrieve, update and delete a project.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_project(self):
        lookup_field = self.kwargs["project_id"]
        return get_object_or_404(Project, id=lookup_field)

    def get_queryset(self):
        return Project.objects.filter(author_user_id=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save(author_user_id=self.request.user)
        Contributor.objects.create(
            user=request.user,
            project_id=project,
            role="Author",
            permission="All")

        return Response({
            'project': ProjectSerializer(project, context=self.get_serializer_context()).data,
            'message': "the project is successfully created"},
            status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            self.perform_destroy(instance)
            return Response(
                {'message': "the project is successfully deleted"},
                status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)