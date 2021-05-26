from .models import PvpSeason, PvpSeasonReward, PvpEntry, PvpBracket, PvpBracketStatistics, Realm, Region, Race, Faction, WowClass, Spec, Language, Talent
from .models import PvpTalent, Covenant, Soulbind, SoulbindTrait, Conduit, Achievement, Character, CharacterConduit, CharacterAchievement
import requests, os
from requests.auth import HTTPBasicAuth
from datetime import datetime
import time
from django.utils.timezone import make_aware
from django.utils import timezone

my_headers = ''

def get_token():
    query = { 'grant_type': 'client_credentials' }
    response = requests.post(
        "https://eu.battle.net/oauth/token",
        params=query,
        auth=HTTPBasicAuth('94f8968fb33c4ba7a2b70c52f11ef232','32hTr9BKNlGJ7Vi8VWnV5nUhH6b2gVCx')
    )
    token = response.json()['access_token']
    global my_headers
    my_headers = {'Authorization': 'Bearer ' + token}

def make_request(url, query):
    if my_headers == '':
        get_token()
    
    response = requests.get(url, headers=my_headers, params=query)

    return response

    # if response.status_code == 200 or response.status_code == 404:
    #     resjson = response.json()
    #     return resjson
    # else:
    #     print(response.text + ' ' + url)

def update_realms():
    Realm.objects.all().delete()
    regions = Region.objects.all()

    if os.path.isdir('static/img/realm') == False:
        os.makedirs('static/img/realm')

    for region in regions:
        query = { 'region': region.name, 'namespace': 'dynamic-' + region.name, 'locale': 'en_US' }
        response = make_request('https://' + region.name + '.api.blizzard.com/data/wow/realm/index', query)
        
        if response.status_code == 200:
            response = response.json()

            for realm in response['realms']:
                query = { 'region': region.name, 'namespace': 'dynamic-' + region.name, 'locale': 'en_US' }
                response = make_request('https://' + region.name + '.api.blizzard.com/data/wow/realm/' + realm['slug'], query)
                if response.status_code == 200:
                    response = response.json()
                    singlerealm = response
                    objregion = Region.objects.get(name=region)
                    locale = singlerealm['locale']
                    locale = locale[0:2] + '_' + locale[2:4]
                    icon = 'static/img/realm/' + str.lower(singlerealm['category']) + '.png'
                    objrealm = Realm(
                        name = realm['name'],
                        rid = realm['id'],
                        slug = realm['slug'],
                        region = objregion,
                        category = singlerealm['category'],
                        locale = locale,
                        timezone = singlerealm['timezone'],
                        rtype = singlerealm['type']['type'],
                        icon = icon,
                    )
                    objrealm.save()
        else:
            print('Error making request: https://' + region.name + '.api.blizzard.com/data/wow/realm/index')
            print(response.text)

def update_races():
    Race.objects.all().delete()
    langs = Language.objects.all()

    possible_clases = {
        'blood_elf': [6,12,3,8,10,2,5,4,9,1],
        'orc': [6,3,8,10,4,7,9,1],
        'draenei': [6,3,8,10,2,5,7,1],
        'zandalari_troll': [11,6,3,8,10,2,5,4,7,1],
        'troll': [11,6,3,8,10,9,5,4,7,1],
        'vulpera': [6,3,8,10,9,5,4,7,1],
        'kul_tiran': [6,3,8,10,11,5,4,7,1],
        'nightborne': [6,3,8,10,9,5,4,1],
        'void_elf': [6,3,8,10,9,5,4,1],
        'undead': [6,3,8,10,9,5,4,1],
        'tauren': [6,11,3,10,2,5,7,1],
        'mechagnome': [6,3,8,10,9,5,4,1],
        'highmountain_tauren': [6,11,3,10,7,1],
        'goblin': [6,3,8,5,4,7,9,1],
        'human': [6,3,8,10,2,5,4,9,1],
        'dwarf': [6,3,8,10,2,5,4,9,1,7],
        'dark_iron_dwarf': [6,3,8,10,2,5,4,9,1,7],
        'night_elf': [6,12,11,3,8,10,5,4,1],
        'worgen': [6,11,3,8,5,4,9,1],
        'lightforged_draenei': [6,3,8,2,5,1],
        'mag\'har_orc': [6,3,8,10,5,4,7,1],
        'gnome': [6,3,8,10,5,4,9,1],
        'pandaren': [6,3,8,10,5,4,7,1],
    }

    if os.path.isdir('static/img/race') == False:
        os.makedirs('static/img/race')

    query = { 'region': 'eu', 'namespace': 'static-eu', 'locale': 'en_US' }
    response = make_request('https://eu.api.blizzard.com/data/wow/playable-race/index', query)

    if response.status_code == 200:

        response = response.json()
        data = response['races']

        for item in data:
            race = {}

            iconmale = 'static/img/race/' + str(item['id']) + '_male.png'
            iconfemale = 'static/img/race/' + str(item['id']) + '_female.png'
            imgmalerequest = requests.get('https://xunamate-assets.fra1.cdn.digitaloceanspaces.com/img/icons/races/' + str(item['id']) + '_MALE.png')
            imgfemalerequest = requests.get('https://xunamate-assets.fra1.cdn.digitaloceanspaces.com/img/icons/races/' + str(item['id']) + '_FEMALE.png')
            imgmale = open(iconmale, "wb")
            imgfemale = open(iconfemale, "wb")
            imgmale.write(imgmalerequest.content)
            imgfemale.write(imgfemalerequest.content)
            imgmale.close()
            imgfemale.close()
            race['icon_male'] = iconmale
            race['icon_female'] = iconfemale

            for lang in langs:
                query = { 'region': 'eu', 'namespace': 'static-eu', 'locale': lang.code }
                response = make_request('https://eu.api.blizzard.com/data/wow/playable-race/' + str(item['id']), query)
                if response.status_code == 200:
                    response = response.json()
                    single = response
                    if lang.name == 'English':
                        race['name'] = single['name']
                        race['rid'] = single['id']
                        obj = Faction.objects.get(name=single['faction']['name'])
                        race['faction'] = obj
                        race['is_allied_race'] = single['is_allied_race']
                    if lang.name == 'Spanish':
                        race['name_es'] = single['name']
                else:
                    print('Error making request: https://eu.api.blizzard.com/data/wow/playable-race/' + str(item['id']))
                    print(response.text)
                    
            raze = Race(**race)
            raze.save()

            for key, value in possible_clases.items():
                key = key.replace('_', ' ')
                if str.lower(item['name']) == key:
                    for cid in value:
                        wow_class = WowClass.objects.get(cid=cid)
                        raze.wow_clases.add(wow_class)
    else:
        print('Error making request: https://eu.api.blizzard.com/data/wow/playable-race/index')
        print(response.text)

