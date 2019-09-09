import requests
from bs4 import BeautifulSoup
import json
import re
from Spielerplus.User import SpielerplusUser
from Spielerplus.Event import SpielerplusEvent
import jsonpickle
import py_linq
import time


class SpielerplusHelper:
    def __init__(self):
        self.baseurl = "https://www.spielerplus.de"
        self.client = None
        self.isLoggedIn = False
        self.events = {}
        self.users = {}
        self.list_modes = {
            'unassigned': 0,
            'absent': 1,
            'participating': 2,
            'unsafe': 3
        }
        self.ifttt_url = 'https://maker.ifttt.com/trigger/spielerplus/with/key/bpw1Uqr9MJpEDnjhcBvN-e'

    def login(self, mail, password):
        if self.isLoggedIn:
            return
        url = "{}/en/site/login".format(self.baseurl)
        self.client = requests.session()
        # Retrieve the CSRF token first
        login_request = self.client.get(url)  # sets cookie
        soup = BeautifulSoup(login_request.text, 'html.parser')
        csrf = soup.find('meta', {"name": 'csrf-token'}).attrs['content']
        print('csrf token: {}'.format(csrf))

        # login
        login = self.client.post(url, data={
            '_csrf': csrf,
            'LoginForm[email]': mail,  # 'markus.moskopp@web.de',
            'LoginForm[password]': password  # 'Machmo95'
        })

        if login.status_code < 400:
            self.isLoggedIn = True

    def get_all_events(self):
        # todo: new thread for every soup (possible with client?)
        print(0)
        events_soup = BeautifulSoup(self.client.get("{}/events".format(self.baseurl)).text, 'html.parser')
        self.get_page_events(events_soup)
        offset = 0
        while True:
            offset = offset + 5
            print(offset)
            events_req = self.client.post('{}/events/ajaxgetevents'.format(self.baseurl),
                                          data={'offset': offset})
            events_reply = json.loads(events_req.text)

            # exit condition
            if 'count' not in events_reply or events_reply['count'] == -1 or 'html' not in events_reply:
                break

            events_soup = BeautifulSoup(events_reply['html'].replace('\n', ''), 'html.parser')
            self.get_page_events(events_soup)

    def get_page_events(self, soup):
        event_list = soup.select('.panel[id^="event-"]')
        events = []
        # get general event info
        for event in event_list:
            if 'id' in event.attrs:
                idstring = event.attrs['id']
                event_id = re.search('[0-9]+', idstring).group(0)
                try:
                    if event_id in self.events:
                        continue
                    event_type = re.search('event-[a-z]+', idstring).group(0).replace('event-', '')
                    new_event = SpielerplusEvent(event_id, event_type)

                    # get event name
                    new_event.name = event.select('.panel-title')[1].text

                    # times
                    times = event.select('.event-time-label + .event-time-value')
                    new_event.start = times[1].text.replace('\n', '').strip()
                    new_event.end = times[2].text.replace('-:-', '').replace('\n', '').strip()
                    if new_event.end == '':
                        new_event.end = '23:00 Uhr'

                    events.append(new_event)
                    self.events[event_id] = new_event
                except:
                    pass
            else:
                continue

        # get event details
        for event in events:
            # get participation
            participation_req = self.client.post("{}/events/ajaxgetparticipation".format(self.baseurl),
                                                 data={'eventid': event.eid, 'eventtype': event.etype})
            participation_reply = json.loads(participation_req.text)['html'].replace('\n', '')
            participation_modal = BeautifulSoup(participation_reply, 'html.parser')

            # event date
            event_header_subline = participation_modal.select('.participation-header .subline')
            datetimestring = event_header_subline[0].text.strip()
            event.date = re.search('^[0-9.]+', datetimestring).group(0)

            # not assigned users
            self.get_participation(event, participation_modal, self.list_modes['unassigned'])

            # participants
            self.get_participation(event, participation_modal, self.list_modes['participating'])

            # absents
            self.get_participation(event, participation_modal, self.list_modes['absent'])

            # unsafe
            self.get_participation(event, participation_modal, self.list_modes['unsafe'])

    def get_participation(self, event, modal_soup, list_mode):
        selector = ''
        if list_mode == self.list_modes['unassigned']:
            selector = '#Noch'
        elif list_mode == self.list_modes['absent']:
            selector = '#Absa'
        elif list_mode == self.list_modes['participating']:
            selector = '#Zuge'
        elif list_mode == self.list_modes['unsafe']:
            selector = '#Unsi'
        else:
            return

        # clear participation
        event.participants = {}
        event.absents = {}
        event.unassigned = {}
        event.unsafe = {}

        participation_list = modal_soup.select('{} .participation-list-user'.format(selector))
        for user in participation_list:
            userstring = str(user)
            try:
                uid = re.search('id=[0-9]+', userstring).group(0).replace('id=', '')
                username = re.search('participation-list-user-name">[A-Za-zäöüÄÖÜß ]+</div>', userstring).group(0) \
                    .replace('participation-list-user-name">', '') \
                    .replace('</div>', '')
                if uid not in self.users:
                    self.users[uid] = SpielerplusUser(uid, username)
                # add to event list
                if list_mode == self.list_modes['unassigned']:
                    if uid not in event.unassigned:
                        event.unassigned[uid] = self.users[uid]
                elif list_mode == self.list_modes['absent']:
                    if uid not in event.absents:
                        event.absents[uid] = self.users[uid]
                elif list_mode == self.list_modes['participating']:
                    if uid not in event.participants:
                        event.participants[uid] = self.users[uid]
                elif list_mode == self.list_modes['unsafe']:
                    if uid not in event.unsafe:
                        event.unsafe[uid] = self.users[uid]
            except AttributeError:
                pass

    def load_events(self, filename):
        try:
            with open(filename, 'r') as f:
                jsonstring = f.read().replace('\n', '')
                self.events = jsonpickle.decode(jsonstring)
        except FileNotFoundError:
            pass

    def track_events(self, name):
        for event in self.events:
            ev = self.events[event]
            totrack = {**ev.unassigned, **ev.unsafe}

            if not ev.isTracked:
                # add calendar event
                if ev.end == '':
                    ev.end = '23:00 Uhr'
                data = {
                    'value1': format_datetime(ev.date, ev.start),
                    'value2': format_datetime(ev.date, ev.end),
                    'value3': ev.name
                }
                r = requests.post(self.ifttt_url, data=data)
                if r.ok:
                    ev.isTracked = True

            doTrack = py_linq.Enumerable(totrack.values()).where(lambda u: u.name == name).first_or_default()
            if doTrack:
                if doTrack.uid not in ev.notifiedUsers:
                    # todo: notify user
                    pass


def format_datetime(date, hour):
    dtstr = '{} {}'.format(date, hour)
    t = time.strptime(dtstr, '%d.%m.%y %H:%M Uhr')
    return time.strftime('%Y-%m-%dT%H:%MTZD', t)
