from django.shortcuts import render
from api.models import PvpSeason, PvpSeasonReward, PvpBracket, Language, Region, Realm, Faction, Race, WowClass, Spec, Talent, PvpTalent, Covenant
from api.models import PvpEntry2v2, PvpEntry3v3, PvpEntryRbg, Soulbind, SoulbindTrait, Conduit, PvpBracketStatistics, CharacterConduit, Character, Achievement, CharacterAchievement
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework import viewsets, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.http import require_http_methods
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime
import html
from . import serializers
from django.shortcuts import get_object_or_404
from . import wowpvp
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

# Create your views here.
class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'name'
    serializer_class = serializers.LanguageSerializer
    permission_classes = [HasAPIKey]
    queryset = Language.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['code']

    @method_decorator(cache_page(60*60*24*90))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.RegionSerializer
    permission_classes = [HasAPIKey]
    queryset = Region.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    @method_decorator(cache_page(60*60*24*90))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class RealmViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.RealmSerializer
    permission_classes = [HasAPIKey]
    queryset = Realm.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['region', 'category', 'locale', 'slug', 'timezone', 'rtype']

    @method_decorator(cache_page(60*60*24*90))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.RealmDetailSerializer
        return serializers.RealmSerializer

class FactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.FactionSerializer
    permission_classes = [HasAPIKey]
    queryset = Faction.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'name_es']

    @method_decorator(cache_page(60*60*24*90))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class RaceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.RaceSerializer
    permission_classes = [HasAPIKey]
    queryset = Race.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'name_es']
    filterset_fields = ['faction', 'is_allied_race']

    @method_decorator(cache_page(60*60*24*90))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.RaceDetailSerializer
        return serializers.RaceSerializer

class WowClassViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.WowClassSerializer
    permission_classes = [HasAPIKey]
    queryset = WowClass.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'name_es']
    filterset_fields = ['power_type']

    @method_decorator(cache_page(60*60*24*90))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.WowClassDetailSerializer
        return serializers.WowClassSerializer

class SpecViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.SpecSerializer
    permission_classes = [HasAPIKey]
    queryset = Spec.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'name_es']
    filterset_fields = ['wow_class', 'role']

    @method_decorator(cache_page(60*60*24*90))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.SpecDetailSerializer
        return serializers.SpecSerializer

class TalentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.TalentSerializer
    permission_classes = [HasAPIKey]
    queryset = Talent.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'name_es']
    filterset_fields = ['spell_id', 'talent_id', 'wow_class', 'spec', 'tier_index', 'column_index', 'level']

    @method_decorator(cache_page(60*60*24*90))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.TalentDetailSerializer
        return serializers.TalentSerializer

class PvpTalentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PvpTalentSerializer
    permission_classes = [HasAPIKey]
    queryset = PvpTalent.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'name_es']
    filterset_fields = ['spell_id', 'talent_id', 'wow_class', 'spec', 'level']

    @method_decorator(cache_page(60*60*24*90))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.PvpTalentDetailSerializer
        return serializers.PvpTalentSerializer

class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.AchievementSerializer
    permission_classes = [HasAPIKey]
    queryset = Achievement.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'name_es']
    filterset_fields = ['is_account_wide']

    @method_decorator(cache_page(60*60*24*90))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.AchievementDetailSerializer
        return serializers.AchievementSerializer

class CharacterAchievementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.CharacterAchievementSerializer
    permission_classes = [HasAPIKey]
    queryset = CharacterAchievement.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['achievement']

    @method_decorator(cache_page(60*60*1))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.CharacterAchievementDetailSerializer
        return serializers.CharacterAchievementSerializer

class CovenantViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.CovenantSerializer
    permission_classes = [HasAPIKey]
    queryset = Covenant.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'name_es']

    @method_decorator(cache_page(60*60*24*90))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.CovenantDetailSerializer
        return serializers.CovenantSerializer

class SoulbindViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.SoulbindSerializer
    permission_classes = [HasAPIKey]
    queryset = Soulbind.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'name_es']
    filterset_fields = ['covenant']

    @method_decorator(cache_page(60*60*24*90))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.SoulbindDetailSerializer
        return serializers.SoulbindSerializer

class SoulbindTraitViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.SoulbindTraitSerializer
    permission_classes = [HasAPIKey]
    queryset = SoulbindTrait.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'name_es']
    filterset_fields = ['soulbind']

    @method_decorator(cache_page(60*60*24*90))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.SoulbindTraitDetailSerializer
        return serializers.SoulbindTraitSerializer

class ConduitViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ConduitSerializer
    permission_classes = [HasAPIKey]
    queryset = Conduit.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'name_es']
    filterset_fields = ['type', 'wow_class']

    @method_decorator(cache_page(60*60*24*90))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.ConduitDetailSerializer
        return serializers.ConduitSerializer

class PvpBracketViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PvpBracketSerializer
    permission_classes = [HasAPIKey]
    queryset = PvpBracket.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['pvp_type']

    @method_decorator(cache_page(60*60*24*90))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.PvpBracketDetailSerializer
        return serializers.PvpBracketSerializer

class PvpSeasonRewardViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PvpSeasonRewardSerializer
    permission_classes = [HasAPIKey]
    queryset = PvpSeasonReward.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['achievement', 'faction', 'bracket']

    @method_decorator(cache_page(60*60*2))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.PvpSeasonRewardDetailSerializer
        return serializers.PvpSeasonRewardSerializer

class CharacterViewSet(viewsets.ModelViewSet):
    lookup_field = 'name'
    serializer_class = serializers.CharacterSerializer
    permission_classes = [HasAPIKey]
    queryset = Character.objects.select_related('region', 'realm', 'wow_class', 'faction', 'spec', 'race')
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['region', 'realm', 'faction', 'race', 'wow_class', 'spec', 'achievements_completed', 'covenant', 'soulbind']

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def retrieve(self, request, region=None, realm=None, name=None):
        lookup = { 'name': region }
        laregion = get_object_or_404(Region, **lookup)
        lookup2 = { 'region': laregion, 'slug': realm }
        elrealm = get_object_or_404(Realm, **lookup2)
        lookup3 = { 'name': name, 'region': laregion, 'realm': elrealm }
        character = get_object_or_404(Character, **lookup3)
        count = character.checked
        count += 1
        character.checked = count
        character.last_search = timezone.now()
        character.save()
        serializer = serializers.CharacterDetailSerializer(character, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.POST.get('name') or not request.POST.get('region') or not request.POST.get('realm'):
            return Response(data={'detail': 'Missing parametre for add character'}, status=status.HTTP_400_BAD_REQUEST)
        
        name = html.unescape(request.POST.get('name'))
        name = str.lower(name)

        region_exists = Region.objects.filter(id=request.POST.get('region'))
        if not region_exists:
            return Response(data={'detail': 'Insert character region'}, status=status.HTTP_400_BAD_REQUEST)
        region = Region.objects.get(id=request.POST.get('region'))

        realm_exists = Realm.objects.filter(id=request.POST.get('realm'))
        if not realm_exists:
            return Response(data={'detail': 'Insert character realm'}, status=status.HTTP_400_BAD_REQUEST)
        realm = Realm.objects.get(id=request.POST.get('realm'))

        if not name or not region or not realm:
            return Response(data={'detail': 'Some of parametre are incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        character_exists = Character.objects.filter(name=name, region=region, realm=realm)
        if character_exists:
            character_exists = Character.objects.get(name=name, region=region, realm=realm)
            if datetime.timestamp(character_exists.last_update) > datetime.timestamp(datetime.now()) - 50:
                return Response(data={'detail': 'Character exists on database and last update date is to short'}, status=status.HTTP_400_BAD_REQUEST)
            res = wowpvp.update_character(character_exists)
            if res == False:
                return Response(data={'detail': 'Update Failed ' + name + '-' + region.name + '-' + realm.slug}, status=status.HTTP_400_BAD_REQUEST) 
            return Response(data={'detail': 'Updated character ' + name + '-' + region.name + '-' + realm.slug})
        res = wowpvp.get_character(name, region, realm)

        if res == False:
            return Response(data={'detail': 'Character ' + name + '-' + region.name + '-' + realm.slug + ' not exists'}, status=status.HTTP_404_NOT_FOUND)

        return Response(data={'detail': 'Added character ' + name + '-' + region.name + '-' + realm.slug})

class PvpEntry2v2ViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PvpEntry2v2Serializer
    permission_classes = []
    queryset = PvpEntry2v2.objects.select_related("character", "season", "region", "character__region", 
    "character__realm", "character__wow_class", "character__faction", "character__spec", "character__race")
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['character__name', 'time']
    filterset_fields = ['rank', 'rating', 'season__sid', 'region__name', 'character__wow_class__name',
    'character__faction__name', 'character__realm__slug']
    ordering_fields = ['rank', 'rating', 'season__sid']
    pagination_class = StandardResultsSetPagination

class PvpEntry3v3ViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PvpEntry3v3Serializer
    permission_classes = []
    queryset = PvpEntry3v3.objects.select_related("character", "season", "region", "character__region", 
    "character__realm", "character__wow_class", "character__faction", "character__spec", "character__race")
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['character__name', 'time']
    filterset_fields = ['rank', 'rating', 'season__sid', 'region__name', 'character__wow_class__name',
    'character__faction__name', 'character__realm__slug']
    ordering_fields = ['rank', 'rating', 'season__sid']
    pagination_class = StandardResultsSetPagination

class PvpEntryRbgViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PvpEntryRbgSerializer
    permission_classes = []
    queryset = PvpEntryRbg.objects.select_related("character", "season", "region", "character__region", 
    "character__realm", "character__wow_class", "character__faction", "character__spec", "character__race")
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['time', 'character__name']
    filterset_fields = ['rank', 'rating', 'season__sid', 'region__name', 'character__wow_class__name',
    'character__faction__name', 'character__realm__slug']
    ordering_fields = ['rank', 'rating', 'season__sid']
    pagination_class = StandardResultsSetPagination

class PvpSeasonViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PvpSeasonSerializer
    permission_classes = [HasAPIKey]
    queryset = PvpSeason.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sid','is_active', 'season_start_timestamp', 'season_end_timestamp']

    @method_decorator(cache_page(60*60*24*90))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.PvpSeasonDetailSerializer
        return serializers.PvpSeasonSerializer
