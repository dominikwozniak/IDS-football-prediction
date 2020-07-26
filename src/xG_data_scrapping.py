# Target: Fetch xG data from understat.com
# https://github.com/amosbastian/understat

import asyncio
import json
import aiohttp
from understat import Understat
import pandas as pd
import os
import shutil

from xG_teams import *


async def main():
    LIST_OF_TEAMS = [TEAMS_2015, TEAMS_2016, TEAMS_2017, TEAMS_2018, TEAMS_2019]
    YEARS = ['2015', '2016', '2017', '2018', '2019']
    YEARS_FLAG = [2015, 2016, 2017, 2018, 2019]
    FLAG_DATA = True
    FLAG_TEAM = True

    index = 0

    if os.path.exists('../data'):
        shutil.rmtree('../data')

    for teams in LIST_OF_TEAMS:
        if FLAG_DATA:
            os.chdir("..")
            os.mkdir("data")
            os.chdir("data")
            FLAG_DATA = False
        for team in teams:
            if FLAG_TEAM:
                os.mkdir("season_" + YEARS[index])
                os.chdir("season_" + YEARS[index])
                FLAG_TEAM = False
            async with aiohttp.ClientSession() as session:
                understat = Understat(session)

                data = await understat.get_team_results(
                    team,
                    YEARS_FLAG[index],
                    side="h"
                )
                data_to_csv = data.copy()
                print(json.dumps(data))

                data2 = await understat.get_team_results(
                    team,
                    YEARS_FLAG[index],
                    side="a"
                )
                data_to_csv2 = data2.copy()
                print(json.dumps(data2))

            dct = {}
            tab = []

            for match in data_to_csv:
                dct[match['a']['title']] = match['xG']['h']
                tab.append(match['xG']['a'])

            df = pd.DataFrame(dct.items(), columns=['away_team', 'xG_home'])
            df['home_team'] = team
            df['xG_away'] = tab
            df = df[['home_team', 'away_team', 'xG_home', 'xG_away']]
            df.to_csv(f'{team}' + '_' + YEARS[index] + '.csv')

        os.chdir("..")
        FLAG_TEAM = True
        index += 1


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
