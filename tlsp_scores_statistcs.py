import numpy as np
import pandas as pd
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', 500)
pitch_or_hall = input('pitch or hall?')
scores_tlsp = pd.read_csv(f"{pitch_or_hall}_scores.csv")


def rename_team_names(data):
    new_team_names = ['SZWEJK / ENCANTO SALON WNĘTRZ', 'BUDLEX', 'CARTED BYDGOSKIE PRZEDMIEŚCIE', 'CZTEROKROPEK / PAN KARP', 'JS POWER-POL', 'LIDER SERWIS RUBINKOWO CENTRUM', 'NIEDŹWIEDZIE', 'SALON OBUWNICZY NADIA', 'DEMTECH', 'BELLA LINE FUNDACJA ŚWIATŁO', 'HITOR']
    old_team_names = ['SZWEJK', 'TORMAL', 'BYDGOSKIE PRZEDMIEŚCIE', 'CZTEROKROPEK', 'REITER SOFA4YOU.COM', 'RUBINKOWO CENTRUM', 'NIEDŹWIEDZIE TORUŃ', 'SALON OBUWNICZY NADIA MZK', 'OPONEO.PL', 'FUNDACJA ŚWIATŁO FLAMHED', 'HITOR2 / NIEDŹWIEDZIE TORUŃ']
    data_with_merged_names = data[data.Season.str.contains('ol') == False].copy()
    for i in range(len(new_team_names)):
        data_with_merged_names = data_with_merged_names.replace(to_replace=old_team_names[i], value=new_team_names[i])
    return data_with_merged_names


data_with_correct_team_names = rename_team_names(scores_tlsp)


def team_statistics(data):
    teams = sorted(set(list(data['Team 1']) + list(data['Team 2'])))
    all_team_statistics = pd.DataFrame([],
                                       columns=['Team', 'Matches', 'Points', 'Points/match', 'Wins',
                                                'Draws', 'Losts', 'Wins %', 'Draws %', 'Losts %',
                                                'Goals for', 'Goals against', 'Goals difference',
                                                'Goals for/match', 'Goals against/match'])
    for team in teams:
        all_team_matches = data.loc[(data['Team 1'] == team) | (data['Team 2'] == team)]
        matches = len(all_team_matches)
        win1, win2 = all_team_matches.loc[all_team_matches['Team 1 goals'] > all_team_matches['Team 2 goals']].loc[all_team_matches['Team 1'] == team], \
                     all_team_matches.loc[all_team_matches['Team 2 goals'] > all_team_matches['Team 1 goals']].loc[all_team_matches['Team 2'] == team]
        wins = len(pd.concat([win1, win2]))
        win_percentage = (wins / matches) * 100
        lost1, lost2 = all_team_matches.loc[all_team_matches['Team 1 goals'] < all_team_matches['Team 2 goals']].loc[all_team_matches['Team 1'] == team], \
                     all_team_matches.loc[all_team_matches['Team 2 goals'] < all_team_matches['Team 1 goals']].loc[all_team_matches['Team 2'] == team]
        losts = len(pd.concat([lost1, lost2]))
        lost_percentage = (losts / matches) * 100
        draws = len(all_team_matches.loc[all_team_matches['Team 1 goals'] == all_team_matches['Team 2 goals']])
        draw_percentage = (draws / matches) * 100
        points = wins * 3 + draws
        points_per_match = points / matches
        goals_for = all_team_matches.loc[all_team_matches['Team 1'] == team, 'Team 1 goals'].sum() + \
                    all_team_matches.loc[all_team_matches['Team 2'] == team, 'Team 2 goals'].sum()
        goals_for_per_match = goals_for / matches
        goals_against = all_team_matches.loc[all_team_matches['Team 1'] == team, 'Team 2 goals'].sum() + \
                    all_team_matches.loc[all_team_matches['Team 2'] == team, 'Team 1 goals'].sum()
        goals_against_per_match = goals_against / matches
        goals_difference = goals_for - goals_against
        all_team_statistics_2 = pd.DataFrame([[team, matches, points, round(points_per_match,2), wins, draws, losts,
                                            round(win_percentage,0), round(draw_percentage,0), round(lost_percentage,0),
                                             goals_for, goals_against, goals_difference, round(goals_for_per_match,2),
                                            round(goals_against_per_match,2)]],
                                           columns=['Team', 'Matches', 'Points', 'Points/match', 'Wins',
                                                        'Draws', 'Losts', 'Wins %', 'Draws %', 'Losts %',
                                                        'Goals for', 'Goals against', 'Goals difference',
                                                        'Goals for/match', 'Goals against/match'])
        all_team_statistics = all_team_statistics.append(all_team_statistics_2, ignore_index=True)
    return all_team_statistics


print(team_statistics(data_with_correct_team_names))

team_statistics(data_with_correct_team_names).to_csv(f"{pitch_or_hall}_tlsp_statistics.csv")