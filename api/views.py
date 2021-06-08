from django.db.models.fields import CharField
from django.shortcuts import render
from api.models import PvpSeason, PvpSeasonReward, PvpBracket, Language, Region, Realm, Faction, Race, WowClass, Spec, Talent, PvpTalent, Covenant, PvpEntry2v2Historical, PvpEntry3v3Historical
from api.models import PvpEntry2v2, PvpEntry3v3, PvpEntryRbg, Soulbind, SoulbindTrait, Conduit, PvpBracketStatistics, CharacterConduit, Character, Achievement, CharacterAchievement, PvpEntryRbgHistorical
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

import django_filters
from django_filters import FilterSet
from rest_framework.pagination import PageNumberPagination
from rest_framework import views

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class PvpEntry2v2HistoricalFilter(FilterSet):

    character__spec__id = django_filters.filters.ModelMultipleChoiceFilter(
        field_name='character__spec__id',
        to_field_name='id',
        queryset=Spec.objects.all(),
    )

    class Meta:
        model = PvpEntry2v2Historical
        fields = ('rank', 'rating', 'season__sid', 'region__name',
    'character__faction__name', 'character__realm__slug', 'character__realm__category', 'character__spec__id')

class PvpEntry3v3HistoricalFilter(FilterSet):

    character__spec__id = django_filters.filters.ModelMultipleChoiceFilter(
        field_name='character__spec__id',
        to_field_name='id',
        queryset=Spec.objects.all(),
    )

    class Meta:
        model = PvpEntry3v3Historical
        fields = ('rank', 'rating', 'season__sid', 'region__name',
    'character__faction__name', 'character__realm__slug', 'character__realm__category', 'character__spec__id')

class PvpEntryRbgHistoricalFilter(FilterSet):

    character__spec__id = django_filters.filters.ModelMultipleChoiceFilter(
        field_name='character__spec__id',
        to_field_name='id',
        queryset=Spec.objects.all(),
    )

    class Meta:
        model = PvpEntryRbgHistorical
        fields = ('rank', 'rating', 'season__sid', 'region__name',
    'character__faction__name', 'character__realm__slug', 'character__realm__category', 'character__spec__id')


class PvpEntry2v2Filter(FilterSet):

    character__spec__id = django_filters.filters.ModelMultipleChoiceFilter(
        field_name='character__spec__id',
        to_field_name='id',
        queryset=Spec.objects.all(),
    )

    class Meta:
        model = PvpEntry2v2
        fields = ('rank', 'rating', 'season__sid', 'region__name',
    'character__faction__name', 'character__realm__slug', 'character__realm__category', 'character__spec__id')

class PvpEntry3v3Filter(FilterSet):

    character__spec__id = django_filters.filters.ModelMultipleChoiceFilter(
        field_name='character__spec__id',
        to_field_name='id',
        queryset=Spec.objects.all(),
    )

    class Meta:
        model = PvpEntry3v3
        fields = ('rank', 'rating', 'season__sid', 'region__name',
    'character__faction__name', 'character__realm__slug', 'character__realm__category', 'character__spec__id')

class PvpEntryRbgFilter(FilterSet):

    character__spec__id = django_filters.filters.ModelMultipleChoiceFilter(
        field_name='character__spec__id',
        to_field_name='id',
        queryset=Spec.objects.all(),
    )

    class Meta:
        model = PvpEntryRbg
        fields = ('rank', 'rating', 'season__sid', 'region__name',
    'character__faction__name', 'character__realm__slug', 'character__realm__category', 'character__spec__id')

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
    search_fields = ['name']

    @method_decorator(cache_page(60*60*24*90))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class RaceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.RaceSerializer
    permission_classes = [HasAPIKey]
    queryset = Race.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
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
    search_fields = ['name']
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
    search_fields = ['name']
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
    search_fields = ['name']
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
    search_fields = ['name']
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
    search_fields = ['name']
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
    search_fields = ['name']

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
    search_fields = ['name']
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
    search_fields = ['name']
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
    search_fields = ['name']
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
    permission_classes = [HasAPIKey]
    queryset = PvpEntry2v2.objects.select_related("character", "season", "region", "character__region", 
    "character__realm", "character__wow_class", "character__faction", "character__spec", "character__race")
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['character__name', 'time']
    filter_class = PvpEntry2v2Filter
    ordering_fields = ['rank', 'rating', 'season__sid']
    pagination_class = StandardResultsSetPagination

class PvpEntry3v3ViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PvpEntry3v3Serializer
    permission_classes = [HasAPIKey]
    queryset = PvpEntry3v3.objects.select_related("character", "season", "region", "character__region", 
    "character__realm", "character__wow_class", "character__faction", "character__spec", "character__race")
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['character__name', 'time']
    filter_class = PvpEntry3v3Filter
    ordering_fields = ['rank', 'rating', 'season__sid']
    pagination_class = StandardResultsSetPagination

class PvpEntryRbgViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PvpEntryRbgSerializer
    permission_classes = [HasAPIKey]
    queryset = PvpEntryRbg.objects.select_related("character", "season", "region", "character__region", 
    "character__realm", "character__wow_class", "character__faction", "character__spec", "character__race")
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['time', 'character__name']
    filter_class = PvpEntryRbgFilter
    ordering_fields = ['rank', 'rating', 'season__sid']
    pagination_class = StandardResultsSetPagination

class PvpEntry2v2HistoricalViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PvpEntry2v2HistoricalSerializer
    permission_classes = [HasAPIKey]
    queryset = PvpEntry2v2Historical.objects.select_related("character", "season", "region", "character__region", 
    "character__realm", "character__wow_class", "character__faction", "character__spec", "character__race")
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['character__name', 'time']
    filter_class = PvpEntry2v2HistoricalFilter
    ordering_fields = ['rank', 'rating', 'season__sid']
    pagination_class = StandardResultsSetPagination

