from django.conf.urls import include
from django.urls import path
from levelupapi.views import register_user, login_user
from rest_framework import routers
from levelupapi.views import GameTypes, GameView, EventView, Profile

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'gametypes', GameTypes, 'gametype')
router.register(r'games', GameView, 'game')
router.register(r'events', EventView, 'event')
router.register(r'profile', Profile, 'profile')
urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]