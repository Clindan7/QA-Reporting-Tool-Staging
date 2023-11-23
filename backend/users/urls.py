from django.urls import path

from users.views import (google_login,create_access_token_from_refresh_token,get_all_users,get_user_by_id)

urlpatterns = [
    path('login/',google_login,name='google_login'),
    path('refreshtoken/',create_access_token_from_refresh_token,name='create_access_token_from_refresh_token'),
    path('userlist',get_all_users,name='user_list'),
    path('getuser',get_user_by_id,name='get_user_by_id')

]