class PvpEntry3v3HistoricalViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PvpEntry3v3HistoricalSerializer
    permission_classes = [HasAPIKey]
    queryset = PvpEntry3v3Historical.objects.select_related("character", "season", "region", "character__region", 
    "character__realm", "character__wow_class", "character__faction", "character__spec", "character__race")
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['character__name', 'time']
    filter_class = PvpEntry3v3HistoricalFilter
    ordering_fields = ['rank', 'rating', 'season__sid']
    pagination_class = StandardResultsSetPagination

class PvpEntryRbgHistoricalViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PvpEntryRbgHistoricalSerializer
    permission_classes = [HasAPIKey]
    queryset = PvpEntryRbgHistorical.objects.select_related("character", "season", "region", "character__region", 
    "character__realm", "character__wow_class", "character__faction", "character__spec", "character__race")
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['time', 'character__name']
    filter_class = PvpEntryRbgHistoricalFilter
    ordering_fields = ['rank', 'rating', 'season__sid']
    pagination_class = StandardResultsSetPagination

class PvpSeasonViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'sid'
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

class Charts2v2ViewSet(views.APIView):

    permission_classes = [HasAPIKey]

    @method_decorator(cache_page(60*60))
    def get(self, request):

        yourdata = [{ 
            'races': {},
            'clases': {},
            'specs': {},
            'realms': {},
            'total_entries': len(PvpEntry2v2.objects.all())
        }]

        races = Race.objects.all()
        for race in races:
            yourdata[0]['races'][race.name] = len(PvpEntry2v2.objects.filter(character__race=race))
            
        clases = WowClass.objects.all()
        for wow_class in clases:
            yourdata[0]['clases'][wow_class.name] = len(PvpEntry2v2.objects.filter(character__wow_class=wow_class))
            specs = Spec.objects.filter(wow_class=wow_class)
            for spec in specs:
                yourdata[0]['specs'][spec.name + '-' + wow_class.name] = len(PvpEntry2v2.objects.filter(character__spec=spec, character__wow_class=wow_class))

        realms = Realm.objects.all()
        for realm in realms:
            realm_pop_horde = len(PvpEntry2v2.objects.filter(character__realm=realm, character__faction__name='Horde'))
            realm_pop_alliance = len(PvpEntry2v2.objects.filter(character__realm=realm, character__faction__name='Alliance'))
            if realm_pop_horde + realm_pop_alliance > 10:
                yourdata[0]['realms'][realm.slug] = { 'Horde': realm_pop_horde, 'Alliance': realm_pop_alliance }

        return Response(yourdata)

class Charts3v3ViewSet(views.APIView):

    permission_classes = [HasAPIKey]

    @method_decorator(cache_page(60*60))
    def get(self, request):

        yourdata = [{ 
            'races': {},
            'clases': {},
            'specs': {},
            'realms': {},
            'total_entries': len(PvpEntry3v3.objects.all())
        }]

        races = Race.objects.all()
        for race in races:
            yourdata[0]['races'][race.name] = len(PvpEntry3v3.objects.filter(character__race=race))
            
        clases = WowClass.objects.all()
        for wow_class in clases:
            yourdata[0]['clases'][wow_class.name] = len(PvpEntry3v3.objects.filter(character__wow_class=wow_class))
            specs = Spec.objects.filter(wow_class=wow_class)
            for spec in specs:
                yourdata[0]['specs'][spec.name + '-' + wow_class.name] = len(PvpEntry3v3.objects.filter(character__spec=spec, character__wow_class=wow_class))

        realms = Realm.objects.all()
        for realm in realms:
            realm_pop_horde = len(PvpEntry3v3.objects.filter(character__realm=realm, character__faction__name='Horde'))
            realm_pop_alliance = len(PvpEntry3v3.objects.filter(character__realm=realm, character__faction__name='Alliance'))
            if realm_pop_horde + realm_pop_alliance > 10:
                yourdata[0]['realms'][realm.slug] = { 'Horde': realm_pop_horde, 'Alliance': realm_pop_alliance }

        return Response(yourdata)

class ChartsRbgViewSet(views.APIView):

    permission_classes = [HasAPIKey]

    @method_decorator(cache_page(60*60))
    def get(self, request):

        yourdata = [{ 
            'races': {},
            'clases': {},
            'specs': {},
            'realms': {},
            'total_entries': len(PvpEntryRbg.objects.all())
        }]

        races = Race.objects.all()
        for race in races:
            yourdata[0]['races'][race.name] = len(PvpEntryRbg.objects.filter(character__race=race))
            
        clases = WowClass.objects.all()
        for wow_class in clases:
            yourdata[0]['clases'][wow_class.name] = len(PvpEntryRbg.objects.filter(character__wow_class=wow_class))
            specs = Spec.objects.filter(wow_class=wow_class)
            for spec in specs:
                yourdata[0]['specs'][spec.name + '-' + wow_class.name] = len(PvpEntryRbg.objects.filter(character__spec=spec, character__wow_class=wow_class))

        realms = Realm.objects.all()
        for realm in realms:
            realm_pop_horde = len(PvpEntryRbg.objects.filter(character__realm=realm, character__faction__name='Horde'))
            realm_pop_alliance = len(PvpEntryRbg.objects.filter(character__realm=realm, character__faction__name='Alliance'))
            if realm_pop_horde + realm_pop_alliance > 10:
                yourdata[0]['realms'][realm.slug] = { 'Horde': realm_pop_horde, 'Alliance': realm_pop_alliance }

        return Response(yourdata)



