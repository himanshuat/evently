from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("explore", views.explore, name="explore"),
    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup, name="signup"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("update-profile", views.update_profile, name="update_profile"),
    path("settings", views.settings, name="settings"),
    path("settings/change-username", views.change_username, name="change_username"),
    path("settings/change-password", views.change_password, name="change_password"),
    path("settings/delete-account", views.delete_account, name="delete_account"),

    path("event/<int:event_id>", views.event_details, name="event_details"),
    path("create-event", views.create_event, name="create_event"),
    path("event/<int:event_id>/edit", views.edit_event, name="edit_event"),
    path("event/<int:event_id>/delete", views.delete_event, name="delete_event"),
    path("event/<int:event_id>/register", views.register_event, name="register_event"),
    path("event/<int:event_id>/request-access", views.submit_event_request, name="submit_event_request"),
    path("event/<int:event_id>/rate", views.rate_event, name="rate_event"),
    path("event/<int:event_id>/confirmattendance", views.confirm_attendance, name="confirm_attendance"),
    path("accepteventrequest/<int:er_id>", views.accept_event_request, name="accept_event_request"),
    path("declineeventrequest/<int:er_id>", views.decline_event_request, name="decline_event_request"),
]
