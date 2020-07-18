# Target: Fetch xG data from understat.com
# https://github.com/amosbastian/understat

import asyncio
import json
import aiohttp
from understat import Understat
import pandas as pd

from .xG_teams import *


async def main():
    for team in TEAMS_2018:
        async with aiohttp.ClientSession() as session:
            understat = Understat(session)

            data = await understat.get_team_results(
                team,
                2018,
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
        df.to_csv(f'{team}_2018.csv')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
