from django.db import models
from jsonfield import JSONField
from django.utils import timezone

# Create your models here.

class Language(models.Model):
    name = models.CharField(max_length=264, null=False, unique=True)
    code = models.CharField(max_length=128, null=False)
    icon = models.ImageField(upload_to = 'static/img/language', null=False)

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=128, null=False, unique=True)
    icon = models.ImageField(upload_to = 'static/img/region', null=False)

    def __str__(self):
        return self.name

class Realm(models.Model):
    name = models.CharField(max_length=264, null=False)
    slug = models.CharField(max_length=264, null=False)
    rid = models.IntegerField(null=False, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=False)
    category = models.CharField(max_length=264, null=False)
    locale = models.CharField(max_length=128, null=False)
    timezone = models.CharField(max_length=264, null=False)
    rtype = models.CharField(max_length=264, null=False)
    icon = models.ImageField(upload_to = 'static/img/realm', null=True)

    def __str__(self):
        return self.name

class Faction(models.Model):
    name = models.CharField(max_length=264, null=False, unique=True)
    icon = models.ImageField(upload_to = 'static/img/faction', null=False)

    def __str__(self):
        return self.name

class WowClass(models.Model):
    name = models.CharField(max_length=264, null=False, unique=True)
    cid = models.IntegerField(null=False, unique=True)
    icon = models.ImageField(upload_to = 'static/img/class', null=False)
    power_type = models.CharField(max_length=264, null=False)
    color = models.CharField(max_length=20, null=True)
    
    def __str__(self):
        return self.name

class Race(models.Model):
    name = models.CharField(max_length=264, null=False)
    rid = models.IntegerField(null=False, unique=True)
    faction = models.ForeignKey(Faction, on_delete=models.CASCADE, null=False)
    is_allied_race = models.BooleanField(null=False)
    wow_clases = models.ManyToManyField(WowClass)
    icon_male = models.ImageField(upload_to = 'static/img/race', null=False)
    icon_female = models.ImageField(upload_to = 'static/img/race', null=False)

    def __str__(self):
        return self.name

class Spec(models.Model):
    name = models.CharField(max_length=264, null=False)
    description = models.CharField(max_length=5000, null=False)
    sid = models.IntegerField(null=False, unique=True)
    wow_class = models.ForeignKey(WowClass, on_delete=models.CASCADE, null=False)
    icon = models.ImageField(upload_to = 'static/img/spec', null=False)
    role = models.CharField(max_length=264, null=False)
    talents = JSONField(null=False)
    pvp_talents = JSONField(null=False)

    def __str__(self):
        return self.name

class Talent(models.Model):
    name = models.CharField(max_length=264, null=False)
    description = models.CharField(max_length=5000, null=False)
    spell_id = models.IntegerField(null=False)
    talent_id = models.IntegerField(null=False, unique=True)
    wow_class = models.ForeignKey(WowClass, on_delete=models.CASCADE, null=False)
    spec = models.ManyToManyField(Spec)
    icon = models.ImageField(upload_to = 'static/img/talent', null=False)
    tier_index = models.IntegerField(null=False)
    column_index = models.IntegerField(null=False)
    level = models.IntegerField(null=False)

    def __str__(self):
        return self.name

class PvpTalent(models.Model):
    name = models.CharField(max_length=264, null=False)
    description = models.CharField(max_length=5000, null=False)
    spell_id = models.IntegerField(null=False)
    talent_id = models.IntegerField(null=False, unique=True)
    wow_class = models.ForeignKey(WowClass, on_delete=models.CASCADE, null=False)
    spec = models.ForeignKey(Spec, on_delete=models.CASCADE, null=False)
    icon = models.ImageField(upload_to = 'static/img/pvp_talent', null=False)
    level = models.IntegerField(null=False)

    def __str__(self):
        return self.name

class Achievement(models.Model):
    name = models.CharField(max_length=264, null=False)
    aid = models.IntegerField(null=False, unique=True)
    description = models.CharField(max_length=5000, null=False)
    is_account_wide = models.BooleanField(null=False)
    points = models.IntegerField()
    icon = models.ImageField(upload_to = 'static/img/achievement', null=False)

    def __str__(self):
        return self.name

class CharacterAchievement(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, null=False)
    date_completed = models.DateTimeField(null=False)

    def __str__(self):
        return self.achievement.name

