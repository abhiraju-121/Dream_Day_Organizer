from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.base,name='base'),
    path('home',views.home,name='home'),
    path('user_register',views.register_user,name='user_register'),
    path('login_user',views.login_user,name='user_login'),
    path('logout_user',views.logout_user,name='user_logout'),
    path('user_dashboard',views.user_dashboard,name='user_dashboard'),
    path('user_profile',views.user_profile,name='user_profile'),


    path('view_event',views.user_event_list,name='user_event_list'),
    path('user_book_event/<int:event_id>/',views.user_book_event,name='user_book_event'),
    path('user_event_bookings/',views.user_event_bookings,name='user_event_bookings'),


    path('venues/', views.venue_list, name='venue_list'),
    path('venues/book/<int:venue_id>/', views.book_venue, name='book_venue'),
    path('user/bookings/', views.user_bookings, name='user_bookings'),
   

    path('transport/', views.user_transport_list, name='user_transport_list'),
    path('transport/book/<int:service_id>/', views.user_book_transport, name='user_book_transport'),
    path('transport/bookings/', views.user_trans_bookings, name='user_trans_bookings'),


    path('catering/', views.user_catering_list, name='user_catering_list'),
    path('catering/book/<int:cater_id>/', views.user_book_catering, name='user_book_catering'),
    path('catering/bookings/', views.user_catering_bookings, name='user_catering_bookings'),

    path('decoration_list/', views.user_decoration_list, name='user_decoration_list'),
    path('decore/book/<int:decore_id>/', views.user_book_decore, name='user_book_decore'),
    path('decore_bookings/', views.user_decore_bookings, name='user_decore_bookings'),


    path('photo_list/', views.user_photo_video_list, name='user_photo_video_list'),
    path('photo_video/book/<int:photo_id>/', views.user_book_photo_video, name='user_book_photo_video'),
    path('photo_video_bookings/', views.user_photo_video_bookings, name='user_photo_video_bookings'),
    

    path('bride_list/', views.user_bride_groom_list, name='user_bride_groom_list'),
    path('bride_groom/book/<int:decore_id>/', views.user_bride_groom, name='user_bride_groom'),
    path('bride_groom_bookings/', views.user_bride_groom_bookings, name='user_bride_groom_bookings'),
    





    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]
