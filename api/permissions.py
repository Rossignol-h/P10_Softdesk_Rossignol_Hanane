from rest_framework.permissions import BasePermission
from django.http import Http404

from project.models import Contributor
# ================================================= ERROR MESSAGES

NOT_AUTHOR_CONTRIBUTOR = "You are not Author or Contributor of this project !"
NOT_CONTRIBUTOR = "You are not a contributor of this project !"
NOT_AUTHOR = "You are not the author of this project !"

# ================================================= PERMISSIONS CLASSES


class IsProjectOwner(BasePermission):
    """
    first check if the connected user is contributor of this project,
    then check if he is the author of this project.
    """
    # edit_methods = ("GET", "PUT", "DELETE")

    def has_permission(self, request, view):
        self.message = NOT_CONTRIBUTOR
        if request.method == 'POST':
            return request.user
        else:
            if view.kwargs.get('project_id'):
                current_project = view.kwargs.get('project_id')
                contributors_of_current_project = Contributor.objects.filter(project_id=current_project)
                current_user = contributors_of_current_project.filter(user=request.user).exists()
                if current_user:
                    return True
            else:
                return request.user.is_authenticated
            return False

    def has_object_permission(self, request, view, obj):
        self.message = NOT_AUTHOR

        if request.user == obj.author_user_id:
            return True
        return False


class IsContributorOrAuthor(BasePermission):
    """
    check if the connected user is Contributor of this project
    then check if he is the author of this Issue or comment;
    """

    message = NOT_AUTHOR_CONTRIBUTOR
    edit_methods = ("GET", "PUT", "DELETE")

    def has_permission(self, request, view):
        if view.kwargs.get('project_id'):
            current_project = view.kwargs.get('project_id')
            contributors_of_current_project = Contributor.objects.filter(project_id=current_project)
            current_user = contributors_of_current_project.filter(user=request.user).exists()
            if current_user:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.id != obj.author_user_id:
            return False
        return True


class ContributorPermission(BasePermission):
    """
    check if the connected user is Author of this project
    """
    message = NOT_AUTHOR

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
