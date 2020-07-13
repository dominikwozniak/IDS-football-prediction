# Target: Fetch xG data from understat.com
# https://github.com/amosbastian/understat

import asyncio
import json
import aiohttp
from understat import Understat


async def main():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = await understat.get_league_players("epl", 2018, {"team_title": "Manchester United"})
        print(json.dumps(data))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
