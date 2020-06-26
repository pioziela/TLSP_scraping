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
                                                'Goals for/match', 'Goals against/match', 'The longest series of wins',
                                                'The longest series without lost', 'The longest series of losts',
                                                'The longest series without win'])
    for team in teams:
        all_team_matches = data.loc[(data['Team 1'] == team) | (data['Team 2'] == team)]
        matches = number_one_team_matches(all_team_matches)
        wins = one_team_wins(all_team_matches, team)
        losts = one_team_losts(all_team_matches, team)
        draws = one_team_draws(all_team_matches)
        win_percentage, lost_percentage, draw_percentage = matches_percentage(matches, wins, losts, draws)
        points = wins * 3 + draws
        goals_for, goals_against = goals_for_against(all_team_matches, team)
        goals_difference = goals_for - goals_against
        points_per_match, goals_for_per_match, goals_against_per_match = per_match(matches, points, goals_for, goals_against)
        the_longest_win_series, the_longest_lost_series, the_longest_series_without_lost, the_longest_series_without_win = the_longest_series(all_team_matches, team)
        all_team_statistics_2 = pd.DataFrame([[team, matches, points, round(points_per_match,2), wins, draws, losts,
                                            round(win_percentage,0), round(draw_percentage,0), round(lost_percentage,0),
                                             goals_for, goals_against, goals_difference, round(goals_for_per_match,2),
                                            round(goals_against_per_match,2), the_longest_win_series,
                                               the_longest_series_without_lost, the_longest_lost_series,
                                               the_longest_series_without_win]],
                                           columns=['Team', 'Matches', 'Points', 'Points/match', 'Wins',
                                                        'Draws', 'Losts', 'Wins %', 'Draws %', 'Losts %',
                                                        'Goals for', 'Goals against', 'Goals difference',
                                                        'Goals for/match', 'Goals against/match',
                                                    'The longest series of wins', 'The longest series without lost',
                                                    'The longest series of losts', 'The longest series without win'])
        all_team_statistics = all_team_statistics.append(all_team_statistics_2, ignore_index=True)
    return all_team_statistics


def number_one_team_matches(team_matches):
    matches = len(team_matches)
    return matches


def one_team_wins(team_matches, club):
    win1 = team_matches.loc[team_matches['Team 1 goals'] > team_matches['Team 2 goals']].loc[team_matches['Team 1'] == club]
    win2 = team_matches.loc[team_matches['Team 2 goals'] > team_matches['Team 1 goals']].loc[team_matches['Team 2'] == club]
    wins = len(pd.concat([win1, win2]))
    return wins


def one_team_losts(team_matches, club):
    lost1 = team_matches.loc[team_matches['Team 1 goals'] < team_matches['Team 2 goals']].loc[team_matches['Team 1'] == club]
    lost2 = team_matches.loc[team_matches['Team 2 goals'] < team_matches['Team 1 goals']].loc[team_matches['Team 2'] == club]
    losts = len(pd.concat([lost1, lost2]))
    return losts


def one_team_draws(team_matches):
    draws = len(team_matches.loc[team_matches['Team 1 goals'] == team_matches['Team 2 goals']])
    return draws


def matches_percentage(matches, wins, losts, draws):
    wins_per = wins / matches * 100
    losts_per = losts / matches * 100
    draws_per = draws / matches * 100
    return wins_per, losts_per, draws_per


def goals_for_against(team_matches, club):
    goals_for = team_matches.loc[team_matches['Team 1'] == club, 'Team 1 goals'].sum() + \
                team_matches.loc[team_matches['Team 2'] == club, 'Team 2 goals'].sum()
    goals_against = team_matches.loc[team_matches['Team 1'] == club, 'Team 2 goals'].sum() + \
                team_matches.loc[team_matches['Team 2'] == club, 'Team 1 goals'].sum()
    return goals_for, goals_against


def per_match(matches, points, goals_for, goals_against):
    points_per_match = points / matches
    goals_for_per_match = goals_for / matches
    goals_against_per_match = goals_against / matches
    return points_per_match, goals_for_per_match, goals_against_per_match


