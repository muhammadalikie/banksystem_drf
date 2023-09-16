from .views  import AccountViewSet, EntryViewSet, TransferViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('accounts', AccountViewSet)
router.register('transfers', TransferViewSet)
router.register('entrys', EntryViewSet)



urlpatterns = router.urls