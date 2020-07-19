# Target: Fetch xG data from understat.com
# https://github.com/amosbastian/understat

import asyncio
import json
import aiohttp
from understat import Understat
import pandas as pd
import os

from xG_teams import *


async def main():
    list_of_TEAMS = [TEAMS_2015, TEAMS_2016, TEAMS_2017, TEAMS_2018, TEAMS_2019]
    years = ['2015', '2016', '2017', '2018', '2019']
    years_fl = [2015, 2016, 2017, 2018, 2019]
    flag_data = True
    flag_team = True
    index = 0
    for teams in list_of_TEAMS:
        if flag_data:
            os.chdir("..")
            os.mkdir("Data")
            os.chdir("Data")
            flag_data = False
        for team in teams:
            if flag_team:
                os.mkdir("Sezon_" + years[index])
                os.chdir("Sezon_" + years[index])
                flag_team = False
            async with aiohttp.ClientSession() as session:
                understat = Understat(session)

                data = await understat.get_team_results(
                    team,
                    years_fl[index],
                    side="h"
                )

                # with open(f'{team}_raw.json', 'w') as outfile:
                # json.dump(data, outfile, sort_keys=True, indent=4,
                # ensure_ascii=False)

                data_to_csv = data.copy()
                # with open(f'{team}_raw.json', 'r') as read_file:
                # data_to_csv = json.load(read_file)

                print(json.dumps(data))

            dct = {}

            for match in data_to_csv:
                dct[match['a']['title']] = match['xG']['h']

            df = pd.DataFrame(dct.items(), columns=['away_team', 'xG'])
            df['home_team'] = team
            df = df[['home_team', 'away_team', 'xG']]
            df.to_csv(f'{team}' + '_'+ years[index] +'.csv')

        os.chdir("..")
        flag_team = True
        index +=1


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


