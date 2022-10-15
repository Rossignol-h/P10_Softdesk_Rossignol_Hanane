from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.http import Http404

from .serializers import IssueSerializer, CommentSerializer
from permissions import IsContributorOrAuthor
from .models import Issue, Comment
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
        lookup_field = self.kwargs['project_id']
        return get_object_or_404(Project, id=lookup_field)

    def get_queryset(self):
        current_project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return Issue.objects.filter(project_id=current_project).order_by('-last_updated')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            current_project = get_object_or_404(Project, pk=self.kwargs['project_id'])
            serializer.is_valid(raise_exception=True)
            new_issue = serializer.save(author_user_id=self.request.user, project_id=current_project)
            return Response({
                'New issue': IssueSerializer(new_issue, context=self.get_serializer_context()).data,
                'message': f"this issue is successfully added to the project : {current_project}"},
                status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            raise Http404

    def destroy(self, request, *args, **kwargs):
        try:
            current_project = get_object_or_404(Project, pk=self.kwargs['project_id'])
            issue_to_delete = Issue.objects.get(project_id=current_project, id=self.kwargs['pk'])

            if issue_to_delete:
                self.perform_destroy(issue_to_delete)
                return Response(
                        {'message': "This issue is successfully deleted"},
                        status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            raise ValidationError(detail="This issue doesn't exist")

# ================================================== COMMENT VIEW SECTION


class CommentViewSet(viewsets.ModelViewSet):
    """
    Create, retrieve, update and delete a comment of an issue.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsContributorOrAuthor]

    def get_project(self):
        lookup_field = self.kwargs['project_id']
        return get_object_or_404(Project, id=lookup_field)

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs['issue_id']).order_by('-last_updated')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            current_project = get_object_or_404(Project, pk=self.kwargs['project_id'])
            current_issue = get_object_or_404(Issue, pk=self.kwargs['issue_id'], project_id=current_project)

            if current_issue:
                serializer.is_valid(raise_exception=True)
                new_comment = serializer.save(author_user_id=self.request.user, issue_id=current_issue)
                return Response({
                    'New comment': CommentSerializer(new_comment, context=self.get_serializer_context()).data,
                    'message': f"this comment is successfully added to the issue : {current_issue}"},
                    status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            raise Http404

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            self.perform_destroy(instance)
            return Response(
                {'message': "this comment is successfully deleted"},
                status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
