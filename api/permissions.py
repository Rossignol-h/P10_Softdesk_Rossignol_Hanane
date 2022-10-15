from rest_framework.permissions import BasePermission
from django.http import Http404

from project.models import Contributor
# ================================================= ERROR MESSAGES

NOT_CONTRIBUTOR = "You are not a contributor of this project !"
NOT_PROJECT_AUTHOR = "You are not the author of this project !"
NOT_CONTENT_AUTHOR = "You are not the author of this content !"

# ================================================= PERMISSIONS CLASSES


class IsProjectOwner(BasePermission):
    """
    For GET detail request : check if the connected user is contributor of this project,
    For PUT AND DELETE : check if he is the author of this project.
    """

    def has_object_permission(self, request, view, obj):
        self.message = NOT_PROJECT_AUTHOR

        if view.action in ['retrieve']:
            self.message = NOT_CONTRIBUTOR
            current_project = view.get_project()
            contributors_of_current_project = Contributor.objects.filter(project_id=current_project)
            current_user = contributors_of_current_project.filter(user=request.user).exists()
            if current_user:
                return True
            else:
                return False

        if view.action in ['update','destroy'] and request.user == obj.author_user_id:
            return True
        return False


class IsContributorOrAuthor(BasePermission):
    """
    check if the connected user is Contributor of this project
    then check if he is the author of this Issue or comment;
    """
    def has_permission(self, request, view):
        self.message = NOT_CONTRIBUTOR
        if view.kwargs.get('project_id'):
            current_project = view.kwargs.get('project_id')
            contributors_of_current_project = Contributor.objects.filter(project_id=current_project)
            current_user = contributors_of_current_project.filter(user=request.user).exists()
            if current_user:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        self.message = NOT_CONTENT_AUTHOR

        if view.action in ['retrieve']:
            current_project = view.get_project()
            contributors_of_current_project = Contributor.objects.filter(project_id=current_project)
            current_user = contributors_of_current_project.filter(user=request.user).exists()
            if current_user:
                return True
            else:
                return False

        if view.action in ['update','destroy'] and request.user == obj.author_user_id:
            return True
        return False

class ContributorPermission(BasePermission):
    """
    check if the connected user is Author of this project
    """
    message = NOT_PROJECT_AUTHOR

    def has_permission(self, request, view):
        id = view.kwargs.get('project_id')
        if Contributor.objects.filter(project_id=id).exists():
            contributors_of_current_project = Contributor.objects.filter(
                project_id=id,
                user=request.user,
                role="Author",
                permission="All").exists()
            if contributors_of_current_project:
                return True
            return False
        raise Http404()
