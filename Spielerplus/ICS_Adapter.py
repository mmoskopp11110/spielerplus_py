from typing import List
from datetime import datetime, time, tzinfo
from dateutil.relativedelta import relativedelta as rd

from Spielerplus.Event import SpielerplusGame
from Spielerplus.Info import team_name


def _get_events_from_ical(url: str):
    from ics import Calendar
    import requests
    import py_linq

    c = Calendar(requests.get(url).text)
    e = py_linq.Enumerable(list(c.events)).where(lambda ev: ev.begin.int_timestamp > datetime.now().timestamp()).to_list()
    e.sort(key=lambda ev: ev.begin.int_timestamp)
    return e


def _parse_event_name(name: str):
    # remove leading league name, replace team name separator, split into team names
    teams = name.split(':')[1].strip().replace(" - ", ";").split(";")
    home_team, away_team = teams[0], teams[1]
    if team_name == home_team:
        return away_team, True
    else:
        return home_team, False


def games_from_ical(url: str) -> List[SpielerplusGame]:
    games = []
    events = _get_events_from_ical(url)

    for event in events:
        game = SpielerplusGame()
        game.start = event.begin.datetime
        game.start = game.start.astimezone()
        game.end = game.start + rd(hours=2)
        game.reminder_date = game.start - rd(days=8)
        game.reminder_date = game.reminder_date.replace(hour=19, minute=0)
        game.participation_date = game.start - rd(days=7)
        game.participation_date = game.participation_date.replace(hour=19, minute=0)
        game.opponent_name, game.home_game = _parse_event_name(event.name)
        game.name = game.opponent_name
        if not game.home_game:
            game.premises = event.location.split(",")[0]
            game.location = event.location
            game.info = event.location
            game.meeting_time = (game.start - rd(hours=2)).time()
        else:
            game.meeting_time = (game.start - rd(hours=2, minutes=30)).time()
        games.append(game)

    return games