def the_longest_series(team_matches, club):
    win_series, the_longest_win_series, lost_series, the_longest_lost_series = 0, 0, 0, 0
    series_without_lost, the_longest_series_without_lost, series_without_win, the_longest_series_without_win = 0, 0, 0, 0
    for index, row in team_matches.iterrows():
        if (row['Team 1'] == club and row['Team 1 goals'] > row['Team 2 goals']) or (
                row['Team 2'] == club and row['Team 2 goals'] > row['Team 1 goals']):
            win_series += 1
        else:
            if win_series > the_longest_win_series:
                the_longest_win_series = win_series
            win_series = 0
        if (row['Team 1'] == club and row['Team 1 goals'] >= row['Team 2 goals']) or (
                row['Team 2'] == club and row['Team 2 goals'] >= row['Team 1 goals']):
            series_without_lost += 1
        else:
            if series_without_lost > the_longest_series_without_lost:
                the_longest_series_without_lost = series_without_lost
            series_without_lost = 0
        if (row['Team 1'] == club and row['Team 1 goals'] < row['Team 2 goals']) or (
                row['Team 2'] == club and row['Team 2 goals'] < row['Team 1 goals']):
            lost_series += 1
        else:
            if lost_series > the_longest_lost_series:
                the_longest_lost_series = lost_series
            lost_series = 0
        if (row['Team 1'] == club and row['Team 1 goals'] <= row['Team 2 goals']) or (
                row['Team 2'] == club and row['Team 2 goals'] <= row['Team 1 goals']):
            series_without_win += 1
        else:
            if series_without_win > the_longest_series_without_win:
                the_longest_series_without_win = series_without_win
            series_without_win = 0
    if win_series > the_longest_win_series:
        the_longest_win_series = win_series
    if lost_series > the_longest_lost_series:
        the_longest_lost_series = lost_series
    if series_without_lost > the_longest_series_without_lost:
        the_longest_series_without_lost = series_without_lost
    if series_without_win > the_longest_series_without_win:
        the_longest_series_without_win = series_without_win
    return the_longest_win_series, the_longest_lost_series, the_longest_series_without_lost, the_longest_series_without_win


print(team_statistics(data_with_correct_team_names))

team_statistics(data_with_correct_team_names).to_csv(f"{pitch_or_hall}_tlsp_statistics.csv")


def general_statistics(data):
    data = unique_score(data)
    data = the_same_teams(data)
    most_common_result = data.groupby('Unique score').count()[['Number of occurrences']]
    sorted_most_common_result = most_common_result.sort_values(by='Number of occurrences', ascending=False)
    most_often_played = data.groupby('Teams in alphabetical order').count()[['The most often played']]
    sorted_most_often_played = most_often_played.sort_values(by='The most often played', ascending=False)
    return sorted_most_often_played, sorted_most_common_result


def unique_score(data_with_teams_matches):
    data_to_unique_score = []
    for index, row in data_with_teams_matches.iterrows():
        if row['Team 1 goals'] > row['Team 2 goals']:
            data_to_unique_score.append(f"{row['Team 1 goals']}:{row['Team 2 goals']}")
        elif row['Team 1 goals'] < row['Team 2 goals']:
            data_to_unique_score.append(f"{row['Team 2 goals']}:{row['Team 1 goals']}")
        elif row['Team 1 goals'] == row['Team 2 goals']:
            data_to_unique_score.append(f"{row['Team 1 goals']}:{row['Team 2 goals']}")
    data_with_teams_matches['Unique score'] = data_to_unique_score
    number_of_result = ['_' for i in range(len(data_with_teams_matches))]
    data_with_teams_matches['Number of occurrences'] = number_of_result
    return data_with_teams_matches


def the_same_teams(data_with_team_matches):
    data_to_the_same_teams_matches = []
    for index, row in data_with_team_matches.iterrows():
        sorted_two_teams_list = sorted([row['Team 1'], row['Team 2']])
        data_to_the_same_teams_matches.append(f"{sorted_two_teams_list[0]} vs {sorted_two_teams_list[1]}")
    data_with_team_matches['Teams in alphabetical order'] = data_to_the_same_teams_matches
    the_same_team = ['_' for i in range(len(data_with_team_matches))]
    data_with_team_matches['The most often played'] = the_same_team
    return data_with_team_matches


often_played, common_result = general_statistics(data_with_correct_team_names)

print(often_played)
print(common_result)
