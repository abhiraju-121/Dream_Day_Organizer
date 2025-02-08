from django.urls import path
from . import views

urlpatterns=[
    path('servicer_register',views.servicer_register,name='servicer_register'),
    path('servicer_login',views.servicer_login,name='servicer_login'),
    path('servicer_logout',views.servicer_logout,name='servicer_logout'),
    path('servicer_dashboard',views.service_provider_dashboard,name='servicer_dashboard'),
    path('servicer_home',views.servicer_home,name='servicer_home'),

    path('service_provider_event_list', views.service_provider_event_list, name='service_provider_event_list'),
    path('add_event', views.add_event, name='add_event'),
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('manage_event_bookings',views.manage_event_bookings,name='manage_event_bookings'),




    path('provider_venue_list', views.provider_venue_list, name='provider_venue_list'),
    path('add_venue', views.add_venue, name='add_venue'),
    path('add_venue/edit/<int:venue_id>/', views.edit_venue, name='edit_venue'),
    path('add_venue/remove/<int:venue_id>/', views.delete_venue, name='delete_venue'),
    path('provider_bookings', views.provider_bookings, name='provider_bookings'),
    path('provider_bookings/approve/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('provider_bookings/reject/<int:booking_id>/', views.reject_booking, name='reject_booking'),


    path('service-provider/transports/', views.service_provider_transports, name='service_provider_transports'),
    path('service-provider/transport/add/', views.add_transport, name='add_transport'),
    path('edit_transport/<int:service_id>/',views.edit_transport,name='edit_transport'),
    path('service-provider/bookings/', views.provider_manage_trans_bookings, name='provider_manage_trans_bookings'),
    path('service-provider/booking/update/<int:booking_id>/<str:status>/', views.update_booking_status, name='update_booking_status'),


    path('provider_catering_services_list', views.provider_catering_services_list, name='provider_catering_services_list'),
    path('add_catering_service/', views.add_catering_service, name='add_catering_service'),
    path('edit_catering_service/<int:service_id>/', views.edit_catering_service, name='edit_catering_service'),
    path('delete_catering_service/<int:service_id>/', views.delete_catering_service, name='delete_catering_service'),
    path('provider_catering_bookings', views.provider_catering_bookings, name='provider_catering_bookings'),
    path('provider/catering/bookings/manage/<int:booking_id>/', views.manage_catering_booking_status, name='manage_catering_booking_status'),


    path('provider_decore_list', views.provider_decore_list, name='provider_decore_list'),
    path('add_decore_service/', views.add_decore_service, name='add_decore_service'),
    path('edit_deocre_service/<int:service_id>/', views.edit_deocre_service, name='edit_deocre_service'),
    path('delete_decore_service/<int:service_id>/', views.delete_decore_service, name='delete_decore_service'),
    path('provider_decore_bookings', views.provider_decore_bookings, name='provider_decore_bookings'),
    path('manage_deocre_booking_status/<int:booking_id>/', views.manage_decore_booking_status, name='manage_decore_booking_status'),

    path('provider_photo_video_list', views.provider_photo_video_list, name='provider_photo_video_list'),
    path('add_photo_video_service/', views.add_photo_video_service, name='add_photo_video_service'),
    path('edit_photo_video_service/<int:service_id>/', views.edit_photo_video_service, name='edit_photo_video_service'),
    path('delete_photo_video_service/<int:service_id>/', views.delete_photo_video_service, name='delete_photo_video_service'),
    path('provider_photo_video_bookings', views.provider_photo_video_bookings, name='provider_photo_video_bookings'),
    path('manage_photo_booking_status/<int:booking_id>/', views.manage_photo_booking_status, name='manage_photo_booking_status'),



    path('provider_bride_groom_list', views.provider_bride_groom_list, name='provider_bride_groom_list'),
    path('add_bride_groom_service/', views.add_bride_groom_service, name='add_bride_groom_service'),
    path('edit_bride_groom_service/<int:service_id>/', views.edit_bride_groom_service, name='edit_bride_groom_service'),
    path('delete_bride_groom_service/<int:service_id>/', views.delete_bride_groom_service, name='delete_bride_groom_service'),
    path('provider_bride_groom_bookings', views.provider_bride_groom_bookings, name='provider_bride_groom_bookings'),
    path('manage_bride_groom_status/<int:booking_id>/', views.manage_bride_groom_status, name='manage_bride_groom_status'),

    

]