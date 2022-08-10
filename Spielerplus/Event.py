from typing import Dict, List, Tuple


class SpielerplusGame:
    def __init__(self):
        from datetime import datetime, time

        self.send_mail = False
        self.send_push = False
        self.reminder_date = datetime(2021, 12, 21, 19, 0, 0, 0)
        self.participation_date = datetime(2021, 12, 22, 11, 0, 0, 0)
        self.participation_scenario = 2
        self.ground = 2
        self.premises = ""
        self.timezone_id = 321
        self.start = datetime(2022, 1, 1, 13, 13, 0, 0)
        self.end = datetime(2022, 1, 1, 15, 15, 0, 0)
        self.meeting_time = time(11, 11, 0)
        self.info = ""
        self.name = "Spiel"
        self.home_game = True
        self.opponent_name = ""
        self.location = ""

    def to_form_data(self) -> Tuple[str, str]:
        # TODO: get roles to nominate from spielerplus (different for every team)

        dt_fmt = "%Y-%m-%d %H:%M:%S"
        d_fmt = "%Y-%m-%d"
        t_fmt = "%H:%M:%S"
        return f"""-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="Game[opponentname]"

{self.opponent_name}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="Game[homegame]"

{int(self.home_game)}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="Game[eventname]"

{self.name}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="Game[info]"

{self.info}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="datepicker-modal-startdate280"

{self.start.strftime("%d.%m.%Y")}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="Game[startdate]"

{self.start.strftime(d_fmt)}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="startdate-datetime-startdate-disp"

{self.start.strftime("%d.%m.%Y")}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="initialStartdate"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="hour"

{self.meeting_time.strftime("%H")}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="minute"

{self.meeting_time.strftime("%M")}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="timepicker-modal-meetingtime"

{self.meeting_time.strftime("%H:%M")}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="Game[meetingtime]"

{self.meeting_time.strftime(t_fmt)}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="meetingtime-datetime-meetingtime-disp"

{self.meeting_time.strftime("%H:%M")}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="hour"

{self.start.strftime("%H")}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="minute"

{self.start.strftime("%M")}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="timepicker-modal-starttime"

{self.start.strftime("%H:%M")}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="Game[starttime]"

{self.start.strftime(t_fmt)}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="starttime-datetime-starttime-disp"

{self.start.strftime("%H:%M")}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="datepicker-modal-enddate646"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="Game[enddate]"

{self.end.strftime(d_fmt)}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="enddate-datetime-enddate-disp"

{self.end.strftime("%d.%m.%Y")}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="hour"

{self.end.strftime("%H")}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="minute"

{self.end.strftime("%M")}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="timepicker-modal-endtime"

{self.end.strftime("%H:%M")}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="Game[endtime]"

{self.end.strftime(t_fmt)}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="endtime-datetime-endtime-disp"

{self.end.strftime("%H:%M")}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="Game[timezone_id]"

{self.timezone_id}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="TeamLocation[autocomplete]"

{self.location}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="Game[location_id]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="location_form_name"

game
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="Game[premises]"

{self.premises}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="Game[ground]"

{self.ground}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[0][url]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[0][name]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[0][type]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[0][length]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[1][url]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[1][name]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[1][type]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[1][length]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[2][url]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[2][name]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[2][type]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[2][length]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[3][url]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[3][name]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[3][type]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[3][length]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[4][url]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[4][name]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[4][type]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[4][length]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[5][url]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[5][name]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[5][type]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[5][length]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[6][url]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[6][name]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[6][type]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[6][length]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[7][url]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[7][name]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[7][type]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[7][length]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[8][url]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[8][name]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[8][type]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[8][length]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[9][url]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[9][name]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[9][type]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="FitnessEvent[9][length]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="NominatedRoles[253116]"

1
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="NominatedRoles[253117]"

1
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="NominatedRoles[253118]"

1
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="NominatedRoles[253119]"

1
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="NominatedRoles[253120]"

1
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="Game[participationscenario]"

{self.participation_scenario}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="Game[participants_limit]"


-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="Game[participationdate]"

{self.participation_date.strftime(dt_fmt)}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="participationdate-game-participationdate-disp"

{self.participation_date.strftime("%d.%m.%Y %H:%M")}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="DynamicModel[fakefieldw32]"

{self.participation_date.strftime("%d.%m.%Y %H:%M")}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="Game[reminderdate]"

{self.reminder_date.strftime(dt_fmt)}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="reminderdate-game-reminderdate-disp"

{self.reminder_date.strftime("%d.%m.%Y %H:%M")}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="DynamicModel[fakefieldw33]"

{self.reminder_date.strftime("%d.%m.%Y %H:%M")}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="Game[sendMail]"

{int(self.send_mail)}
-----------------------------172922225234162545263520663748
Content-Disposition: form-data; name="Game[sendPush]"

{int(self.send_push)}
-----------------------------172922225234162545263520663748--""", \
               "---------------------------172922225234162545263520663748"


class SpielerplusEvent:
    def __init__(self, event_id: str, event_type: str):
        from Spielerplus import User

        self.eid: str = event_id
        self.etype: str = event_type
        self.name: str = ""
        self.date: str = ""
        self.start: str = ""
        self.end: str = ""
        self.is_tracked: bool = False
        self.notified_users: List[str] = []
        self.participants: Dict[str, User] = {}
        self.absents: Dict[str, User] = {}
        self.unassigned: Dict[str, User] = {}
        self.unsafe: Dict[str, User] = {}


if __name__ == "__main__":
    g = SpielerplusGame()
    print(g.to_form_data())
