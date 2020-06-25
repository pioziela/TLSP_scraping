from bs4 import BeautifulSoup
import requests
import csv

seasons = ['2017', '2018', '2019', '2020']
levels = ['ek', '1l', '2l', '3l', '4l', 'ol']


def tlsp_scores(place):
    www_address_part_1 = 'lnb'
    www_address_part_2 = 'b'
    if place == 'hall':
        www_address_part_1 = 'hlp'
        www_address_part_2 = 'h'
    file_name = f"{place}_scores"
    with open(f"{file_name}.csv", "w", newline='') as file_with_results:
        the_writer = csv.writer(file_with_results)
        the_writer.writerow(["Season", "Team 1", "Team 2", "Team 1 goals", "Team 2 goals"])
        for season in seasons:
            for level in levels:
                www = f"http://tlsp.pl/wyniki/{season}/{www_address_part_1}/{www_address_part_2}{level}/"
                get_www = requests.get(www)
                source_www = get_www.content
                soup_www = BeautifulSoup(source_www, 'lxml')
                if soup_www.find("div", class_="wiersz") is not None:
                    continue
                for result in soup_www.find_all("tr"):
                    if result.find("td", class_="wyn_wynik") is None:
                        continue
                    team_1, team_2 = result.find("td", class_="wyn_druzynad").find("a").contents[0], result.find("td", class_="wyn_druzynaw").find("a").contents[0]
                    if result.find("td", class_="wyn_wynik").find("b") is None:
                        continue
                    score_team_1, score_team_2 = result.find("td", class_="wyn_wynik").find("b").contents[0].split(':')[0].strip(), result.find("td", class_="wyn_wynik").find("b").contents[0].split(':')[1].strip()
                    the_writer.writerow([f"{season}_{level}",team_1, team_2, score_team_1, score_team_2])