class Covenant(models.Model):
    name = models.CharField(max_length=264, null=False, unique=True)
    description = models.CharField(max_length=5000, null=False)
    cid = models.IntegerField(null=False, unique=True)
    icon = models.ImageField(upload_to = 'static/img/covenant', null=False)

    def __str__(self):
        return self.name

class Soulbind(models.Model):
    name = models.CharField(max_length=264, null=False)
    sid = models.IntegerField(null=False, unique=True)
    covenant = models.ForeignKey(Covenant, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name

class SoulbindTrait(models.Model):
    name = models.CharField(max_length=264, null=False)
    sid = models.IntegerField(null=False, unique=True)
    spell_id = models.IntegerField(null=False)
    soulbind = models.ForeignKey(Soulbind, on_delete=models.CASCADE, null=False)
    description = models.CharField(max_length=5000, null=False)
    icon = models.ImageField(upload_to = 'static/img/soulbind_trait', null=False)

    def __str__(self):
        return self.name

class Conduit(models.Model):
    name = models.CharField(max_length=264, null=False)
    cid = models.IntegerField(null=False, unique=True)
    ranks = JSONField(null=False)
    type = models.CharField(max_length=264, null=False)
    icon = models.ImageField(upload_to = 'static/img/conduit', null=False)

    def __str__(self):
        return self.name

class CharacterConduit(models.Model):
    conduit = models.ForeignKey(Conduit, on_delete=models.CASCADE, null=False)
    rank = models.IntegerField(null=False)
    spell_id = models.IntegerField(null=True)

    def __str__(self):
        return self.conduit.name

class PvpBracket(models.Model):
    pvp_type = models.CharField(max_length=264, null=False, unique=True)
    bid = models.IntegerField(null=False, unique=True)
    description = models.CharField(max_length=5000, null=False)

    def __str__(self):
        return self.pvp_type

class PvpSeasonReward(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, null=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
    bracket = models.ForeignKey(PvpBracket, on_delete=models.CASCADE, null=False)
    faction = models.ForeignKey(Faction, on_delete=models.CASCADE, null=False)
    cutoff = models.IntegerField(null=True, blank=True, default=None)

    def __str__(self):
        return self.achievement.name

class PvpSeason(models.Model):
    sid = models.IntegerField(null=False, unique=True)
    season_start_timestamp = models.DateTimeField(null=False)
    season_end_timestamp = models.DateTimeField(null=True, default=None, blank=True)
    rewards = models.ManyToManyField(PvpSeasonReward, blank=True, default=None)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.sid)

class PvpBracketStatistics(models.Model):
    bracket = models.ForeignKey(PvpBracket, on_delete=models.CASCADE, null=False)
    rating = models.IntegerField(null=False)
    won = models.IntegerField(null=False)
    lost = models.IntegerField(null=False)
    played = models.IntegerField(null=False)
    winratio = models.IntegerField(null=False)

    def __str__(self):
        return str(self.rating)

class Character(models.Model):
    name = models.CharField(max_length=264, null=False)
    gender = models.CharField(max_length=264, null=False)
    cid = models.IntegerField(null=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=False)
    realm = models.ForeignKey(Realm, on_delete=models.CASCADE, null=False)
    faction = models.ForeignKey(Faction, on_delete=models.CASCADE, null=False)
    race = models.ForeignKey(Race, on_delete=models.CASCADE, null=False)
    wow_class = models.ForeignKey(WowClass, on_delete=models.CASCADE, null=False)
    spec = models.ForeignKey(Spec, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    guild = models.CharField(max_length=528, null=True, blank=True, default=None)
    level = models.IntegerField(null=False)
    active_title = models.CharField(max_length=2000, null=True, blank=True, default=None)
    talents = models.ManyToManyField(Talent, blank=True, default=None)
    pvp_talents = models.ManyToManyField(PvpTalent, blank=True, default=None)
    covenant = models.ForeignKey(Covenant, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    covenant_rank = models.IntegerField(null=True, blank=True, default=None)
    soulbind = models.ForeignKey(Soulbind, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    soulbind_abilities = models.ManyToManyField(SoulbindTrait, blank=True, default=None)
    conduits = models.ManyToManyField(CharacterConduit, blank=True, default=None)
    item_level = models.IntegerField(null=False)
    media = models.CharField(max_length=1064, null=False)
    avatar = models.CharField(max_length=1064, null=False)
    ratings = models.ManyToManyField(PvpBracketStatistics, blank=True, default=None)
    achievement_points = models.IntegerField(null=False)
    achievements = models.ManyToManyField(CharacterAchievement, blank=True, default=None)
    achievements_completed = models.ManyToManyField(Achievement, blank=True, default=None)
    max_2v2_rating = models.IntegerField(null=True, blank=True, default=None)
    max_3v3_rating = models.IntegerField(null=True, blank=True, default=None)
    max_5v5_rating = models.IntegerField(null=True, blank=True, default=None)
    max_rbg_rating = models.IntegerField(null=True, blank=True, default=None)
    alters = models.ManyToManyField('self', blank=True, default=None)
    last_update = models.DateTimeField(default=timezone.now)
    last_search = models.DateTimeField(default=timezone.now)
    checked = models.IntegerField(default=1)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name + '-' + self.realm.name

class PvpEntry2v2(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, null=False)
    season = models.ForeignKey(PvpSeason, on_delete=models.CASCADE, null=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=False)
    rank = models.IntegerField(null=False)
    rating = models.IntegerField(null=False)
    won = models.IntegerField(null=False)
    lost = models.IntegerField(null=False)
    played = models.IntegerField(null=False)
    winratio = models.IntegerField(null=False)
    time = models.DateTimeField(null=False, default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['character', 'time']),
        ]

    def __str__(self):
        return self.character.name + ' ' + str(self.rating)

class PvpEntry3v3(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, null=False)
    season = models.ForeignKey(PvpSeason, on_delete=models.CASCADE, null=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=False)
    rank = models.IntegerField(null=False)
    rating = models.IntegerField(null=False)
    won = models.IntegerField(null=False)
    lost = models.IntegerField(null=False)
    played = models.IntegerField(null=False)
    winratio = models.IntegerField(null=False)
    time = models.DateTimeField(null=False, default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['character', 'time']),
        ]

    def __str__(self):
        return self.character.name + ' ' + str(self.rating)

class PvpEntryRbg(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, null=False)
    season = models.ForeignKey(PvpSeason, on_delete=models.CASCADE, null=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=False)
    rank = models.IntegerField(null=False)
    rating = models.IntegerField(null=False)
    won = models.IntegerField(null=False)
    lost = models.IntegerField(null=False)
    played = models.IntegerField(null=False)
    winratio = models.IntegerField(null=False)
    time = models.DateTimeField(null=False, default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['character', 'time']),
        ]

    def __str__(self):
        return self.character.name + ' ' + str(self.rating)

class PvpEntry2v2Historical(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, null=False)
    season = models.ForeignKey(PvpSeason, on_delete=models.CASCADE, null=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=False)
    rank = models.IntegerField(null=False)
    rating = models.IntegerField(null=False)
    won = models.IntegerField(null=False)
    lost = models.IntegerField(null=False)
    played = models.IntegerField(null=False)
    winratio = models.IntegerField(null=False)
    time = models.DateTimeField(null=False, default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['character', 'time']),
        ]

    def __str__(self):
        return self.character.name + ' ' + str(self.rating)

class PvpEntry3v3Historical(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, null=False)
    season = models.ForeignKey(PvpSeason, on_delete=models.CASCADE, null=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=False)
    rank = models.IntegerField(null=False)
    rating = models.IntegerField(null=False)
    won = models.IntegerField(null=False)
    lost = models.IntegerField(null=False)
    played = models.IntegerField(null=False)
    winratio = models.IntegerField(null=False)
    time = models.DateTimeField(null=False, default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['character', 'time']),
        ]

    def __str__(self):
        return self.character.name + ' ' + str(self.rating)

class PvpEntryRbgHistorical(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, null=False)
    season = models.ForeignKey(PvpSeason, on_delete=models.CASCADE, null=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=False)
    rank = models.IntegerField(null=False)
    rating = models.IntegerField(null=False)
    won = models.IntegerField(null=False)
    lost = models.IntegerField(null=False)
    played = models.IntegerField(null=False)
    winratio = models.IntegerField(null=False)
    time = models.DateTimeField(null=False, default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['character', 'time']),
        ]

    def __str__(self):
        return self.character.name + ' ' + str(self.rating)

