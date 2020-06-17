from bs4 import BeautifulSoup
import requests
import csv

seasons = ['2020', '2019', '2018', '2017']
levels = ['ek', '1l', '2l', '3l', '4l', 'ol']


def hall_scores():
    for season in seasons:
        for level in levels:
            www = f"http://tlsp.pl/wynikihl/{season}/hlp/h{level}/"
            get_www = requests.get(www)
            source_www = get_www.content
            soup_www = BeautifulSoup(source_www, 'lxml')
            try:
                soup_www.find("div", class_="wiersz").contents[0]
                pass
            except:
                file_name = f"hall_{season}_{level}"
                with open(f"{file_name}.csv", "w", newline='') as file_with_results:
                    the_writer = csv.writer(file_with_results)
                    for result in soup_www.find_all("tr"):
                        if result.find("td", class_="wyn_wynik") is not None:
                            team_1 = result.find("td", class_="wyn_druzynad").find("a").contents[0]
                            team_2 = result.find("td", class_="wyn_druzynaw").find("a").contents[0]
                            try:
                                score_team_1 = result.find("td", class_="wyn_wynik").find("b").contents[0].split(':')[0].strip()
                                score_team_2 = result.find("td", class_="wyn_wynik").find("b").contents[0].split(':')[1].strip()
                            except:
                                pass
                            the_writer.writerow([team_1, team_2, score_team_1, score_team_2])




