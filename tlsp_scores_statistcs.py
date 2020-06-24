import numpy as np
import pandas as pd

scores_tlsp = pd.read_csv('pitch_scores.csv')


def rename_team_names(data):
    new_team_names = ['SZWEJK / ENCANTO SALON WNĘTRZ', 'TORMAL', 'CARTED BYDGOSKIE PRZEDMIEŚCIE', 'CZTEROKROPEK / PAN KARP', 'JS POWER-POL', 'LIDER SERWIS RUBINKOWO CENTRUM', 'NIEDŹWIEDZIE', 'SALON OBUWNICZY NADIA' ]
    old_team_names = ['SZWEJK', 'BUDLEX', 'BYDGOSKIE PRZEDMIEŚCIE', 'CZTEROKROPEK', 'REITER SOFA4YOU.COM', 'RUBINKOWO CENTRUM', 'NIEDŹWIEDZIE TORUŃ', 'SALON OBUWNICZY NADIA MZK']
    data_with_merged_names = data.copy()
    for i in range(len(new_team_names)):
        data_with_merged_names = data_with_merged_names.replace(to_replace=old_team_names[i], value=new_team_names[i])
    return data_with_merged_names


data_with_correct_team_names = rename_team_names(scores_tlsp)
print(data_with_correct_team_names)

