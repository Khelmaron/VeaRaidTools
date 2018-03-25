import requests

 # Konfigurationsvariablen für die benötigten APIS => später auslagern
API_key_Blizzard = 'xgj9ybddvfx8e83fd3mwrrkbnq9a63gc'
guild = 'Veritas et Aequitas'
Realm = 'destromath'
API_key_warcraftlogs = "78b8cabdd100caf3d3d86003cd02807a"

class Guildmemberhandler:

    def get_guildmembers(APIKey, guild, Realm):
        members = requests.get("https://eu.api.battle.net/wow/guild/{}/{}?fields=members&locale=en_GB&apikey={}".format(Realm, guild, APIKey))
        return members.json()['members']

    def return_guildmembers():
        result = []
        for member in Guildmemberhandler.get_guildmembers(API_key_Blizzard, guild, Realm):
            data = { 'name' : member['character']['name'],
                        'rank' : member['rank']}
            result.append(data)
        return result

class RaidlogInterface:

    def get_reports(guild, Realm, API_key):
        return requests.get("https://www.warcraftlogs.com:443/v1/reports/guild/{}/{}/EU?api_key={}".format(guild, Realm, API_key)).json()

    def get_latest_report_ids(time=None):
        if not time: time = 0
        data = RaidlogInterface.get_reports(guild, Realm, API_key_warcraftlogs)
        return data

    def get_report_data(reportID):
        return requests.get("https://www.warcraftlogs.com:443/v1/report/fights/{}?api_key={}"
                            .format(reportID, API_key_warcraftlogs)).json()

    def get_participants(reportID):
        warcraftlog_fight_info = RaidlogInterface.get_report_data(reportID)
        participants = []
        for part in warcraftlog_fight_info['friendlies']:
            if part['type'] not in ('NPC', 'Pet','Boss'):
                participants.append(part["name"])
        return participants

    def get_report_object(warcraftlog_fight_info):
        return (Int(warcraftlog_fight_info['end']),get_participants(warcraftlog_fight_info))
##        latest_reports = []
##        for report in data:
##        if report['end'] > time:
##            latest_reports.append(report['id'])

##        return latest_reports
