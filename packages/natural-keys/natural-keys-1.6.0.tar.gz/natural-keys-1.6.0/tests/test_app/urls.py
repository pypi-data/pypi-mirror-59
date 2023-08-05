from rest_framework import routers
from .views import (
    NaturalKeyChildViewSet, ModelWithNaturalKeyViewSet,
    ModelWithSingleUniqueFieldViewSet,
    NaturalKeyLookupViewSet,
)


router = routers.DefaultRouter()
router.register(r'naturalkeychilds', NaturalKeyChildViewSet)
router.register(r'modelwithnaturalkeys', ModelWithNaturalKeyViewSet)
router.register(r'modelwithsingleuniquefield',
                ModelWithSingleUniqueFieldViewSet)
router.register(r'naturalkeylookup', NaturalKeyLookupViewSet)

urlpatterns = router.urls
