import statsapi
import pandas
import numpy
import calendar
import fpdf
import re

# Get dates
class ReportGen:
    def __init__(self, team_, month_, year_):
        self.team = team_
        self.month = month_
        self.year = year_
        self.date_range = calendar.monthrange(year_, month_)
        self.schedule = statsapi.schedule(f'{self.month}/{self.date_range[0]:02}/{self.year}')

        self.roster = self.__get_roster()

    def __get_number_games_played(self):
        return len(statsapi.schedule(f'{self.month}/{self.date_range[0]:02}/{self.year}'))

    def __get_roster(self):
        roster = statsapi.roster(self.team).split('\n')
        clean_roster = [x for x in list(map(self.__name_split, roster)) if x != 'NA']
        return clean_roster

    def __name_split(player_info):
        reg = re.match(r'(?P<number>#\d{1,2})\s+(?P<position>\w{1,2})\s*(?P<name>\S* \S*)', player_info)
        if reg:
            return reg['number'], reg['position'], reg['name']
        else:
            return 'NA'

    def get_report(self):
        return
