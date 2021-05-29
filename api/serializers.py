from rest_framework import serializers
from api.models import Achievement, CharacterAchievement, CharacterConduit, PvpSeason, PvpSeasonReward, PvpBracket, PvpBracketStatistics, Language
from api.models import PvpEntry2v2, PvpEntry3v3, PvpEntryRbg, Region, Realm, Faction, Race, WowClass, Spec, Talent, PvpTalent, Covenant, Soulbind, SoulbindTrait, Conduit, Character
from django.conf import settings

class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ['id', 'name', 'code', 'icon']

class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ['id', 'name', 'icon']

class RealmDetailSerializer(serializers.ModelSerializer):

    region = RegionSerializer(read_only=True)

    class Meta:
        model = Realm
        fields = ['id', 'name', 'slug', 'region', 'category', 'locale', 'timezone', 'rtype', 'icon']

class RealmSerializer(serializers.ModelSerializer):

    region = serializers.ReadOnlyField(source='region.name')

    class Meta:
        model = Realm
        fields = ['id', 'slug', 'region', 'icon', 'category']

class FactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Faction
        fields = ['id', 'name', 'name_es', 'icon']

class WowClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = WowClass
        fields = ['id', 'name', 'color', 'icon']

class WowClassDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = WowClass
        fields = ['id', 'name', 'name_es', 'color', 'power_type', 'icon']

class RaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Race
        fields = ['id', 'name', 'faction']

class RaceDetailSerializer(serializers.ModelSerializer):

    faction = FactionSerializer(read_only=True)
    wow_clases = WowClassSerializer(read_only=True, many=True)

    class Meta:
        model = Race
        fields = ['id', 'name', 'name_es', 'faction', 'wow_clases', 'is_allied_race', 'icon_male', 'icon_female']


class SpecDetailSerializer(serializers.ModelSerializer):

    wow_class = WowClassSerializer(read_only=True)

    class Meta:
        model = Spec
        fields = ['id', 'name', 'name_es', 'description', 'description_es', 'icon', 'wow_class', 'role', 'talents', 'pvp_talents']

class SpecSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spec
        fields = ['id', 'name', 'icon', 'wow_class']

class TalentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Talent
        fields = ['id', 'name', 'spell_id', 'talent_id']

class TalentDetailSerializer(serializers.ModelSerializer):

    wow_class = WowClassSerializer(read_only=True)
    spec = SpecSerializer(many=True, read_only=True)

    class Meta:
        model = Talent
        fields = ['id', 'name', 'name_es', 'description', 'description_es', 'spell_id', 'talent_id', 'wow_class', 'spec', 'tier_index', 'column_index', 'level', 'icon']


class PvpTalentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PvpTalent
        fields = ['id', 'name', 'spell_id', 'talent_id']


class PvpTalentDetailSerializer(serializers.ModelSerializer):

    wow_class = WowClassSerializer(read_only=True)
    spec = SpecSerializer(read_only=True)

    class Meta:
        model = PvpTalent
        fields = ['id', 'name', 'name_es', 'description', 'description_es', 'spell_id', 'talent_id', 'wow_class', 'spec', 'level', 'icon']

class AchievementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Achievement
        fields = ['id', 'name', 'aid' ]


class AchievementDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Achievement
        fields = ['id', 'name', 'aid', 'name_es', 'description', 'description_es', 'is_account_wide', 'points', 'icon']

class CharacterAchievementSerializer(serializers.ModelSerializer):

    aid = serializers.ReadOnlyField(source='achievement.aid')
    name = serializers.ReadOnlyField(source='achievement.name')
    description = serializers.ReadOnlyField(source='achievement.description')

    class Meta:
        model = CharacterAchievement
        fields = ['name', 'description', 'achievement', 'aid', 'date_completed']

class CharacterAchievementDetailSerializer(serializers.ModelSerializer):

    achievement = AchievementSerializer(read_only=True)

    class Meta:
        model = CharacterAchievement
        fields = ['id', 'achievement', 'date_completed']

class CovenantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Covenant
        fields = ['id', 'name', 'cid']

class CovenantDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Covenant
        fields = ['id', 'name', 'name_es', 'description', 'description_es', 'icon']

class SoulbindSerializer(serializers.ModelSerializer):

    class Meta:
        model = Soulbind
        fields = ['id', 'name']

class SoulbindDetailSerializer(serializers.ModelSerializer):

    covenant = CovenantSerializer(read_only=True)

    class Meta:
        model = Soulbind
        fields = ['id', 'name', 'name_es', 'covenant']

class SoulbindTraitDetailSerializer(serializers.ModelSerializer):

    soulbind = SoulbindSerializer(read_only=True)

    class Meta:
        model = SoulbindTrait
        fields = ['id', 'name', 'sid', 'name_es', 'soulbind', 'description', 'description_es', 'spell_id', 'icon']

class SoulbindTraitSerializer(serializers.ModelSerializer):

    class Meta:
        model = SoulbindTrait
        fields = ['id', 'name', 'spell_id', 'sid']

class ConduitDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conduit
        fields = ['id', 'name', 'cid', 'name_es', 'ranks', 'type', 'icon']

class ConduitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conduit
        fields = ['id', 'name', 'cid' ]

class CharacterConduitSerializer(serializers.ModelSerializer):

    cid = serializers.ReadOnlyField(source='conduit.cid')

    class Meta:
        model = CharacterConduit
        fields = ['id', 'cid', 'rank', 'spell_id']

class PvpBracketSerializer(serializers.ModelSerializer):

    class Meta:
        model = PvpBracket
        fields = ['id', 'pvp_type']

class PvpBracketDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = PvpBracket
        fields = ['id', 'pvp_type', 'description', 'description_es']

class PvpSeasonRewardSerializer(serializers.ModelSerializer):

    class Meta:
        model = PvpSeasonReward
        fields = ['id', 'achievement']

class PvpSeasonRewardDetailSerializer(serializers.ModelSerializer):

    achievement = AchievementSerializer(read_only=True)
    faction = FactionSerializer(read_only=True)
    bracket = PvpBracketSerializer(read_only=True)

    class Meta:
        model = PvpSeasonReward
        fields = ['id', 'achievement', 'faction', 'bracket', 'cutoff']

class PvpBracketStatisticsSerializer(serializers.ModelSerializer):

    bracket = PvpBracketSerializer(read_only=True)

    class Meta:
        model = PvpBracketStatistics
        fields = ['bracket', 'rating', 'won', 'lost', 'played', 'winratio']

class PvpSeasonSerializer(serializers.ModelSerializer):

    class Meta:
        model = PvpSeason
        fields = ['id', 'sid', 'season_start_timestamp']

class PvpSeasonDetailSerializer(serializers.ModelSerializer):

    rewards = PvpSeasonRewardSerializer(read_only=True)
    
    class Meta:
        model = PvpSeason
        fields = ['id', 'sid', 'season_start_timestamp', 'season_end_timestamp', 'is_active', 'rewards']
        

class CharacterSerializer(serializers.ModelSerializer):

    region = serializers.ReadOnlyField(source='region.name')
    realm = serializers.ReadOnlyField(source='realm.slug')
    wow_class = serializers.ReadOnlyField(source='wow_class.name')
    faction = serializers.ReadOnlyField(source='faction.name')
    spec = serializers.ReadOnlyField(source='spec.name')
    race = serializers.ReadOnlyField(source='race.name')

    class Meta:
        model = Character
        fields = ['name', 'realm', 'region', 'faction', 'wow_class', 'guild', 'spec', 'race', 'gender', 'max_3v3_rating', 'max_2v2_rating']


class CharacterDetailSerializer(serializers.ModelSerializer):

    region = RegionSerializer(read_only=True)
    realm = RealmSerializer(read_only=True)
    faction = FactionSerializer(read_only=True)
    race = RaceSerializer(read_only=True)
    wow_class = WowClassSerializer(read_only=True)
    spec = SpecSerializer(read_only=True)
    talents = TalentSerializer(many=True, read_only=True)
    pvp_talents = PvpTalentSerializer(many=True, read_only=True)
    covenant = CovenantSerializer(read_only=True)
    soulbind = SoulbindSerializer(read_only=True)
    soulbind_abilities = SoulbindTraitSerializer(many=True, read_only=True)
    conduits = CharacterConduitSerializer(many=True, read_only=True)
    achievements = CharacterAchievementSerializer(many=True, read_only=True)
    ratings = PvpBracketStatisticsSerializer(many=True, read_only=True)
    alters = CharacterSerializer(many=True, read_only=True)

    class Meta:
        model = Character
        fields = ['id', 'name', 'region', 'realm', 'faction', 'race', 'wow_class', 'spec', 'talents', 'pvp_talents', 'active_title', 'guild',
        'covenant', 'covenant_rank', 'soulbind', 'soulbind_abilities', 'conduits', 'item_level', 'media', 'avatar', 'achievement_points', 'gender', 
        'achievements', 'ratings', 'max_2v2_rating', 'max_3v3_rating', 'max_rbg_rating', 'alters', 'last_update', 'last_search', 'checked', 'level']


class PvpEntry2v2Serializer(serializers.ModelSerializer):

    character = CharacterSerializer(read_only=True)
    season = PvpSeasonSerializer(read_only=True)
    region = RegionSerializer(read_only=True)

    class Meta:
        model = PvpEntry2v2
        fields = ['rank', 'rating', 'season', 'region', 'character', 'won', 'lost', 'played', 'winratio', 'time']

class PvpEntry3v3Serializer(serializers.ModelSerializer):

    character = CharacterSerializer(read_only=True)
    season = PvpSeasonSerializer(read_only=True)
    region = RegionSerializer(read_only=True)

    class Meta:
        model = PvpEntry3v3
        fields = ['rank', 'rating', 'season', 'region', 'character', 'won', 'lost', 'played', 'winratio', 'time']

class PvpEntryRbgSerializer(serializers.ModelSerializer):

    character = CharacterSerializer(read_only=True)
    season = PvpSeasonSerializer(read_only=True)
    region = RegionSerializer(read_only=True)

    class Meta:
        model = PvpEntryRbg
        fields = ['rank', 'rating', 'season', 'region', 'character', 'won', 'lost', 'played', 'winratio', 'time']
