import statsapi
from TeamInfo import TeamInfo
from ReportGen import create_report
import argparse


def get_teams_by_id():
    team_list = statsapi.lookup_team('')
    teams = {}
    for team in team_list:
        teams[team['id']] = (team['name'], team['fileCode'].upper())
    return teams


def get_teams_by_code():
    team_list = statsapi.lookup_team('')
    teams = {}
    for team in team_list:
        teams[team['fileCode']] = (team['name'], team['id'])
    return teams


def generate_report(teamid, month, year, teams, is_summary=True):
    team = TeamInfo(teamid, month, year, teams)
    if team.num_games > 0:
        create_report(team.get_results(), summary=is_summary)
    else:
        print("No games found.")


if __name__ == "__main__":
    team_ids = get_teams_by_id()
    team_codes = get_teams_by_code()
    valid_team_codes = team_codes.keys()

    parser = argparse.ArgumentParser(description='Example call: main.py PHI 06 2023')
    parser.add_argument('team_code', choices=valid_team_codes, type=str.lower)
    parser.add_argument('month', choices=range(1, 13), type=int)
    parser.add_argument('year', type=int)
    parser.add_argument('-s', '--summary', action='store_true')
    args = parser.parse_args()

    teamid = None
    month = None
    year = None
    summary = False
    if args.team_code:
        teamid = team_codes[args.team_code][1]
    if args.month:
        month = args.month
    if args.year:
        year = args.year
    if args.summary:
        summary = args.summary

    if teamid is not None and month is not None and year is not None:
        try:
            generate_report(teamid, month, year, team_ids, is_summary=summary)
        except Exception as e:
            print(e)
