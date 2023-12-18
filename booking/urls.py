from django.urls import path
from .views import *



# git@github.com:nastyakurzanova/Backend_BMSTU.git
# https://github.com/nastyakurzanova/Backend_BMSTU.git

# git@github.com:nastyakurzanova/Frontend_BMSTU.git
# https://github.com/nastyakurzanova/Frontend_BMSTU.git


urlpatterns = [
    # Набор методов для услуг search_audiences
    path('api/audiences/search/<int:audiences_id>/', get_audiences_by_id),  # GET
    path('api/audiences/search/', search_audiences),  # GET !!
    path('api/audiences/<int:audiences_id>/', get_audiences_by_id),  # GET
    path('api/audiences/<int:audiences_id>/update/', update_audiences),  # PUT
    path('api/audiences/<int:audiences_id>/delete/', delete_audiences),  # DELETE
    path('api/audiences/create/', create_audiences),  # POST ДЕЛАЕТ ТОЛЬКО ДЕФОЛТНЫЕ 
    path('api/audiences/<int:audiences_id>/add_to_booking/', add_audiences_to_booking),  # POST добавление услуги в заявку
    path('api/audiences/<int:audiences_id>/image/', get_audiences_image),  # GET
    path('api/audiences/<int:audiences_id>/update_image/', update_audiences_image),  # PUT

    # Набор методов для заявок

    path('api/booking/search/', get_booking),  # GET
    path('api/booking/<int:booking_id>/', get_booking_by_id),  # GET
    path('api/booking/<int:booking_id>/update/', update_booking),  # PUT
    path('api/booking/<int:booking_id>/update_status_user/', update_status_user),  # PUT
    path('api/booking/<int:booking_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/booking/<int:booking_id>/delete/', delete_booking),  # DELETE
    path('api/booking/<int:booking_id>/delete_audiences/<int:audiences_id>/', delete_audiences_from_booking), # DELETE
]
