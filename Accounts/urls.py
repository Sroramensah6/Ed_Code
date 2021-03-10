from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'

urlpatterns = [
    path(r'activate/<slug:uidb64>/<slug:token>',
         views.activate, name='activate'),
    path(r'signup', views.signup_view, name='signup'),
    path(r'logout', views.logout_view, name='logout'),
    path(r'login', views.loginPage_view, name='login'),
    path(r'profile', views.update_profile_view, name='profile'),
    path(r'sent', views.activation_sent_view, name="activation_sent"),

    # Start Change password setup
    path(
        r'password/change', auth_views.PasswordChangeView.as_view(
            template_name="accounts/change_password/password_change.html"
        ),
        name="password_change"
    ),
    path(
        r'password/change/done', auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/change_password/password_change_complete.html"
        ), name="password_change_done"
    ),
    # End Change password setup

    # Submit reset_password email form
    path(
        r'password/reset',
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset/reset_password.html"
        ),
        name="reset_password"
    ),
    # Email sent success message
    path(
        r'password/reset/sent',
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset/reset_password_sent.html"
        ),
        name="password_reset_done"
    ),
    # Link to password Reset form in email
    path(
        r'password/reset/<uidb64>/<token>',
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset/password_reset_form.html"
        ),
        name="password_reset_confirm"
    ),
    # Password sucessfully changed message
    path(
        r'password/reset/complete',
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset/password_reset_complete.html"
        ),
        name="password_reset_complete"
    )
]
