from fpdf import FPDF
from TeamInfo import TeamInfo


def create_report(team_data, summary=True):
    pdf = ReportGen()

    # Summary Page
    pdf.add_page()
    pdf.set_font('Times', 'B', 20)
    title = f"{team_data['teamName']}: Snapshot of {team_data['month']:02}/{team_data['year']}"
    pdf.cell(w=0, h=12, txt=title, ln=1, align='C')

    ## Record + Run Differential
    pdf.set_font('Times', 'I', 16)
    pdf.cell(w=0, h=5, txt=f"Record: {team_data['record'][0]}W-{team_data['record'][1]}L", ln=1, align='C')
    pdf.cell(w=0, h=5, txt=f"Runs for/against: {team_data['run_differential'][0]}-{team_data['run_differential'][1]}", ln=1, align='C')

    ## Game Results
    pdf.set_font('Times', '', 14)
    pdf.cell(w=0, h=10, txt="Game Results", ln=1, align='L')
    ### Table Header
    features = ['game_date', 'away_team', 'home_team', 'away_score', 'home_score', 'result']
    feature_titles = ['Game Date', 'Away Team', 'Home Team', 'Away Score', 'Home Score', 'Result']
    ch = 6
    pdf.set_font('Arial', 'B', 12)
    for feature in feature_titles:
        if feature == feature_titles[-1]:
            pdf.cell(30, ch, feature, 1, 1, 'C')
        else:
            pdf.cell(30, ch, feature, 1, 0, 'C')

    ### Table Contents
    pdf.set_font('Times', '', 12)
    game_results = team_data['games']
    for i in range(len(game_results)):
        for j in range(len(features)):
            if j == len(features) - 1:
                pdf.cell(30, ch, str(game_results[i][features[j]]), 1, 1, 'C')
            else:
                pdf.cell(30, ch, str(game_results[i][features[j]]), 1, 0, 'C')

    ## Standings
    pdf.set_font('Times', '', 14)
    standings = team_data['standings']
    div_name = standings['div_name']
    pdf.ln()
    pdf.cell(w=0, h=10, txt=f"{div_name} Standings (As of {team_data['end_date']})", ln=1, align='L')

    ### Table Header
    team_standings = standings['teams']
    standing_features = ['div_rank', 'wc_rank', 'name', 'w', 'l', 'gb', 'wc_gb']
    standing_feature_titles = ['Rank', 'WC Rank', 'Name', 'W', 'L', 'GB', 'WC GB']
    ch = 6
    pdf.set_font('Times', 'B', 12)
    for feature in standing_feature_titles:
        if feature == standing_feature_titles[-1]:
            pdf.cell(20, ch, feature, 1, 1, 'C')
        elif feature == standing_feature_titles[2]:
            pdf.cell(60, ch, feature, 1, 0, 'C')
        else:
            pdf.cell(20, ch, feature, 1, 0, 'C')

    ### Table Contents
    pdf.set_font('Times', '', 12)
    for i in range(len(team_standings)):
        for j in range(len(standing_features)):
            if j == len(standing_features) - 1:
                pdf.cell(20, ch, str(team_standings[i][standing_features[j]]), 1, 1, 'C')
            elif j == 2:
                pdf.cell(60, ch, str(team_standings[i][standing_features[j]]), 1, 0, 'C')
            else:
                pdf.cell(20, ch, str(team_standings[i][standing_features[j]]), 1, 0, 'C')

    ## Batting Stats
    pdf.add_page()
    stats_eod = team_data['player_stats_eod']

    pdf.set_font('Times', '', 14)
    pdf.ln()
    pdf.cell(w=0, h=10, txt=f"Player Batting Stats (As of {team_data['end_date']})", ln=1, align='L')

    ### Table Header
    batting_features = ['name', 'atBats', 'baseOnBalls', 'strikeOuts', 'hits', 'doubles', 'triples', 'homeRuns', 'runs', 'rbi', 'stolenBases', 'avg', 'obp', 'slg', 'ops']
    batting_features_titles = ['Name', 'AB', 'BB', 'SO', 'H', '2B', '3B', 'HR', 'R', 'RBI', 'SB', 'AVG', 'OBP', 'SLG', 'OPS']
    ch = 6
    pdf.set_font('Times', 'B', 10)
    for feature in batting_features_titles:
        if feature == batting_features_titles[-1]:
            pdf.cell(10, ch, feature, 1, 1, 'C')
        elif feature == batting_features_titles[0]:
            pdf.cell(50, ch, feature, 1, 0, 'C')
        else:
            pdf.cell(10, ch, feature, 1, 0, 'C')

    ### Table Contents
    pdf.set_font('Times', '', 10)
    for player in stats_eod:
        if player['season_batting'] != '':
            for j in range(len(batting_features)):
                if j == len(player['season_batting']) - 1:
                    pdf.cell(10, ch, str(player['season_batting'][batting_features[j]]), 1, 1, 'C')
                elif j == 0:
                        pdf.cell(50, ch, str(player['name']), 1, 0, 'L')
                else:
                    pdf.cell(10, ch, str(player['season_batting'][batting_features[j]]), 1, 0, 'C')

    ## Pitching Stats
    pdf.add_page()
    pdf.set_font('Times', '', 14)
    pdf.ln()
    pdf.cell(w=0, h=10, txt=f"Player Pitching Stats (As of {team_data['end_date']})", ln=1, align='L')

    ### Table Header
    pitching_features = ['name', 'inningsPitched', 'wins', 'losses', 'atBats', 'baseOnBalls', 'strikeOuts', 'hits', 'doubles', 'triples', 'homeRuns', 'runs', 'earnedRuns', 'stolenBases', 'era', 'obp', 'blownSaves', 'numberOfPitches']
    pitching_features_titles = ['Name', 'IP', 'W', 'L', 'AB', 'BB', 'SO', 'H', '2B', '3B', 'HR', 'R', 'ER', 'SB', 'ERA', 'OBP', 'BS', 'NP']
    ch = 6
    pdf.set_font('Times', 'B', 10)
    for feature in pitching_features_titles:
        if feature == pitching_features_titles[-1]:
            pdf.cell(10, ch, feature, 1, 1, 'C')
        elif feature == pitching_features_titles[0]:
            pdf.cell(25, ch, feature, 1, 0, 'C')
        else:
            pdf.cell(10, ch, feature, 1, 0, 'C')

    ### Table Contents
    pdf.set_font('Times', '', 8)
    for player in stats_eod:
        if player['season_pitching'] != '':
            for j in range(len(pitching_features)):
                if j == len(pitching_features) - 1:
                    pdf.cell(10, ch, str(player['season_pitching'][pitching_features[j]]), 1, 1, 'C')
                elif j == 0:
                        pdf.cell(25, ch, str(player['name']), 1, 0, 'L')
                else:
                    pdf.cell(10, ch, str(player['season_pitching'][pitching_features[j]]), 1, 0, 'C')

    pdf.output(f"./{team_data['teamCode']}-{team_data['month']:02}-{team_data['year']}.pdf", 'F')

class ReportGen(FPDF):
    def __init__(self):
        super().__init__()

    # def header(self):
    #     self.set_font('Arial', '', 12)
    #     self.cell(0, 8, 'Header', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', '', 12)
        if self.page_no() in [1, 2, 3]:
            self.cell(0, 8, f'Summary', 0, 0, 'C')
        else:
            self.cell(0, 8, f'Page {self.page_no()}', 0, 0, 'C')
