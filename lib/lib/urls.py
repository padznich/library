"""lib URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.models import User

from rest_framework import routers, serializers, viewsets
from rest_framework.urlpatterns import format_suffix_patterns

from app_db import views


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # rest authentication
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # app_db_view
    url(r'^app_db/$', views.app_db_list),
    url(r'^app_db/(?P<pk>[0-9]+)$', views.app_db_detail),

    url(r'^capp_db/$', views.AppdbList.as_view()),
    url(r'^capp_db/(?P<pk>[0-9]+)$', views.AppdbDetail.as_view()),

    url(r'^sapp_db/$', views.SnippetList.as_view()),
    url(r'^sapp_db/(?P<pk>[0-9]+)$', views.SnippetDetail.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
