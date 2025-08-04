from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'appm-api'
router = NetBoxRouter()
router.register('application-groups', views.ApplicationGroupViewSet)
router.register('applications', views.ApplicationViewSet)
router.register('application-servers', views.ApplicationServerViewSet)
router.register('application-endpoints', views.ApplicationEndpointViewSet)
router.register('application-personnel', views.ApplicationPersonnelViewSet)
urlpatterns = router.urls