from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.views import (
    UserViewSet, MechanicProfileViewSet, ServiceViewSet, 
    BookingViewSet, PaymentViewSet, BookingCSVDownloadView
)
from core.views_html import register_view, login_view, home_view, logout_view, profile_view
from core.views_html import (register_view, login_view, home_view, logout_view, profile_view, services_view, book_service, my_bookings, add_service_view, become_mechanic_view)

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('mechanics', MechanicProfileViewSet)
router.register('services', ServiceViewSet)
router.register('bookings', BookingViewSet)
router.register('payments', PaymentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/bookings/csv/', BookingCSVDownloadView.as_view(), name='booking_csv'),
    path('register/', register_view, name='register_view'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('', home_view, name='home'),
    path('services/', services_view, name='services_view'),
    path('services/book/<int:service_id>/', book_service, name='book_service'),
    path('my_bookings/', my_bookings, name='my_bookings'),
    path('services/add/', add_service_view, name='add_service'),
    path('become_mechanic/', become_mechanic_view, name='become_mechanic'),
]
