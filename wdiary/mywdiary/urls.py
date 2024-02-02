from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import registration_success, confirmation_sent
from .views import confirm_email, user_login, view_entry_view, delete_selected_entries_view, export_diary_entries
from django.contrib.auth import views as auth_views
from .views import home, save_entry_view, password_reset_request, reset_email_sent
# from .views import home, save_entry_view, add_entry,  login_prompt,
from django.contrib import admin
from django.contrib.auth.views import PasswordChangeView

urlpatterns = [
    path('', views.index, name="mywdiary"),
    path('admin/', admin.site.urls),
    path('login-prompt/', user_login, name='user_login'),
    path('home/', home, name='home'),
    path('save_entry/', save_entry_view, name='save_entry'),
    path('view/<int:entry_id>/', view_entry_view, name='view_entry'),
    path('delete_selected_entries/', delete_selected_entries_view, name='delete_selected_entries'),
    path('accounts/', include('allauth.urls')),
    path('save_entry/<int:entry_id>/', save_entry_view, name='save_entry_with_id'),
    path('export_diary_entries/', export_diary_entries, name='export_diary_entries'),

    path('password_reset/', password_reset_request, name='password_reset'),
    path('reset_email_sent/', reset_email_sent, name='reset_email_sent'),
    # path('send_reset_email/', send_reset_email, name='send_reset_email'),
    # path('password_reset/', password_reset, name='password_reset'),
    # path('password_reset/', include('django.contrib.auth.urls')),
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('registration-success/', registration_success, name='registration_success'),
    path('confirmation-sent/', confirmation_sent, name='confirmation_sent'),
    path('confirm/<str:uid>/<str:token>/', confirm_email, name='confirm_email'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
