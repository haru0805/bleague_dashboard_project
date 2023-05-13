from django.urls import path
from .views import team_list, team_detail, player_detail

urlpatterns = [
    path('<int:team_id>/', team_detail, name='team_detail'),
    path('<int:team_id>/<int:player_id>/', player_detail, name='player_detail'),
    path('', team_list, name='team_list'),
]