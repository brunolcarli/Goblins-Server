"""game_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
import pathlib
import django
from django.contrib import admin
from django.urls import path

from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from graphql import GraphQLCoreBackend


class GraphQLCustomCoreBackend(GraphQLCoreBackend):
    def __init__(self, executor=None):
        super().__init__(executor)
        self.execute_params['allow_subscriptions'] = True

def subscriptions(request):
    """Trivial view to serve the `graphiql.html` file."""
    del request
    graphiql_filepath = pathlib.Path(__file__).absolute().parent / "subscriptions.html"
    with open(graphiql_filepath) as f:
        return django.http.response.HttpResponse(f.read())


urlpatterns = [
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, backend=GraphQLCustomCoreBackend()))),
    django.urls.path("", subscriptions),
    django.urls.path("admin", django.contrib.admin.site.urls),
]
