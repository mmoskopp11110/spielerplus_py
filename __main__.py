import jsonpickle
from datetime import datetime, time
from dateutil.relativedelta import relativedelta as rd

from Spielerplus.Event import SpielerplusGame
from Spielerplus.Helper import SpielerplusHelper
from Spielerplus.ICS_Adapter import games_from_ical


if __name__ == "__main__":
    cache = False
    join = False
    add_games = False
    test = False

    print("main:")

    # load from ical
    if add_games:
        games = games_from_ical("https://www.volley.de/resourcerequest/qp/rh-Cal/wid-28645/wsid-1/tid-62570/heimspiele-0")
    else:
        games = []

    login_data = {
        "user": "",
        "password": ""
    }

    # set team id
    if test:
        team = "7276299"  # test
    else:
        team = "936886"  # tsv

    helper = SpielerplusHelper()
    helper.login(login_data["user"], login_data["password"], team_id=team)

    if cache:
        helper.load_events('events.json')

    helper.get_all_events()
    print(f"loaded {len(helper.events)} events")

    if join:
        helper.join_events(helper.events, team)

    if add_games:
        gamedates = [datetime.strptime(ev.date, "%d.%m.%y").date() for ev in helper.events.values() if ev.etype == "game"]
        for game in [g for g in games if g.start.date() not in gamedates]:
            helper.add_game(game)
            if test:
                break

    if cache:
        with open('events.json', 'w') as f:
            f.write(jsonpickle.encode(helper.events))
    print("done")
