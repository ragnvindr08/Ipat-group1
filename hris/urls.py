from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import *



urlpatterns = [
        path('register/', views.registerPage, name='register'),
        path('login/', views.loginPage, name='login'),
        path('logout/', views.logoutUser, name='logout'),
        path("", views.home, name="home"),
        path('account/', views.accountSettings, name="account"),
        path('user/', views.userPage, name='user-page'),
        path('upload/', views.upload_file, name='upload_file'),
        path('upload/success/', views.upload_success, name='upload_success'),  # Add this line
        path('search/', views.search_records, name='search_records'),
        path('dtr/', views.search_attendance, name='search_attendance'),
        path('search_attendance/', views.search_attendance_record, name='search_attendance_record'),
        path('edit/<int:record_id>/', views.edit_attendance_record, name='edit_attendance_record'),
        path('attendance_records/', views.view_attendance_records, name='attendance_records'),
        path('official_time/', views.official_time_view, name='official_time'),
        path('edit-logs/', views.edit_logs, name='edit_logs'),
        path('pds1/', views.pds1, name='pds1'),
]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  

        # # path("products/", views.products, name='products'),
        # path("profile/<str:pk_test>/", views.customer, name='customer'),
        # path('create_order/<str:pk>/', views.createOrder, name='create_order'),
        # path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
        # path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),
        # path('reset_password', auth_views.PasswordResetView.as_view(), name='reset_password'),
        # path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
        # path('reset/<uidb64>/<toke>/', auth_views.PasswordResetConfirmView.as_view(), name='passqord_reset_confirm'),
        # path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),