def update_classes():
    colors = {
        'warlock': '#8788EE',
        'death_knight': '#C41E3A',
        'hunter': '#AAD372',
        'demon_hunter': '#A330C9',
        'shaman': '#0070DD',
        'druid': '#FF7C0A',
        'warrior': '#C69B6D',
        'mage': '#3FC7EB',
        'monk': '#00FF98',
        'paladin': '#F48CBA',
        'rogue': '#FFF468',
        'priest': '#FFFFFF'
    }

    WowClass.objects.all().delete()
    langs = Language.objects.all()

    if os.path.isdir('static/img/class') == False:
        os.makedirs('static/img/class')
    
    query = { 'region': 'eu', 'namespace': 'static-eu', 'locale': 'en_US' }
    response = make_request('https://eu.api.blizzard.com/data/wow/playable-class/index', query)

    if response.status_code == 200:
        response = response.json()
    
        data = response['classes']

        for item in data:
            class_data = {}

            icon = 'static/img/class/' + str(item['id']) + '.jpg'
            query = { 'region': 'eu', 'namespace': 'static-eu', 'locale': 'en_US' }
            responsemedia = make_request('https://eu.api.blizzard.com/data/wow/media/playable-class/' + str(item['id']), query)
            if responsemedia.status_code == 200:
                responsemedia = responsemedia.json()
                media = responsemedia
                imgrequest = requests.get(media['assets'][0]['value'])
                img = open(icon, "wb")
                img.write(imgrequest.content)
                img.close()
                class_data['icon'] = icon

                for lang in langs:
                    query = { 'region': 'eu', 'namespace': 'static-eu', 'locale': lang.code }
                    response = make_request('https://eu.api.blizzard.com/data/wow/playable-class/' + str(item['id']), query)
                    if response.status_code == 200:
                        response = response.json()
                        single = response

                        for key, value in colors.items():
                            key = key.replace('_', ' ')
                            if str.lower(single['name']) == key:
                                class_data['color'] = value
                                
                        if lang.name == 'English':
                            class_data['name'] = single['name']
                            class_data['cid'] = single['id']
                            class_data['power_type'] = single['power_type']['name']
                        if lang.name == 'Spanish':
                            class_data['name_es'] = single['name']
                    else:
                        print('Error making request: https://eu.api.blizzard.com/data/wow/playable-class/' + str(item['id']))
                        print(response.text)
            else:
                print('Error making request: https://eu.api.blizzard.com/data/wow/media/playable-class/' + str(item['id']))
                print(responsemedia.text)

            wow_class = WowClass(**class_data)
            wow_class.save()
    else:
        print('Error making request: https://eu.api.blizzard.com/data/wow/playable-class/index')
        print(response.text)
    

def update_specs():
    Spec.objects.all().delete()
    langs = Language.objects.all()

    if os.path.isdir('static/img/spec') == False:
        os.makedirs('static/img/spec')

    query = { 'region': 'eu', 'namespace': 'static-eu', 'locale': 'en_US' }
    response = make_request('https://eu.api.blizzard.com/data/wow/playable-specialization/index', query)

    if response.status_code == 200:
        response = response.json()
        data = response['character_specializations']
        
        for item in data:
            spec_data = {}

            icon = 'static/img/spec/' + str(item['id']) + '.png'
            query = { 'region': 'eu', 'namespace': 'static-eu', 'locale': 'en_US' }
            responsemedia = make_request('https://eu.api.blizzard.com/data/wow/media/playable-specialization/' + str(item['id']), query)
            if responsemedia.status_code == 200:
                responsemedia = responsemedia.json()
                media = responsemedia
                imgrequest = requests.get(media['assets'][0]['value'])
                img = open(icon, "wb")
                img.write(imgrequest.content)
                img.close()
                spec_data['icon'] = icon

                for lang in langs:
                    query = { 'region': 'eu', 'namespace': 'static-eu', 'locale': lang.code }
                    response = make_request('https://eu.api.blizzard.com/data/wow/playable-specialization/' + str(item['id']), query)
                    if response.status_code == 200:
                        response = response.json()
                        single = response
                        if lang.name == 'English':
                            spec_data['name'] = single['name']
                            spec_data['sid'] = single['id']
                            obj = WowClass.objects.get(cid=single['playable_class']['id'])
                            spec_data['wow_class'] = obj
                            spec_data['description'] = single['gender_description']['male']
                            spec_data['role'] = single['role']['name']
                            spec_data['talents'] = single['talent_tiers']
                            spec_data['pvp_talents'] = single['pvp_talents']
                            
                        if lang.name == 'Spanish':
                            spec_data['name_es'] = single['name']
                            spec_data['description_es'] = single['gender_description']['male']
                    else:
                        print('Error making request: https://eu.api.blizzard.com/data/wow/playable-specialization/' + str(item['id']))
                        print(response.text)
            else:
                print('Error making request: https://eu.api.blizzard.com/data/wow/media/playable-specialization/' + str(item['id']))
                print(responsemedia.text)

            spec = Spec(**spec_data)
            spec.save()
    else:
        print('Error making request: https://eu.api.blizzard.com/data/wow/playable-specialization/index')
        print(response.text)

