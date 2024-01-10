from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import register, confirm_email, user_login, login_prompt
from django.contrib.auth import views as auth_views
from .views import home, save_entry_view, add_entry


urlpatterns = [
    path('', views.index, name="mywdiary"),
    path('add-entry/', add_entry, name="add_entry"),
    path('register/', register, name='register'),
    path('login/', user_login, name='user_login'),
    path('login-prompt/', login_prompt, name='login_prompt'),
    path('home/', home, name='home'),
    path('save_entry/', save_entry_view, name='save_entry'),
    path('confirm/<str:token>/', confirm_email, name='confirm_email'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
