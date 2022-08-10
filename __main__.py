import jsonpickle
from datetime import datetime, time
from dateutil.relativedelta import relativedelta as rd

from Spielerplus.Event import SpielerplusGame
from Spielerplus.Helper import SpielerplusHelper
from Spielerplus.ICS_Adapter import games_from_ical


if __name__ == "__main__":
    print("main:")
    games = games_from_ical("https://www.volley.de/resourcerequest/qp/rh-Cal/wid-20909/wsid-1/tid-49811/heimspiele-0")
    helper = SpielerplusHelper()
    helper.login('7276299')  # test
    #helper.login('936886')  # tsv

    #helper.load_events('events.json')
    #helper.joinEvents(helper.events, 936886)
    helper.get_all_events()
    print(helper.events)

    gamedates = [datetime.strptime(ev.date, "%d.%m.%y").date() for ev in helper.events.values() if ev.etype == "game"]
    for game in [g for g in games if g.start.date() not in gamedates]:
        helper.add_gQame(game)
        break
    #with open('events.json', 'w') as f:
        #f.write(jsonpickle.encode(helper.events))
