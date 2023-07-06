import statsapi
import pandas as pd
import numpy
import calendar
import re


class TeamInfo:
    def __init__(self, teamid_, month_, year_, team_ids_):
        self.team_ids = team_ids_
        self.teamid = teamid_
        self.teamname = self.team_ids[teamid_][0]
        self.teamcode = self.team_ids[teamid_][1]
        self.month = month_
        self.year = year_
        self.end_day = calendar.monthrange(year_, month_)[1]
        self.schedule = statsapi.schedule(start_date=f'{self.month}/01/{self.year}',
                                          end_date=f'{self.month}/{self.end_day}/{self.year}', team=self.teamid)
        self.num_games = self.__get_number_games()

        self.roster = self.__get_roster()
        self.game_results = self.__get_game_results()
        self.record = self.__get_win_loss()
        self.run_differential = self.__get_run_differential()
        self.player_stats_to_date = self.__get_current_season_player_stats()
        self.standings = self.__get_standings()

    def __get_number_games(self):
        return len(self.schedule)

    def __get_game_results(self):
        if self.num_games > 0:
            df = pd.DataFrame.from_dict(self.schedule)[['game_date', 'away_id', 'home_id', 'away_score', 'home_score', 'winning_team']]
            df['result'] = df.apply(lambda x: "W" if x['winning_team'] == self.teamname else "L", axis=1)
            df = df.drop(['winning_team'], axis=1)
            df['away_id'] = df.apply(lambda x: self.team_ids[int(x['away_id'])][1], axis=1)
            df['home_id'] = df.apply(lambda x: self.team_ids[int(x['home_id'])][1], axis=1)
            df = df.rename(columns={'away_id': 'away_team', 'home_id': "home_team"})
            return df.to_dict('index')

    def __get_win_loss(self):
        if self.num_games > 0:
            w = 0
            l = 0
            for game in self.game_results.values():
                if game['result'] == 'W':
                    w += 1
                else:
                    l += 1
            return w, l

    def __get_run_differential(self):
        if self.num_games > 0:
            runs_for = 0
            runs_against = 0
            for game in self.game_results.values():
                if game['home_team'] == self.teamcode.upper():
                    runs_for += int(game['home_score'])
                    runs_against += int(game['away_score'])
                else:
                    runs_for += int(game['away_score'])
                    runs_against += int(game['home_score'])
            return runs_for, runs_against

    def __get_standings(self):
        if self.num_games > 0:
            standings = statsapi.standings_data(leagueId="103,104", division="all", include_wildcard=True, season=None,
                                                standingsTypes=None, date=f'{self.month}/{self.end_day}/{self.year}')
            for div in standings.values():
                for team in div['teams']:
                    if team['team_id'] == self.teamid:
                        return div

    def __get_roster(self):
        roster = statsapi.roster(self.teamid).split('\n')
        clean_roster = [x for x in list(map(self.__name_split, roster)) if x != 'NA']
        return clean_roster

    def __get_game_season_stats_for_players(self, game_box):
        if self.num_games > 0:
            player_stats = []
            if game_box['teamInfo']['home']['id'] == self.teamid:
                team_data = game_box['home']
            else:
                team_data = game_box['away']
            pitchers = team_data['pitchers'] + team_data['bullpen']
            batters = team_data['batters'] + team_data['bench']
            for info in team_data['players'].values():
                pid = info['person']['id']
                name = info['person']['fullName']
                position = list(info['position'].values())
                if 'allPositions' in info:
                    all_positions = [x['abbreviation'] for x in info['allPositions']]
                else:
                    all_positions = position
                data = {
                    'id': pid,
                    'name': name,
                    'current_position': position,
                    'all_positions': all_positions,
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

    def __get_current_season_player_stats(self):
        if self.num_games > 0:
            # Grabs the season stats for the players by the last game in the date range
            game_ids = [game['game_id'] for game in self.schedule]

            # Season stats by end of the month (last game of the month)
            game_box = statsapi.boxscore_data(game_ids[-1])
            player_stats = self.__get_game_season_stats_for_players(game_box)
            return player_stats

    def __get_all_season_player_stats(self):
        if self.num_games > 0:
            # Grabs the season stats for the players for each game in the date range
            game_ids = [game['game_id'] for game in self.schedule]
            game_stats = []
            for game_id in game_ids:
                game_box = statsapi.boxscore_data(game_id)
                player_stats = self.__get_game_season_stats_for_players(game_box)
                game_stats.append(player_stats)
            return game_stats

    def __name_split(self, player_info):
        reg = re.match(r'(?P<number>#\d{1,2})\s+(?P<position>\w{1,2})\s*(?P<name>\S* \S*)', player_info)
        if reg:
            return reg['number'], reg['position'], reg['name']
        else:
            return 'NA'

    def get_results(self):
        if self.num_games > 0:
            info = {
                "teamid": self.teamid,
                "teamName": self.teamname,
                "teamCode": self.teamcode,
                "month": self.month,
                "year": self.year,
                "start_date": f'{self.month}/01/{self.year}',
                "end_date": f'{self.month}/{self.end_day}/{self.year}',
                "roster": self.roster,
                "games": self.game_results,
                "record": self.record,
                "run_differential": self.run_differential,
                "player_stats": self.player_stats_to_date,
                "standings": self.standings
            }
            return info
        else:
            return None
