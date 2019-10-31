import time
from urllib.request import urlopen

from bs4 import BeautifulSoup

from models import Match, Jornada, League

base_url = "http://www.resultados-futbol.com/primera{}/grupo1/calendario"


def get_match(tr):
    stadium = tr.find('span', attrs={'class': 'location'}).text.strip()
    date_td = tr.td
    teamA_td = date_td.find_next_sibling()
    score_td = teamA_td.find_next_sibling()
    teamB_td = score_td.find_next_sibling()

    date = date_td.text.strip()
    team_A = teamA_td.a.text.strip()
    team_B = teamB_td.a.text.strip()
    score = score_td.a.text
    if score.find('-') == -1:
        raise Exception("Symbol '-' not found!")
    score_team_A = score.split('-')[0].strip()
    score_team_B = score.split('-')[1].strip()

    return Match(date, stadium, team_A, team_B, score_team_A, score_team_B)


def get_jornada(caja):
    matches = []
    id = caja.find('span', attrs={'class': 'titlebox'}).text.split()[-1]
    trs = caja.tbody.find_all('tr')
    # trs = trs[:1]
    for tr in trs:
        matches.append(get_match(tr))
    return Jornada(id, matches)


def league_to_csv(league, filename='dataset'):
    f = open(filename + '.csv', "r+", encoding="utf8")
    if len(f.readline()) == 0:
        print(
            "year,jornada,date,stadium,teamA,teamB,scoreTeamA,scoreTeamB,winner,winnerAsNumeric",
            file=f)
    for jornada in league.jornadas:
        for match in jornada.matches:
            print(
                "{},{},{},{},{},{},{},{},{},{}".format(league.year, jornada.id,
                                                       match.date,
                                                       match.stadium,
                                                       match.team_A,
                                                       match.team_B,
                                                       match.score_team_A,
                                                       match.score_team_B,
                                                       match.get_winner(),
                                                       match.get_winner_as_numeric()),
                file=f)


def handle_jornada(year):
    jornadas = []
    url = base_url.format(year)
    print("Using url:", url)
    page = urlopen(url)
    soup = BeautifulSoup(page.read(), "html.parser")
    try:
        contenedor_jornadas = soup.find('div',
                                        attrs={'class': 'b2col-container'})
        cajas = contenedor_jornadas.find_all('div',
                                             attrs={'class': 'boxhome-2col'})
        # cajas = cajas[:1]
        for caja in cajas:
            try:
                jornadas.append(get_jornada(caja))
            except Exception:
                print("Exception")
                break
    except Exception:
        print(
            soup.find('div', attrs={'class': 'ld-infohistorical'}).text.strip())
    return jornadas


def main():
    for i in range(1929, 1936):
        print("Getting year", i)
        league = League(i, handle_jornada(i))
        league_to_csv(league)
        time.sleep(5)


if __name__ == '__main__':
    main()
