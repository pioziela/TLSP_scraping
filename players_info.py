from bs4 import BeautifulSoup
import requests
import csv


def players():
    file_name = f"players_TLSP_v2"
    with open(f"{file_name}.csv", "w", newline='') as file_with_player_info:
        the_writer = csv.writer(file_with_player_info)
        player_id = 1
        while player_id < 2500:
            www = f"http://tlsp.pl/zawodnik/{player_id}/"
            get_www = requests.get(www)
            source_www = get_www.content
            soup_www = BeautifulSoup(source_www, 'lxml')
            if soup_www.find("div", class_="wiersz") is not None:
                player_id += 1
                continue
            player_name = soup_www.find("tr").find("b").contents[0]
            the_writer.writerow([player_name])
            for tr in soup_www.find_all("tr"):
                if tr.find("td", class_="zaw_pozycja") is None:
                    continue
                if tr.find("td", class_="zaw_pozycja").contents[0] == 'Pozycja':
                    continue
                if len(tr.find("td", class_="zaw_pozycja").contents[0]) < 2:
                    continue
                player_season_info = []
                for td in tr.find_all("td"):
                    player_season_info.append(td)
                player_season = player_season_info[0].find("a").contents[0]
                if len(player_season_info[1].find("a").contents) == 0:
                    player_team = 'unknown'
                else:
                    player_team = player_season_info[1].find("a").contents[0]
                player_position = player_season_info[2].contents[0]
                player_matches = player_season_info[3].contents[0]
                player_goals = player_season_info[4].contents[0]
                player_yellow_cards = player_season_info[5].contents[0]
                player_red_cards = player_season_info[6].contents[0]
                the_writer.writerow([player_season, player_team, player_position, player_matches,
                                    player_goals, player_yellow_cards, player_red_cards])
            player_id += 1
            print(player_id)