def update_talents():
    Talent.objects.all().delete()
    langs = Language.objects.all()

    if os.path.isdir('static/img/talent') == False:
        os.makedirs('static/img/talent')

    query = { 'region': 'eu', 'namespace': 'static-eu', 'locale': 'en_US' }
    response = make_request('https://eu.api.blizzard.com/data/wow/talent/index', query)
    if response.status_code == 200:
        response = response.json()
        data = response['talents']

        for item in data:
            talent_data = {}

            for lang in langs:

                query = { 'region': 'eu', 'namespace': 'static-eu', 'locale': lang.code }
                response = make_request('https://eu.api.blizzard.com/data/wow/talent/' + str(item['id']), query)
                if response.status_code == 200:
                    response = response.json()
                    single = response

                    if lang.name == 'English':
                        icon = 'static/img/talent/' + str(item['id']) + '.png'
                        responsemedia = make_request('https://eu.api.blizzard.com/data/wow/media/spell/' + str(single['spell']['id']), query)
                        if responsemedia.status_code == 200:
                            responsemedia = responsemedia.json()
                            media = responsemedia
                            imgrequest = requests.get(media['assets'][0]['value'])
                            img = open(icon, "wb")
                            img.write(imgrequest.content)
                            img.close()
                            talent_data['icon'] = icon
                            
                            objc = WowClass.objects.get(cid=single['playable_class']['id'])
                            talent_data['name'] = single['spell']['name']
                            talent_data['talent_id'] = single['id']
                            talent_data['spell_id'] = single['spell']['id']
                            talent_data['wow_class'] = objc
                            talent_data['description'] = single['description']
                            talent_data['tier_index'] = single['tier_index']
                            talent_data['column_index'] = single['column_index']
                            talent_data['level'] = single['level']
                        else:
                            print('Error making request: https://eu.api.blizzard.com/data/wow/media/spell/' + str(single['spell']['id']))
                            print(responsemedia.text)

                    if lang.name == 'Spanish':
                        talent_data['name_es'] = single['spell']['name']
                        talent_data['description_es'] = single['description']
                else:
                    print('Error making request: https://eu.api.blizzard.com/data/wow/talent/' + str(item['id']))
                    print(response.text)

            talent = Talent(**talent_data)
            talent.save()

            objs = Spec.objects.filter(wow_class=talent_data['wow_class'])
            for spec in objs:
                if spec.talents[single['tier_index']]['talents'][single['column_index']]['talent']['id'] == single['id']:
                    talent.spec.add(spec)
    else:
        print('Error making request: https://eu.api.blizzard.com/data/wow/talent/index')
        print(response.text)

def update_pvp_talents():
    PvpTalent.objects.all().delete()
    langs = Language.objects.all()

    if os.path.isdir('static/img/pvp_talent') == False:
        os.makedirs('static/img/pvp_talent')
    
    query = { 'region': 'eu', 'namespace': 'static-eu', 'locale': 'en_US' }
    response = make_request('https://eu.api.blizzard.com/data/wow/pvp-talent/index', query)
    if response.status_code == 200:
        response = response.json()
        data = response['pvp_talents']
        for item in data:
            pvp_talent_data = {}

            for lang in langs:
                query = { 'region': 'eu', 'namespace': 'static-eu', 'locale': lang.code }
                response = make_request('https://eu.api.blizzard.com/data/wow/pvp-talent/' + str(item['id']), query)
                if response.status_code == 200:
                    response = response.json()
                    single = response

                    if lang.name == 'English':
                        icon = 'static/img/pvp_talent/' + str(item['id']) + '.png'
                        responsemedia = make_request('https://eu.api.blizzard.com/data/wow/media/spell/' + str(single['spell']['id']), query)
                        if responsemedia.status_code == 200:
                            responsemedia = responsemedia.json()
                            media = responsemedia
                            imgrequest = requests.get(media['assets'][0]['value'])
                            img = open(icon, "wb")
                            img.write(imgrequest.content)
                            img.close()
                            pvp_talent_data['icon'] = icon

                            objts = Spec.objects.get(sid=single['playable_specialization']['id'])
                            objc = WowClass.objects.get(cid=objts.wow_class.cid)
                            pvp_talent_data['name'] = single['spell']['name']
                            pvp_talent_data['spell_id'] = single['spell']['id']
                            pvp_talent_data['talent_id'] = single['id']
                            pvp_talent_data['wow_class'] = objc
                            pvp_talent_data['spec'] = objts
                            pvp_talent_data['description'] = single['description']
                            pvp_talent_data['level'] = single['unlock_player_level']
                    if lang.name == 'Spanish':
                        pvp_talent_data['name_es'] = single['spell']['name']
                        pvp_talent_data['description_es'] = single['description']

            talent = PvpTalent(**pvp_talent_data)
            talent.save()

