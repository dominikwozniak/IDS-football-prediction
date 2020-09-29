# Target: Fetch xG data from understat.com
# https://github.com/amosbastian/understat

import asyncio
import json
import aiohttp
from understat import Understat
import pandas as pd
import os

from xG_teams import *

DATA_PATH = os.path.join('..', 'data')
LAST_DATE_PATH = os.path.join('..', 'last_date.txt')
LIST_OF_TEAMS = [TEAMS_2015, TEAMS_2016, TEAMS_2017, TEAMS_2018, TEAMS_2019, TEAMS_2020]
YEARS = ['2015', '2016', '2017', '2018', '2019', '2020']
YEARS_FLAG = [2015, 2016, 2017, 2018, 2019, 2020]


def find_last_season(path: str) -> int:
    years = list(map(lambda x: x[-4:], os.listdir(path)))
    return int(max(years))


def save_last_date(file: str, date: str = '0001-01-01 00:00:00'):
    with open(file, 'w') as f:
        f.write(date)


def read_last_date(file: str) -> str:
    with open(file) as f:
        last_date = f.read()
    return last_date


async def main():
    last_season = YEARS_FLAG[0] - 1

    if not os.path.exists(LAST_DATE_PATH):
        save_last_date(LAST_DATE_PATH)
    last_date = read_last_date(LAST_DATE_PATH)
    last_date_downloaded = last_date

    if os.path.exists(DATA_PATH):
        last_season = find_last_season(DATA_PATH)
        os.chdir(DATA_PATH)
    else:
        os.chdir("..")
        os.mkdir("data")
        os.chdir("data")

    for index, teams in enumerate(LIST_OF_TEAMS):
        if last_season > YEARS_FLAG[index]:
            continue

        if not os.path.exists("season_" + YEARS[index]):
            print("Creating directory: season_" + YEARS[index])
            os.mkdir("season_" + YEARS[index])

        os.chdir("season_" + YEARS[index])
        print(f"Downloading season dataset ... [{index+1} of {len(LIST_OF_TEAMS)}]")

        for counter, team in enumerate(teams):
            print(f'Downloading match data ... [{counter+1} of {len(teams)}]')
            async with aiohttp.ClientSession() as session:
                understat = Understat(session)

                data = await understat.get_team_results(
                    team,
                    YEARS_FLAG[index],
                    side="h",
                )
                data_to_csv = data.copy()

                data2 = await understat.get_team_results(
                    team,
                    YEARS_FLAG[index],
                    side="a"
                )
                data_to_csv2 = data2.copy()

            dct = {}
            tab = []

            for match in data_to_csv:
                if match['datetime'] > last_date_downloaded:
                    dct[match['a']['title']] = match['xG']['h']
                    tab.append(match['xG']['a'])
                    if match['datetime'] > last_date:
                        last_date = match['datetime']
                else:
                    continue

            df = pd.DataFrame(dct.items(), columns=['away_team', 'xG_home'])
            df['home_team'] = team
            df['xG_away'] = tab
            df = df[['home_team', 'away_team', 'xG_home', 'xG_away']]

            if os.path.exists(f'{team}_{YEARS[index]}.csv'):
                df.to_csv(f'{team}_{YEARS[index]}.csv', mode='a', header=False)
            else:
                df.to_csv(f'{team}_{YEARS[index]}.csv')

        os.chdir("..")

    save_last_date(LAST_DATE_PATH, last_date)
    print("Dataset downloaded successfully")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())