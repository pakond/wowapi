from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path
from . import views

router = routers.DefaultRouter()
router.register(r'language', views.LanguageViewSet, basename="language")
router.register(r'region', views.RegionViewSet, basename="region")
router.register(r'realm', views.RealmViewSet, basename="realm")
router.register(r'faction', views.FactionViewSet, basename="faction")
router.register(r'race', views.RaceViewSet, basename="race")
router.register(r'class', views.WowClassViewSet, basename="class")
router.register(r'spec', views.SpecViewSet, basename="spec")
router.register(r'talent', views.TalentViewSet, basename="talent")
router.register(r'pvp-talent', views.PvpTalentViewSet, basename="pvp-talent")
router.register(r'achievement', views.AchievementViewSet, basename="achievement")
router.register(r'character-achievement', views.CharacterAchievementViewSet, basename="character-achievement")
router.register(r'covenant', views.CovenantViewSet, basename="covenant")
router.register(r'soulbind', views.SoulbindViewSet, basename="soulbind")
router.register(r'soulbind-trait', views.SoulbindTraitViewSet, basename="soulbind-trait")
router.register(r'conduit', views.ConduitViewSet, basename="conduit")
router.register(r'pvp-season-reward', views.PvpSeasonRewardViewSet, basename="pvp-season-reward")
router.register(r'pvp-bracket', views.PvpBracketViewSet, basename="pvp-bracket")
router.register(r'character', views.CharacterViewSet, basename="character")
router.register(r'pvp-entry', views.PvpEntryViewSet, basename="pvp-entry")
router.register(r'pvp-season', views.PvpSeasonViewSet, basename="pvp-season")

urlpatterns = [
    path('character/<str:region>/<slug:realm>/<str:name>/', views.CharacterViewSet.as_view({'get': 'retrieve'}), name='character-detail'),
    url(r'^', include(router.urls)),
]