def update_achievements():
    character_wide = [
        #RBG
        6941,6942,5337,5343,5356,5353,5342,5352,5330,5331,5350,5359,5351,5340,5355,5335,5332,5338,5333,5336,5339,5354,5341,5357,5347,5349,5348,5334,5345,5346,
        #ARENA
        2091,2092,2090,2093,1159,5267,399,5266,400,401,1160,402,405,403,
        #SEASONS
        14690,14685,14689,13967,13639,13641,13634,13199,14687,14686,14688,13200,9239,3336,14691,12168,13957,11014,13465,12961,8214,420,12952,13964,8666,9232,
        12185,419,12945,13989,4599,13209,8667,11015,10099,11062,3436,10110,8643,418,13630,12171,13676,13647,11038,11061,12167,12035,8791,12959,12036,13204,
        11037,12134,13642,13963,11027,6124,11017,11028,9242,13962,12034,12186,9240,13451,12010,12960,6002,11012,6938,11060,12187,8649,11041,11058,11011,13205,11040,
        11059,10097,13203,13959,11039,12169,10101,10113,11026,10111,11013,12045,10098,3758,11016,9241,10100,10112,13212,12170,12188,10096,13210,13211,13643,13644,
        13966,13965,14693,14692
    ]
    account_wide = [
        11132,11131,11130,11129,11128,11127,11126,239,869,870,5363,12515,12245,13163,12243,12518,14013,12244,12242,13206,13161,14418,12807,7410,7411,
        11715,6924,5751,3496,5845,11137,7462,14881,11743,1516,11136,7465,4626,13762,12020,2076,885,11761,12947,12988,14027,7483,11748,1312,6555
    ]

    Achievement.objects.all().delete()
    langs = Language.objects.all()

    if os.path.isdir('static/img/achievement') == False:
        os.makedirs('static/img/achievement')

    for item in character_wide:
        achieve_data = {}

        for lang in langs:
            query = { 'region': 'eu', 'namespace': 'static-eu', 'locale': lang.code }
            response = make_request('https://eu.api.blizzard.com/data/wow/achievement/' + str(item), query)
            if response.status_code == 200:
                response = response.json()
                single = response

                if lang.name == 'English':
                    icon = 'static/img/achievement/' + str(item) + '.png'
                    responsemedia = make_request('https://eu.api.blizzard.com/data/wow/media/achievement/' + str(item), query)
                    if responsemedia.status_code == 200:
                        responsemedia = responsemedia.json()
                        media = responsemedia
                        imgrequest = requests.get(media['assets'][0]['value'])
                        img = open(icon, "wb")
                        img.write(imgrequest.content)
                        img.close()
                        achieve_data['icon'] = icon
                        achieve_data['name'] = single['name']
                        achieve_data['description'] = single['description']
                        achieve_data['is_account_wide'] = single['is_account_wide']
                        achieve_data['aid'] = single['id']
                        achieve_data['points'] = single['points']
                
                if lang.name == 'Spanish':
                    achieve_data['name_es'] = single['name']
                    achieve_data['description_es'] = single['description'] 

        achievement = Achievement(**achieve_data)
        achievement.save()

    for item in account_wide:
        achieve_data = {}

        for lang in langs:
            query = { 'region': 'eu', 'namespace': 'static-eu', 'locale': lang.code }
            response = make_request('https://eu.api.blizzard.com/data/wow/achievement/' + str(item), query)
            if response.status_code == 200:
                response = response.json()
                single = response

                if lang.name == 'English':
                    icon = 'static/img/achievement/' + str(item) + '.png'
                    responsemedia = make_request('https://eu.api.blizzard.com/data/wow/media/achievement/' + str(item), query)
                    if responsemedia.status_code == 200:
                        responsemedia = responsemedia.json()
                        media = responsemedia
                        imgrequest = requests.get(media['assets'][0]['value'])
                        img = open(icon, "wb")
                        img.write(imgrequest.content)
                        img.close()
                        achieve_data['icon'] = icon
                        achieve_data['name'] = single['name']
                        achieve_data['description'] = single['description']
                        achieve_data['is_account_wide'] = single['is_account_wide']
                        achieve_data['aid'] = single['id']
                        achieve_data['points'] = single['points']
                
                if lang.name == 'Spanish':
                    achieve_data['name_es'] = single['name']
                    achieve_data['description_es'] = single['description'] 

        achievement = Achievement(**achieve_data)
        achievement.save()

def update_covenant():
    Covenant.objects.all().delete()
    langs = Language.objects.all()

    if os.path.isdir('static/img/covenant') == False:
        os.makedirs('static/img/covenant')
    
    query = { 'region': 'eu', 'namespace': 'static-eu', 'locale': 'en_US' }
    response = make_request('https://eu.api.blizzard.com/data/wow/covenant/index', query)
    if response.status_code == 200:
        response = response.json()
        data = response['covenants']

        for item in data:
            covenant_data = {}

            for lang in langs:
                icon = 'static/img/covenant/' + str(item['id']) + '.png'
                responsemedia = make_request('https://eu.api.blizzard.com/data/wow/media/covenant/' + str(item['id']), query)
                if responsemedia.status_code == 200:
                    responsemedia = responsemedia.json()
                    media = responsemedia
                    imgrequest = requests.get(media['assets'][0]['value'])
                    img = open(icon, "wb")
                    img.write(imgrequest.content)
                    img.close()
                    covenant_data['icon'] = icon

                    query = { 'region': 'eu', 'namespace': 'static-eu', 'locale': lang.code }
                    response = make_request('https://eu.api.blizzard.com/data/wow/covenant/' + str(item['id']), query)
                    if response.status_code == 200:
                        response = response.json()
                        single = response

                        if lang.name == 'English':
                            covenant_data['name'] = single['name']
                            covenant_data['description'] = single['description']
                            covenant_data['cid'] = single['id']

                        if lang.name == 'Spanish':
                            covenant_data['name_es'] = single['name']
                            covenant_data['description_es'] = single['description']

            covenant = Covenant(**covenant_data)
            covenant.save()

def update_soulbinds():
    Soulbind.objects.all().delete()
    langs = Language.objects.all()

    if os.path.isdir('static/img/soulbind') == False:
        os.makedirs('static/img/soulbind')

    query = { 'region': 'eu', 'namespace': 'static-eu', 'locale': 'en_US' }
    response = make_request('https://eu.api.blizzard.com/data/wow/covenant/soulbind/index', query)
    if response.status_code == 200:
        response = response.json()
        data = response['soulbinds']

        for item in data:
            soulbind_data = {}

            for lang in langs:
                query = { 'region': 'eu', 'namespace': 'static-eu', 'locale': lang.code }
                response = make_request('https://eu.api.blizzard.com/data/wow/covenant/soulbind/' + str(item['id']), query)
                if response.status_code == 200:
                    response = response.json()
                    single = response
                    obj = Covenant.objects.get(cid=single['covenant']['id'])
                    if lang.name == 'English':
                        soulbind_data['name'] = single['name']
                        soulbind_data['covenant'] = obj
                        soulbind_data['sid'] = item['id']
                    
                    if lang.name == 'Spanish':
                        soulbind_data['name_es'] = single['name']

            soulbind = Soulbind(**soulbind_data)
            soulbind.save()

