from unicodedata import name
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views #import this

app_name = 'Auth_system'

urlpatterns = [
    path('login/',views.loginpage,name='loginpage'),#extra
    path('register/',views.register,name='registerpage'),#extra
    path('register_user/',views.register_user,name='register_user_n'),
    path('login_user/',views.login_user,name='login_user_n'),
    path('logout_user/',views.logout_user,name='logout_user_n'),
    path('tmp/',views.tmp,name='tmp_n'),
    # path('accounts/', include('django.contrib.auth.urls')),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='Auth_system/password_reset_done.html'), name='password_reset_done'),#second
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="Auth_system/password_reset_confirm.html",success_url="/Auth_system/login_user/"), name='password_reset_confirm'),#third
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='Auth_system/password_reset_complete.html'), name='password_reset_complete'), #four

    path("password_reset", views.password_reset_request, name="password_reset")#first

]