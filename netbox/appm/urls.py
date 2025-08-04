from django.urls import include, path

from utilities.urls import get_model_urls
from . import views

app_name = 'appm'
urlpatterns = [

    # Application groups
    path('application-groups/', include(get_model_urls('appm', 'applicationgroup', detail=False))),
    path('application-groups/<int:pk>/', include(get_model_urls('appm', 'applicationgroup'))),

    # Applications
    path('applications/', include(get_model_urls('appm', 'application', detail=False))),
    path('applications/<int:pk>/', include(get_model_urls('appm', 'application'))),

    # Application servers
    path('application-servers/', include(get_model_urls('appm', 'applicationserver', detail=False))),
    path('application-servers/<int:pk>/', include(get_model_urls('appm', 'applicationserver'))),

    # Application endpoints
    path('application-endpoints/', include(get_model_urls('appm', 'applicationendpoint', detail=False))),
    path('application-endpoints/<int:pk>/', include(get_model_urls('appm', 'applicationendpoint'))),

    # Application personnel
    path('application-personnel/', include(get_model_urls('appm', 'applicationpersonnel', detail=False))),
    path('application-personnel/<int:pk>/', include(get_model_urls('appm', 'applicationpersonnel'))),

]