def update_soulbinds_traits():
    SoulbindTrait.objects.all().delete()
    langs = Language.objects.all()

    if os.path.isdir('static/img/soulbind_trait') == False:
        os.makedirs('static/img/soulbind_trait')

    query = { 'region': 'eu', 'namespace': 'static-eu', 'locale': 'en_US' }
    response = make_request('https://eu.api.blizzard.com/data/wow/tech-talent/index', query)
    if response.status_code == 200:
        response = response.json()
        data = response['talents']
        
        for item in data:
            item_data = {}

            query = { 'region': 'eu', 'namespace': 'static-eu', 'locale': 'en_US' }
            response = make_request('https://eu.api.blizzard.com/data/wow/tech-talent/' + str(item['id']), query)
            if response.status_code == 200:
                response = response.json()
                single = response

                if single['spell_tooltip']['cast_time'] not in ('Passive', 'Pasivo'):
                    continue
                if single['talent_tree']['name'].find('Maldraxxus') != -1 or single['talent_tree']['name'].find('Bastion') != -1 or single['talent_tree']['name'].find('Ardenweald') != -1  or single['talent_tree']['name'].find('Revendreth') != -1:
                    continue

                icon = 'static/img/soulbind_trait/' + str(item['id']) + '.png'
                responsemedia = make_request('https://eu.api.blizzard.com/data/wow/media/tech-talent/' + str(item['id']), query)
                if responsemedia.status_code == 200:
                    responsemedia = responsemedia.json()
                    media = responsemedia
                    imgrequest = requests.get(media['assets'][0]['value'])
                    img = open(icon, "wb")
                    img.write(imgrequest.content)
                    img.close()
                    item_data['icon'] = icon

                    for lang in langs:
                        query = { 'region': 'eu', 'namespace': 'static-eu', 'locale': lang.code }
                        response = make_request('https://eu.api.blizzard.com/data/wow/tech-talent/' + str(item['id']), query)
                        if response.status_code == 200:
                            response = response.json()
                            single = response

                            if lang.name == 'English':
                                if single['talent_tree']['name'] == 'Mikanikos':
                                    single['talent_tree']['name'] = 'Forgelite Prime Mikanikos'
                                item_data['name'] = single['name']
                                item_data['sid'] = single['id']
                                item_data['spell_id'] = single['spell_tooltip']['spell']['id']
                                item_data['description'] = single['spell_tooltip']['description']
                                obj = Soulbind.objects.get(name=single['talent_tree']['name'])
                                item_data['soulbind'] = obj

                            if lang.name == 'Spanish':
                                if single['talent_tree']['name'] == 'Mikanikos':
                                    single['talent_tree']['name'] = 'Forjador supremo Mikanikos'
                                item_data['name_es'] = single['name']
                                item_data['description_es'] = single['spell_tooltip']['description']
                
            soulbind_trait = SoulbindTrait(**item_data)
            soulbind_trait.save()

def update_conduit():
    Conduit.objects.all().delete()
    langs = Language.objects.all()

    if os.path.isdir('static/img/conduit') == False:
        os.makedirs('static/img/conduit')

    query = { 'region': 'eu', 'namespace': 'static-eu', 'locale': 'en_US' }
    response = make_request('https://eu.api.blizzard.com/data/wow/covenant/conduit/index', query)
    if response.status_code == 200:
        response = response.json()
        data = response['conduits']

        for item in data:
            conduit_data = {}

            for lang in langs:
                query = { 'region': 'eu', 'namespace': 'static-eu', 'locale': lang.code }
                response = make_request('https://eu.api.blizzard.com/data/wow/covenant/conduit/' + str(item['id']), query)
                if response.status_code == 200:
                    response = response.json()
                    single = response

                    icon = 'static/img/conduit/' + str(item['id']) + '.png'
                    responsemedia = make_request('https://eu.api.blizzard.com/data/wow/media/spell/' + str(single['ranks'][0]['spell_tooltip']['spell']['id']), query)
                    if responsemedia.status_code == 200:
                        responsemedia = responsemedia.json()
                        media = responsemedia
                        imgrequest = requests.get(media['assets'][0]['value'])
                        img = open(icon, "wb")
                        img.write(imgrequest.content)
                        img.close()
                        conduit_data['icon'] = icon

                        if lang.name == 'English':
                            conduit_data['name'] = single['name']
                            conduit_data['cid'] = single['id']
                            conduit_data['ranks'] = single['ranks']
                            conduit_data['type'] = single['socket_type']['type']

                        if lang.name == 'Spanish':
                            conduit_data['name_es'] = single['name']

            conduit = Conduit(**conduit_data)
            conduit.save()

def update_pvp_seasons():
    PvpSeasonReward.objects.all().delete()
    PvpSeason.objects.all().delete()
    regions = Region.objects.all()

    active = 0

    query = { 'region': 'eu', 'namespace': 'dynamic-eu', 'locale': 'en_US' }
    response = make_request('https://eu.api.blizzard.com/data/wow/pvp-season/index', query)
    if response.status_code == 200:
        response = response.json()
        data = response

        if data:
            if 'current_season' in data:
                    active = data['current_season']['id']

            for item in data['seasons']:
                if item['id'] > 26:
                    response = make_request('https://eu.api.blizzard.com/data/wow/pvp-season/' + str(item['id']), query)
                    if response.status_code == 200:
                        response = response.json()
                        single = response

                        if single:
                            season = PvpSeason(
                                sid = single['id'],
                                season_start_timestamp = datetime.fromtimestamp(single['season_start_timestamp'] / 1000)
                            )
                            season.save()
                            if season.sid == active:
                                season.is_active = True
                                season.save()
                            if 'season_end_timestamp' in single:
                                season.season_end_timestamp = datetime.fromtimestamp(single['season_end_timestamp'] / 1000)
                                season.save()

                            for region in regions:
                                query2 = { 'region': region.name, 'namespace': 'dynamic-' + region.name, 'locale': 'en_US' }
                                response = make_request('https://' + region.name + '.api.blizzard.com/data/wow/pvp-season/' + str(season.sid) + '/pvp-reward/index', query2)
                                if response.status_code == 200:
                                    response = response.json()
                                    if response:
                                        singledata = response['rewards']

                                        for item2 in singledata:
                                            season_reward = PvpSeasonReward(
                                                achievement = Achievement.objects.get(aid=item2['achievement']['id']),
                                                region = Region.objects.get(id=region.id),
                                                bracket = PvpBracket.objects.get(pvp_type=item2['bracket']['type']),
                                                faction = Faction.objects.get(name=item2['faction']['name']),
                                                cutoff = item2['rating_cutoff'],
                                            )
                                            season_reward.save()
                                            season.rewards.add(season_reward)

