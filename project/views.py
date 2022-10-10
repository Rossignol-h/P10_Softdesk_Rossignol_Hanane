from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.conf import settings

from .serializers import ProjectSerializer, ContributorSerializer
from permissions import IsProjectOwner, ContributorPermission
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

# =========================================================== CONTRIBUTOR VIEWS


class ContributorViewSet(viewsets.ModelViewSet):
    """
    Add, retrieve, update and delete contributor to a project.
    """

    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()
    permission_classes = [IsAuthenticated, ContributorPermission]

    def get_queryset(self):
        """ retrieve all contributors"""
        id_project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return Contributor.objects.filter(project_id=id_project)

    def create(self, request, *args, **kwargs):
        id_project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        user = request.data['user']
        queryset = Contributor.objects.filter(user=user, project_id=id_project)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if queryset:
            return Response({
                    "message": "This user is already a contributor."},
                    status=status.HTTP_403_FORBIDDEN)

        else:
            contribution = serializer.save(project_id=id_project)
            return Response({'contribution': ContributorSerializer(contribution,
                            context=self.get_serializer_context()).data,
                            'message': "This new contributor is successfully added to the project."},
                            status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        try:
            get_object_or_404(Project, pk=self.kwargs['project_id'])
            contributor_to_delete = Contributor.objects.get(
                project_id=self.kwargs['project_id'],
                user=self.kwargs['pk'])

            if contributor_to_delete.role == "Author":
                return Response(
                    {'message': "The author can't be deleted !"},
                    status=status.HTTP_403_FORBIDDEN)
            else:
                self.perform_destroy(Contributor.objects.filter(
                    user=self.kwargs['pk'],
                    project_id=self.kwargs['project_id']))
                return Response(
                        {'message': "This contributor is successfully deleted"},
                        status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            raise ValidationError("This contributor doesn't exist")
