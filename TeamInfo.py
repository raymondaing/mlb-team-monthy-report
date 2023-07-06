import statsapi
import pandas as pd
import numpy
import calendar
import fpdf
import re
from collections import  defaultdict


class TeamInfo:
    def __init__(self, teamid_, month_, year_):
        self.teams = self.__get_teams_info()
        self.teamid = teamid_
        self.teamname = self.teams[teamid_][0]
        self.teamcode = self.teams[teamid_][1]
        self.month = month_
        self.year = year_
        self.date_range = calendar.monthrange(year_, month_)
        self.schedule = statsapi.schedule(start_date=f'{self.month}/{self.date_range[0]:02}/{self.year}',
                                          end_date=f'{self.month}/{self.date_range[1]:02}/{self.year}', team=self.teamid)
        self.roster = self.__get_roster()
        self.game_results = self.__get_game_results()
        self.player_stats = self.__get_current_month_player_stats()

    def __get_number_games(self):
        return len(self.schedule)

    def __get_teams_info(self):
        team_list = statsapi.lookup_team('')
        teams = {}
        for team in team_list:
            teams[team['id']] = (team['name'], team['fileCode'].upper())
        return teams

    def __get_game_results(self):
        df = pd.DataFrame.from_dict(self.schedule)[['game_date', 'away_id', 'home_id', 'away_score', 'home_score', 'winning_team']]
        df['Result'] = df.apply(lambda x: "W" if x['winning_team'] == self.teamname else "L", axis=1)
        df = df.drop(['winning_team'], axis=1)
        df['away_id'] = df.apply(lambda x: self.teams[int(x['away_id'])][1], axis=1)
        df['home_id'] = df.apply(lambda x: self.teams[int(x['home_id'])][1], axis=1)
        df.rename(columns={'away_id': 'Away Team', 'home_id': "Home Team"})
        return df.to_dict('index')

    def __get_roster(self):
        roster = statsapi.roster(self.teamid).split('\n')
        clean_roster = [x for x in list(map(self.__name_split, roster)) if x != 'NA']
        return clean_roster

    def __get_current_month_player_stats(self):
        player_stats = []
        game_ids = [game['game_id'] for game in self.schedule]
        # Season stats by end of the month (last game of the month)
        game_box = statsapi.boxscore_data(game_ids[-1])
        if game_box['teamInfo']['home']['id'] == self.teamid:
            team_data = game_box['home']
        else:
            team_data = game_box['away']
        pitchers = team_data['pitchers'] + team_data['bullpen']
        batters = team_data['batters'] + team_data['bench']
        for info in team_data['players'].values():
            pid = info['person']['id']
            name = info['person']['fullName']
            data = {
                'id': pid,
                'name': name,
                'season_batting': "",
                'season_pitching': ""
            }

            if pid in pitchers:
                is_pitcher = True
            else:
                is_pitcher = False

            if pid in batters:
                is_batter = True
            else:
                is_batter = False

            if is_batter:
                data['season_batting'] = info['seasonStats']['batting']
            if is_pitcher:
                data['season_pitching'] = info['seasonStats']['pitching']
            player_stats.append(data)
        return player_stats

    def __name_split(self, player_info):
        reg = re.match(r'(?P<number>#\d{1,2})\s+(?P<position>\w{1,2})\s*(?P<name>\S* \S*)', player_info)
        if reg:
            return reg['number'], reg['position'], reg['name']
        else:
            return 'NA'

    def get_results(self):
        info = {
            "teamid": self.teamid,
            "teamName": self.teamname,
            "teamCode": self.teamcode,
            "month": self.month,
            "year": self.year,
            "roster": self.roster,
            "games": self.game_results,
            "player_stats": self.player_stats
        }
        return info