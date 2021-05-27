from django.contrib import admin
from .models import PvpSeason, PvpSeasonReward, PvpBracket, Language, Faction, Region, Realm, Race, WowClass, Spec, Talent, PvpTalent, Covenant, Soulbind, SoulbindTrait, Conduit, CharacterConduit, PvpBracketStatistics, Character, Achievement, CharacterAchievement
# Register your models here.

class CustomLanguage(admin.ModelAdmin):
    model = Language
    list_display = ('name', 'code', 'icon',)
    list_filter = ('name', 'code',)

class CustomFaction(admin.ModelAdmin):
    model = Faction
    list_display = ('name', 'icon',)
    list_filter = ('name',)

class CustomRegion(admin.ModelAdmin):
    model = Region
    list_display = ('name', 'icon',)
    list_filter = ('name',)

class CustomRealm(admin.ModelAdmin):
    model = Realm
    list_display = ('name', 'slug', 'rid', 'region', 'category', 'locale', 'timezone', 'rtype',)
    list_filter = ('name', 'slug', 'rid', 'region', 'category', 'locale', 'timezone', 'rtype',)

class CustomRace(admin.ModelAdmin):
    model = Race
    list_display = ('name', 'rid', 'faction', 'is_allied_race',)
    list_filter = ('name', 'rid', 'faction', 'is_allied_race',)

class CustomWowClass(admin.ModelAdmin):
    model = WowClass
    list_display = ('name', 'cid', 'power_type', 'icon',)
    list_filter = ('name', 'cid', 'power_type',)

class CustomSpec(admin.ModelAdmin):
    model = Spec
    list_display = ('name', 'sid', 'wow_class', 'icon', 'role',)
    list_filter = ('name', 'sid', 'wow_class', 'role',)

class CustomTalent(admin.ModelAdmin):
    model = Talent
    list_display = ('name', 'spell_id', 'talent_id', 'wow_class', 'level',)
    list_filter = ('name', 'spell_id', 'talent_id', 'wow_class', 'level',)

class CustomPvpTalent(admin.ModelAdmin):
    model = PvpTalent
    list_display = ('name', 'spell_id', 'talent_id', 'wow_class',)
    list_filter = ('name', 'spell_id', 'talent_id', 'wow_class',)

class CustomAchievement(admin.ModelAdmin):
    model = Achievement
    list_display = ('name', 'aid', 'is_account_wide', 'points',)
    list_filter = ('name', 'aid', 'is_account_wide', 'points',)

class CustomCharacterAchievement(admin.ModelAdmin):
    model = CharacterAchievement
    list_display = ('date_completed',)
    list_filter = ('date_completed',)

class CustomCovenant(admin.ModelAdmin):
    model = Covenant
    list_display = ('name', 'cid',)
    list_filter = ('name', 'cid',)

class CustomSoulbind(admin.ModelAdmin):
    model = Soulbind
    list_display = ('name', 'sid', 'covenant',)
    list_filter = ('name', 'sid', 'covenant',)

class CustomSoulbindTrait(admin.ModelAdmin):
    model = SoulbindTrait
    list_display = ('name', 'sid', 'soulbind', 'spell_id',)
    list_filter = ('name', 'sid', 'soulbind', 'soulbind',)

class CustomConduit(admin.ModelAdmin):
    model = Conduit
    list_display = ('name', 'cid', 'type',)
    list_filter = ('name', 'cid', 'type',)

class CustomCharacterConduit(admin.ModelAdmin):
    model = CharacterConduit
    list_display = ('rank',)
    list_filter = ('rank',)

class CustomPvpBracketStatistics(admin.ModelAdmin):
    model = PvpBracketStatistics
    list_display = ('bracket', 'rating', 'won', 'lost', 'played', 'winratio',)
    list_filter = ('bracket', 'rating', 'won', 'lost', 'played', 'winratio',)

class CustomPvpBracket(admin.ModelAdmin):
    model = PvpBracket
    list_display = ('pvp_type',)
    list_filter = ('pvp_type',)

class CustomCharacter(admin.ModelAdmin):
    model = Character
    list_display = ('name', 'region', 'realm', 'faction', 'race', 'spec', 'covenant', 'covenant_rank', 
    'soulbind', 'item_level', 'achievement_points', 'last_update', 'last_search', 'checked',)
    list_filter = ('name', 'region', 'realm', 'faction', 'race', 'spec', 'covenant', 'covenant_rank', 
    'soulbind', 'item_level', 'achievement_points', 'last_update', 'last_search', 'checked',)


class CustomPvpSeasonReward(admin.ModelAdmin):
    model = PvpSeasonReward
    list_display = ('achievement', 'bracket', 'faction', 'region', 'cutoff',)
    list_filter = ('achievement', 'bracket', 'faction', 'region', 'cutoff',)

class CustomPvpSeason(admin.ModelAdmin):
    model = PvpSeason
    list_display = ('sid', 'season_start_timestamp', 'is_active', 'season_end_timestamp',)
    list_filter = ('sid', 'season_start_timestamp', 'is_active', 'season_end_timestamp',)

admin.site.register(Language, CustomLanguage)
admin.site.register(Faction, CustomFaction)
admin.site.register(Region, CustomRegion)
admin.site.register(Realm, CustomRealm)
admin.site.register(Race, CustomRace)
admin.site.register(WowClass, CustomWowClass)
admin.site.register(Spec, CustomSpec)
admin.site.register(Talent, CustomTalent)
admin.site.register(PvpTalent, CustomPvpTalent)
admin.site.register(Achievement, CustomAchievement)
admin.site.register(CharacterAchievement, CustomCharacterAchievement)
admin.site.register(Covenant, CustomCovenant)
admin.site.register(Soulbind, CustomSoulbind)
admin.site.register(SoulbindTrait, CustomSoulbindTrait)
admin.site.register(Conduit, CustomConduit)
admin.site.register(CharacterConduit, CustomCharacterConduit)
admin.site.register(PvpBracketStatistics, CustomPvpBracketStatistics)
admin.site.register(Character, CustomCharacter)
admin.site.register(PvpBracket, CustomPvpBracket)
admin.site.register(PvpSeasonReward, CustomPvpSeasonReward)
admin.site.register(PvpSeason, CustomPvpSeason)