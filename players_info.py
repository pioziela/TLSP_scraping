from bs4 import BeautifulSoup
import requests
import csv


def players():
    player_id = 1
    player_exist = True
    # usunac player_id < 20
    while player_exist is True and player_id < 20:
        www = f"http://tlsp.pl/zawodnik/{player_id}/"
        get_www = requests.get(www)
        source_www = get_www.content
        soup_www = BeautifulSoup(source_www, 'lxml')
        player_name = soup_www.find("tr").find("b").contents[0]
        file_name = f"player_{player_id}_{player_name.strip()}"
        with open(f"TLSP_players/{file_name}.csv", "w", newline='') as file_with_player_info:
                    the_writer = csv.writer(file_with_player_info)
                    for player in soup_www.find_all("tr"):
                        if player.find("td", class_="zaw_zawody") is not None and player.find("td", class_="zaw_zawody").find("a") is not None:
                            for info in player:
                                print(info.a)


                            """
                            season = player.find("td", class_="zaw_zawody").find("a").contents[0]
                            team = player.find("td", class_="zaw_druzyna").find("a").contents[0]
                            position = player.find("td", class_="zaw_pozycja").contents[0]
                            metches = player.find("td").contents[0]
                            goals = player.find("td").contents[0]
                            yellow_cards = player.find("td").contents[0]
                            red_cards = player.find("td").contents[0]
                            """
                            #the_writer.writerow([season, team, position, metches, goals, yellow_cards, red_cards])