#@background(schedule=7200)
def get_entries():

    regions = Region.objects.all()
    season = PvpSeason.objects.get(is_active=True)
    brackets = PvpBracket.objects.all()

    for region in regions:
        for bracket in brackets:
            safebracket = bracket.pvp_type
            safebracket = safebracket.replace('ARENA_', '')
            safebracket = safebracket.replace('BATTLEGROUNDS', 'rbg')
            query = { 'region': region.name, 'namespace': 'dynamic-' + region.name, 'locale': 'en_GB' }
            response = make_request('https://' + region.name + '.api.blizzard.com/data/wow/pvp-season/' + str(season.sid) + '/pvp-leaderboard/' + safebracket, query)
            if response.status_code == 200:
                response = response.json()
                data = response['entries']

                for item in data:
                    character = Character.objects.filter(cid=item['character']['id'])
                    if character:
                        character = Character.objects.get(cid=item['character']['id'])
                        pvp_entry = PvpEntry(
                            character = character,
                            bracket = bracket,
                            season=season,
                            region=region,
                            rank = item['rank'],
                            rating = item['rating'],
                            won = item['season_match_statistics']['won'],
                            lost = item['season_match_statistics']['lost'],
                            played = item['season_match_statistics']['played'],
                            winratio = (item['season_match_statistics']['won'] * 100) / item['season_match_statistics']['played']
                        )
                        pvp_entry.save()
                    else:
                        get_character(str.lower(item['character']['name']), region, Realm.objects.get(rid=item['character']['realm']['id']))
                        character = Character.objects.filter(cid=item['character']['id'])
                        if character:
                            character = Character.objects.get(cid=item['character']['id'])
                            pvp_entry = PvpEntry(
                                character = character,
                                bracket = bracket,
                                season=season,
                                region=region,
                                rank = item['rank'],
                                rating = item['rating'],
                                won = item['season_match_statistics']['won'],
                                lost = item['season_match_statistics']['lost'],
                                played = item['season_match_statistics']['played'],
                                winratio = (item['season_match_statistics']['won'] * 100) / item['season_match_statistics']['played']
                            )
                            pvp_entry.save()
                        else:
                            continue

def get_character(name, region, realm):

    #mytime = datetime.timestamp(datetime.now())

    character_data = {}

    query = { 'region': region.name, 'namespace': 'profile-' + region.name, 'locale': 'en_US' }
    response = make_request('https://' + region.name + '.api.blizzard.com/profile/wow/character/' + realm.slug + '/' + name, query)

    if response.status_code == 200:
        response = response.json()
    
        character_data['name'] = name
        character_data['cid'] = response['id']
        character_data['gender'] = response['gender']['name']
        if 'guild' in response:
            character_data['guild'] = response['guild']['name']
        character_data['level'] = response['level']
        character_data['achievement_points'] = response['achievement_points']
        character_data['region'] = region
        character_data['realm'] = realm
        character_data['item_level'] = response['equipped_item_level']
        if 'active_title' in response:
            character_data['active_title'] = response['active_title']['display_string']
        character_data['faction'] = Faction.objects.get(name=response['faction']['name'])
        character_data['race'] = Race.objects.get(rid=response['race']['id'])
        character_data['wow_class'] = WowClass.objects.get(cid=response['character_class']['id'])
        if 'active_spec' in response and 'id' in response['active_spec']:
            character_data['spec'] = Spec.objects.get(sid=response['active_spec']['id'])
        if 'covenant_progress' in response:
            character_data['covenant'] = Covenant.objects.get(cid=response['covenant_progress']['chosen_covenant']['id'])
            character_data['covenant_rank'] = response['covenant_progress']['renown_level']

        character_data['media'], character_data['avatar'] = get_media(name, realm, region, response['id'])

        character = Character(**character_data)
        character.save()

        get_max_ratings(character)
        
        current_rbg_rating = get_ratings(character)

        if 'specializations' in response:
            get_talents(character)

        if 'covenant_progress' in response and 'soulbinds' in response['covenant_progress']:
            get_soulbinds_conduits(character)
        
        get_logros(character, current_rbg_rating)

        get_alters(character)

        # lasttime = datetime.timestamp(datetime.now())
        # thetime = lasttime - mytime
        # print('added ' + name + ' in: ' + str(thetime))

        return True

    else:
        return False

def update_character(character):
    query = { 'region': character.region.name, 'namespace': 'profile-' + character.region.name, 'locale': 'en_US' }
    response = make_request('https://' + character.region.name + '.api.blizzard.com/profile/wow/character/' + character.realm.slug + '/' + character.name, query)
    
    if response.status_code == 200:
        response = response.json()
        
        if 'guild' in response:
            character.guild = response['guild']['name']
        if 'level' in response:
            character.level = response['level']
        if 'achievement_points' in response:
            character.achievement_points = response['achievement_points']
        if 'equiped_item_level' in response:
            character.item_level = response['equipped_item_level']
        if 'active_title' in response:
            character.active_title = response['active_title']['display_string']
        if 'faction' in response:
            character.faction = Faction.objects.get(name=response['faction']['name'])
        if 'race' in response:
            character.race = Race.objects.get(rid=response['race']['id'])
        if 'active_spec' in response and 'id' in response['active_spec']:
            character.spec = Spec.objects.get(sid=response['active_spec']['id'])
        if 'covenant_progress' in response:
            character.covenant = Covenant.objects.get(cid=response['covenant_progress']['chosen_covenant']['id'])
            character.covenant_rank = response['covenant_progress']['renown_level']

        character.media, character.avatar = get_media(character.name, character.realm, character.region, response['id'])

        get_max_ratings(character)
    
        current_rbg_rating = get_ratings(character)

        if 'specializations' in response:
            get_talents(character)

        if 'covenant_progress' in response and 'soulbinds' in response['covenant_progress']:
            get_soulbinds_conduits(character)
        
        get_logros(character, current_rbg_rating)

        character.last_update = timezone.now()

        character.save()

        return True
    
    else:
        character.delete()
        return False

