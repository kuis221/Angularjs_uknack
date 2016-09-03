from django.conf.urls import url
from .views import UserConnectView, UserDisconnectView, UserNotificationEmailViewSet


urlpatterns = [
    url(r'^register/?$', 'user_auth.views.register'),
    url(r'^register_email$', 'user_auth.views.register_email'),
    url(r'^already_registered$', 'user_auth.views.already_registered'),
    url(r'^login$', 'user_auth.views.obtain_auth_token'),
    url(r'^fb_login$', 'user_auth.views.social_login'),
    url(r'^logout$', 'user_auth.views.logout'),
    url(r'^change-password', 'user_auth.views.change_password'),
    url(r'^forgot-password$', 'user_auth.views.forgot_password'),
    url(r'^isResetable$', 'user_auth.views.isResetable'),
    url(r'^reset-password$', 'user_auth.views.reset_password'),
    url(r'^profile$', 'user_auth.views.profile_view'),
    url(r'^profile/edit$', 'user_auth.views.profile_edit_view'),
    url(r'^profile/picture/edit$', 'user_auth.views.profile_picture_edit_view'),
    url(r'^profile/social/edit$', 'user_auth.views.profile_social_edit_view'),
    url(r'^profile/about/edit$', 'user_auth.views.profile_about_edit_view'),
    url(r'^profile/payment/edit$', 'user_auth.views.profile_payment_edit_view'),
    url(r'^profile/public_url/edit$', 'user_auth.views.profile_url_edit_view'),
    url(r'^profile/reasons/edit$', 'user_auth.views.profile_reasons_edit_view'),
    url(r'^profile/notification_email/edit$', UserNotificationEmailViewSet.as_view({'put': 'update'})),
    url(r'^profile/connect$', UserConnectView.as_view()),
    url(r'^profile/disconnect',  UserDisconnectView.as_view()),
    url(r'^colleges$', 'user_auth.views.college_list_view'),
    url(r'^years$', 'user_auth.views.year_list_view'),
    url(r'^genders', 'user_auth.views.gender_list_view')
]
