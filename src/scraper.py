import argparse
import os
import sys
import time
import urllib
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import urlopen

from models import Match, Jornada, League

base_url = "http://www.resultados-futbol.com/primera{}/grupo1/calendario"


def handle_team_logo(team_name, link):
    path = '%s/%s.jpg' % (logos_folder_name, team_name)
    if not os.path.isfile(path):
        txt = open(path, "wb")
        download_img = urlopen(link)
        print(team_name, link)
        txt.write(download_img.read())
        txt.close()


def get_match(tr):
    stadium = tr.find('span', attrs={'class': 'location'}).text.strip()
    date_td = tr.td
    teamA_td = date_td.find_next_sibling()
    score_td = teamA_td.find_next_sibling()
    teamB_td = score_td.find_next_sibling()

    date = date_td.text.strip()
    team_A = teamA_td.a.text.strip()
    handle_team_logo(team_A, teamA_td.a.img['src'])
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


def league_to_csv(league):
    for jornada in league.jornadas:
        for match in jornada.matches:
            print(
                "{},{},{},{},{},{},{},{},{},{},{},{}".format(league.year,
                                                             jornada.id,
                                                             match.date,
                                                             match.stadium,
                                                             match.team_A,
                                                             match.logo_team_A,
                                                             match.team_B,
                                                             match.logo_team_B,
                                                             match.score_team_A,
                                                             match.score_team_B,
                                                             match.get_winner(),
                                                             match.get_winner_as_numeric()),
                file=f)


def handle_jornada(year):
    jornadas = []
    url = base_url.format(year)
    print("Using url:", url)

    # https://www.google.com/search?q=my+user+agent&oq=my+user+agent
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    req = urllib.request.Request(url, headers={'User-Agent': user_agent})
    try:
        page = urlopen(req)
    except:
        print('Something went wrong retrieving data')
        sys.exit(-1)

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


def check_logos_directory():
    if not os.path.isdir(logos_folder_name):
        os.makedirs(logos_folder_name)


def get_data():
    check_logos_directory()
    for i in range(1929, 2021):
        print("Getting year", i)
        league = League(i, handle_jornada(i))
        league_to_csv(league)
        time.sleep(5)


def selenium_example():
    # https://sites.google.com/a/chromium.org/chromedriver/downloads
    browser = webdriver.Chrome(executable_path=r"./chromedriver_78.exe")
    browser.get("http://www.resultados-futbol.com")
    browser.find_element_by_class_name("qc-cmp-button").click()
    browser.find_element_by_class_name("qc-cmp-secondary-button").click()
    browser.find_element_by_class_name("qc-cmp-save-and-exit").click()
    time.sleep(2)

    browser.find_element_by_id("login_a").click()
    browser.find_element_by_id("user_nameL").send_keys("scraper")
    browser.find_element_by_id("passwordL").send_keys("scraper")

    # https://stackoverflow.com/questions/8832858/using-python-bindings-selenium-webdriver-click-is-not-working-sometimes
    browser.find_element_by_id("iniciosesion").send_keys("\n")
    time.sleep(5)

    browser.find_element_by_id("swithSessWindow").click()
    browser.find_element_by_link_text('Ir a mi perfil').click()

    info = browser.find_element_by_id("info").text.split()
    username = info[0]
    print('Username', username)
    is_connected = info[1] == 'Conectado'
    print('Is Connected?', is_connected)

    points = browser.find_element_by_class_name("points").text
    print('Points', points)

    ncomments = browser.find_element_by_class_name("ncomments").text
    print('ncomments', ncomments)

    nfriends = browser.find_element_by_class_name("nfriends").text
    print('nfriends', nfriends)


def main():
    if args.selenium: selenium_example()
    if not args.no_data: get_data()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Web scraper to get data from a website.')

    parser.add_argument('--selenium', help='Launch Selenium example', action='store_true')
    parser.add_argument('--no_data', help='Get data with the scraper', action='store_true')
    args = parser.parse_args()

    logos_folder_name = 'logos'
    f = open('football_spanish_league.csv', "w", encoding="utf8")
    print(
        "year,jornada,date,stadium,teamA,logo_teamA,teamB,logo_teamB,scoreTeamA,scoreTeamB,winner,winnerAsNumeric",
        file=f)
    main()
    f.close()