def get_logros(character, current_rbg_rating):

    logros_rbg = {
        'alliance': [5330,5331,5332,5333,5334,5335,5336,5337,5359,5339,5314,5341,5357,5343],
        'horde': [5345,5346,5347,5348,5349,5350,5351,5352,5338,5353,5354,5355,5342,5356]
    }
    hay_flow = 0
    maximo_dutti = 1000

    query = { 'region': character.region.name, 'namespace': 'profile-' + character.region.name, 'locale': 'en_US' }
    responseachievements = make_request('https://' + character.region.name + '.api.blizzard.com/profile/wow/character/' + character.realm.slug + '/' + character.name + '/achievements', query)
    
    if responseachievements.status_code == 200:
        responseachievements = responseachievements.json()

        achs = Achievement.objects.all()

        character.achievements_completed.clear()
        character.achievements.clear()
        for achievement in responseachievements['achievements']:
            if 'criteria' in achievement and achievement['criteria']['is_completed'] == True:
                if 'completed_timestamp' in achievement:
                    mytime = datetime.fromtimestamp(achievement['completed_timestamp'] / 1000)
                    mytime = make_aware(mytime)
                    for achieve in achs:
                        if achieve.aid == achievement['id']:
                            character.achievements_completed.add(achieve)
                            objca = CharacterAchievement(achievement=achieve, date_completed=mytime)
                            objca.save()
                            character.achievements.add(objca)
                            # maximo logro rbg
                            if character.faction.name == 'Alliance':
                                for numlogro in logros_rbg['alliance']:
                                    if achieve.aid == numlogro:
                                        hay_flow = 1
                                        maximo_dutti = maximo_dutti + 100
                                        break                   
                            if character.faction.name == 'Horde':
                                for numlogro in logros_rbg['horde']:
                                    if achieve.aid == numlogro:
                                        hay_flow = 1
                                        maximo_dutti = maximo_dutti + 100
                                        break

        if hay_flow == 1:
            if current_rbg_rating > maximo_dutti:
                character.max_rbg_rating = current_rbg_rating
                character.save()
            else:         
                character.max_rbg_rating = maximo_dutti
                character.save()  
        else:
            if current_rbg_rating != 0:
                character.max_rbg_rating = current_rbg_rating
                character.save()

def get_talents(character):

    query = { 'region': character.region.name, 'namespace': 'profile-' + character.region.name, 'locale': 'en_US' }
    responsespec = make_request('https://' + character.region.name + '.api.blizzard.com/profile/wow/character/' + character.realm.slug + '/' + character.name + '/specializations', query)
    if responsespec.status_code == 200:
        responsespec = responsespec.json()
        responsespec = responsespec['specializations'][0]

        if 'pvp_talent_slots' in responsespec:
            character.pvp_talents.clear()
            for pvp_talent in responsespec['pvp_talent_slots']:
                talents = PvpTalent.objects.filter(talent_id=pvp_talent['selected']['talent']['id'])
                if talents:
                    talented = PvpTalent.objects.get(talent_id=pvp_talent['selected']['talent']['id'])
                    character.pvp_talents.add(talented)
                
        if 'talents' in responsespec:
            character.talents.clear()
            for talent in responsespec['talents']:
                talents = Talent.objects.filter(talent_id=talent['talent']['id'])
                if talents:
                    talented = Talent.objects.get(talent_id=talent['talent']['id'])
                    character.talents.add(talented)


def get_ratings(character):

    season = PvpSeason.objects.get(is_active=True)

    query = { 'region': character.region.name, 'namespace': 'profile-' + character.region.name, 'locale': 'en_US' }
    response2v2 = make_request('https://' + character.region.name + '.api.blizzard.com/profile/wow/character/' + character.realm.slug + '/' + character.name + '/pvp-bracket/2v2', query)
    response3v3 = make_request('https://' + character.region.name + '.api.blizzard.com/profile/wow/character/' + character.realm.slug + '/' + character.name + '/pvp-bracket/3v3', query)
    responserbg = make_request('https://' + character.region.name + '.api.blizzard.com/profile/wow/character/' + character.realm.slug + '/' + character.name + '/pvp-bracket/rbg', query)

    character.ratings.clear()

    if response2v2.status_code == 200:
        response2v2 = response2v2.json()
        if 'bracket' in response2v2:
            if response2v2['season']['id'] == season.sid:
                bracket2v2 = PvpBracket.objects.get(bid=response2v2['bracket']['id'])
                winratio = response2v2['season_match_statistics']['won'] * 100 / response2v2['season_match_statistics']['played']
                match_statistics = PvpBracketStatistics(
                    bracket=bracket2v2,
                    rating=response2v2['rating'],
                    won=response2v2['season_match_statistics']['won'],
                    lost=response2v2['season_match_statistics']['lost'],
                    played=response2v2['season_match_statistics']['played'],
                    winratio=round(winratio)
                )
                match_statistics.save()
                character.ratings.add(match_statistics)

    if response3v3.status_code == 200:
        response3v3 = response3v3.json()
        if 'bracket' in response3v3:
            if response3v3['season']['id'] == season.sid:
                bracket3v3 = PvpBracket.objects.get(bid=response3v3['bracket']['id'])
                winratio = response3v3['season_match_statistics']['won'] * 100 / response3v3['season_match_statistics']['played']
                match_statistics = PvpBracketStatistics(
                    bracket=bracket3v3,
                    rating=response3v3['rating'],
                    won=response3v3['season_match_statistics']['won'],
                    lost=response3v3['season_match_statistics']['lost'],
                    played=response3v3['season_match_statistics']['played'],
                    winratio=round(winratio)
                )
                match_statistics.save()
                character.ratings.add(match_statistics)

    current_rbg_rating = 0
    if responserbg.status_code == 200:
        responserbg = responserbg.json()
        if 'bracket' in responserbg:
            if responserbg['season']['id'] == season.sid:
                bracketrbg = PvpBracket.objects.get(bid=responserbg['bracket']['id'])
                winratio = responserbg['season_match_statistics']['won'] * 100 / responserbg['season_match_statistics']['played']
                match_statistics = PvpBracketStatistics(
                    bracket=bracketrbg,
                    rating=responserbg['rating'],
                    won=responserbg['season_match_statistics']['won'],
                    lost=responserbg['season_match_statistics']['lost'],
                    played=responserbg['season_match_statistics']['played'],
                    winratio=round(winratio)
                )
                match_statistics.save()
                character.ratings.add(match_statistics)
                current_rbg_rating = responserbg['rating']
    
    return current_rbg_rating

