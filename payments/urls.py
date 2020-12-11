from django.contrib.auth import views as auth_views
from django.urls import path
from payments import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    # Reset Password URLs
    path(
        'reset_password/',
        auth_views.PasswordResetView.as_view(template_name="accounts/password_reset/password_reset.html"),
        name="reset_password"
    ),

    path(
        'reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset/password_reset_sent.html"
        ),
        name="password_reset_done"
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset/password_reset_confirm.html"
        ),
        name="password_reset_confirm"
    ),

    path(
        'reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset/password_reset_done.html"
        ),
        name="password_reset_complete"
    ),

]
