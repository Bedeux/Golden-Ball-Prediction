import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_all_big_clubs_id():
    r = requests.get("https://fbref.com/fr/comps/Big5/")
    soup = BeautifulSoup(r.content, "html.parser")
    clubs = []
    clubs_div = soup.find("div", {"id": "div_big5_table"})
    for a_href in clubs_div.find_all("a", href=True):
        if '/fr/equipes/' in a_href["href"] :
            link = a_href["href"]
            club_id = link.split('/')[3]
            if club_id not in clubs: clubs.append(club_id)
    return clubs

def get_all_player_id_from_club(club_id):
    # print("https://fbref.com/fr/equipes/" + club_id)
    r = requests.get("https://fbref.com/fr/equipes/" + club_id)
    soup = BeautifulSoup(r.content, "html.parser")
    players = []
    players_div = soup.find("div", {"id": "all_stats_standard"})
    for a_href in players_div.find_all("a", href=True):
        if '/fr/joueurs/' in a_href["href"] and '/matchs/' not in a_href["href"]:
            link = a_href["href"]
            player_id = link.split('/')[3]+'/'+ link.split('/')[4]
            if player_id not in players:
                players.append(player_id)
    return players


def get_player_stat(player_id):
    r = requests.get("https://fbref.com/fr/joueurs/" + player_id)
    print("https://fbref.com/fr/joueurs/" + player_id)
    html_content = r.text

    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', {'id': 'stats_standard_dom_lg'})
    tbody = table.find('tbody')
    rows = tbody.find_all('tr')
    data = []
    columns = []  

    for row in rows:
        cols = row.find_all('td')
        if not columns:
            # Si les noms de colonnes ne sont pas déjà extraits, le faire à partir des en-têtes
            header = row.find('th')
            columns.append(header['data-stat'])
        # Récupérer les valeurs des <td> et leurs attributs data-stat
        values = [(col['data-stat'], col.text.strip()) for col in cols]
        data.append(values)
    print(data)


# print(get_all_player_id_from_club("Lens"))
test = get_all_big_clubs_id()
# print(test[3])
test_player = get_all_player_id_from_club(test[0])[0]

print(get_player_stat(test_player))