def get_max_ratings(character):

    query = { 'region': character.region.name, 'namespace': 'profile-' + character.region.name, 'locale': 'en_US' }
    responsestats = make_request('https://' + character.region.name + '.api.blizzard.com/profile/wow/character/' + character.realm.slug + '/' + character.name + '/achievements/statistics', query)

    if responsestats.status_code == 200:
        responsestats = responsestats.json()
        if 'code' in responsestats and responsestats['code'] == 404:
            pass
        else: 
            stats = responsestats['categories']

            max_data = {}

            for x in stats:
                if 'sub_categories' in x:
                    for y in x['sub_categories']:
                        if y['name'] == 'Rated Arenas':
                            for z in y['statistics']:
                                if z['id'] == 595:
                                    max_data['max_3v3_rating'] = z['quantity']
                                if z['id'] == 370:
                                    max_data['max_2v2_rating'] = z['quantity']
                                if z['id'] == 596:
                                    max_data['max_5v5_rating'] = z['quantity']
                else:
                    if x['name'] == 'Rated Arenas':
                        for z in x['statistics']:
                                if z['id'] == 595:
                                    max_data['max_3v3_rating'] = z['quantity']
                                if z['id'] == 370:
                                    max_data['max_2v2_rating'] = z['quantity']
                                if z['id'] == 596:
                                    max_data['max_5v5_rating'] = z['quantity']

            if 'max_2v2_rating' in max_data:
                character.max_2v2_rating = max_data['max_2v2_rating']
            if 'max_3v3_rating' in max_data:
                character.max_3v3_rating = max_data['max_3v3_rating']
            if 'max_5v5_rating' in max_data:
                character.max_5v5_rating = max_data['max_5v5_rating']

            character.save()

def get_media(name, realm, region, cid):

    media_path = ''
    avatar_path = ''

    query = { 'region': region.name, 'namespace': 'profile-' + region.name, 'locale': 'en_US' }
    responsemedia = make_request('https://' + region.name + '.api.blizzard.com/profile/wow/character/' + realm.slug + '/' + name + '/character-media', query)

    if responsemedia.status_code == 200:
        responsemedia = responsemedia.json()
        if 'assets' in responsemedia:
            responsemedia = responsemedia['assets']
            for media in responsemedia:
                if media['key'] == 'avatar':
                    avatar_path = media['value']
                    continue
                if media['key'] == 'main':
                    media_path = media['value']
                    continue
        else:
            avatar_path = responsemedia['avatar_url']
            media_path = responsemedia['render_url']

    return media_path, avatar_path

def get_soulbinds_conduits(character):

    query = { 'region': character.region.name, 'namespace': 'profile-' + character.region.name, 'locale': 'en_US' }
    responsesoulbinds = make_request('https://' + character.region.name + '.api.blizzard.com/profile/wow/character/' + character.realm.slug + '/' + character.name + '/soulbinds', query)

    if responsesoulbinds.status_code == 200:
        responsesoulbinds = responsesoulbinds.json()
        if 'soulbinds' in responsesoulbinds:
            for slbind in responsesoulbinds['soulbinds']:
                if 'is_active' in slbind:
                    soulbind = Soulbind.objects.get(sid=slbind['soulbind']['id'])
                    character.soulbind = soulbind
                    character.save()
                    if 'traits' in slbind:
                        character.soulbind_abilities.clear()
                        character.conduits.clear()
                        for sltrait in slbind['traits']:
                            if 'trait' in sltrait:
                                soulbind_ability = SoulbindTrait.objects.get(sid=sltrait['trait']['id'])
                                character.soulbind_abilities.add(soulbind_ability)
                            if 'conduit_socket' in sltrait:
                                if 'socket' in sltrait['conduit_socket']:
                                    if 'conduit' in sltrait['conduit_socket']['socket']:
                                        conduit = Conduit.objects.get(cid=sltrait['conduit_socket']['socket']['conduit']['id'])
                                        spellid = 0
                                        for ranks in conduit.ranks:
                                            if ranks['tier'] == sltrait['conduit_socket']['socket']['rank']:
                                                spellid = ranks['spell_tooltip']['spell']['id']
                                        cconduit = CharacterConduit(conduit=conduit, rank=sltrait['conduit_socket']['socket']['rank'], spell_id=spellid)
                                        cconduit.save()
                                        character.conduits.add(cconduit)

def get_alters(character):

    region = character.region
    logro = character.achievements.filter(achievement__is_account_wide=True).first()

    if hasattr(logro, 'achievement'):
        characters = Character.objects.filter(
            region=region,
            achievements__achievement=logro.achievement,
            achievements__date_completed=logro.date_completed
        ).exclude(id=character.id)

        for char in characters:
            print("Adding alter: " + character.name + " of " + char.name)
            character.alters.add(char)
            char.alters.add(character)

    else:
        characters = Character.objects.filter(
            region=region,
            achievement_points=character.achievement_points
        ).exclude(id=character.id)

        for char in characters:
            print("Adding alter: " + character.name + " of " + char.name)
            character.alters.add(char)
            char.alters.add(character)