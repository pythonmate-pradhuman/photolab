
from rest_framework import routers
from file_app.views import ImageViewset
from CustomFilters.views import CustomFiltersViewset


router = routers.DefaultRouter()
router.register('filter', ImageViewset),
router.register('custom-filters', CustomFiltersViewset)
# router.register('hashtag',ImageHashtagView)
