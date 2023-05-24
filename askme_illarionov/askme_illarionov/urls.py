"""
URL configuration for askme_illarionov project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from askme import views

from . import settings

urlpatterns = [
    #path('<int:page>', views.paginate, name='index_page'),
    path('', views.index, name="index"),
    path('admin/', admin.site.urls),
    path('question/<int:question_id>/', views.question, name="question"),
    path('ask/', views.ask, name="ask"),
    path('settings/', views.settings, name='settings'),
    path('hot/', views.hot, name='hot'),
    path('tag/<str:tag>/', views.tag, name="tag"),
    path('login/', views.log_in, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('question_like/', views.question_like, name='question_like'),
    path('answer_like/', views.answer_like, name='answer_like'),
    path('mark_as_correct/', views.mark_as_correct, name='mark_as_correct'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
