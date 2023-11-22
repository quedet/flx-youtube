from django.urls import path
from apps.accounts import views
from django.contrib.auth.views import LogoutView

app_name = "accounts"

urlpatterns = [
    path("login/identifier/", views.LoginIdentifierView.as_view(), name="login-identifier"),
    path("login/pwd/", views.LoginCompleteView.as_view(), name="login-complete"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("signup/name/", views.SignupNameView.as_view(), name="signup-name"),
    path("signup/basic-info/", views.SignupBasicInformationView.as_view(), name="signup-info"),
    path("signup/email/", views.SignupEmailView.as_view(), name="signup-email"),
    path("signup/complete/", views.SignupView.as_view(), name="signup"),

    path("signup/skip-channel/", views.SignupSkipChannelCreationView.as_view(), name="skip-or-create-channel"),
]