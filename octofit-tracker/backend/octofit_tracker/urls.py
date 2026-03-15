"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from octofit_tracker.views import UserViewSet, TeamViewSet, ActivityViewSet, WorkoutViewSet, LeaderboardViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view

CODESPACE_NAME = os.environ.get('CODESPACE_NAME')
CODESPACE_BASE_URL = (
    f"https://{CODESPACE_NAME}-8000.app.github.dev" if CODESPACE_NAME else None
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'workouts', WorkoutViewSet)
router.register(r'leaderboard', LeaderboardViewSet)

@api_view(['GET'])
def api_root(request, format=None):
    """Return API root links.

    If running inside a GitHub Codespace, build absolute links using the
    $CODESPACE_NAME proxy domain to avoid HTTPS/certificate issues.
    """

    if CODESPACE_BASE_URL:
        base = CODESPACE_BASE_URL
    else:
        base = request.build_absolute_uri('/')[:-1]

    def url(path: str) -> str:
        return f"{base}{path}"

    return Response({
        'users': url('/api/users/'),
        'teams': url('/api/teams/'),
        'activities': url('/api/activities/'),
        'workouts': url('/api/workouts/'),
        'leaderboard': url('/api/leaderboard/'),
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root, name='api-root'),
    path('api/', include(router.urls)),
]
