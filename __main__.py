import requests
import re
from bs4 import BeautifulSoup
import json


class SpielerplusUser:
    def __init__(self, uid, username):
        self.uid = uid
        self.name = username


class SpielerplusEvent:
    def __init__(self, event_id, event_type):
        self.eid = event_id
        self.etype = event_type
        self.date = ""
        self.time = ""
        self.participants = {}
        self.absents = {}
        self.unassigned = {}
        self.unsafe = {}


class SpielerplusHelper:
    def __init__(self):
        self.data = []
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
        events_soup = BeautifulSoup(self.client.get("{}/events".format(self.baseurl)).text, 'html.parser')
        self.get_page_events(events_soup)
        offset = 0
        while True:
            offset = offset + 5
            events_req = self.client.post('{}/events/ajaxgetevents'.format(self.baseurl),
                                          data={'offset': offset})
            events_reply = json.loads(events_req.text)

            # exit condition
            if 'count' not in events_reply or events_reply['count'] == -1 or 'html' not in events_reply:
                break

            events_soup = BeautifulSoup(events_reply['html'].replace('\n', ''), 'html.parser')
            self.get_page_events(events_soup)

    def get_page_events(self, soup):
        event_list = soup.find_all('div', {'class': 'list event'})
        events = []
        # get general event info
        for event in event_list:
            event_link_list = event.select('div .event-header-border')
            for event_link in event_link_list:
                if 'href' in event_link.attrs:
                    try:
                        link = event_link.attrs['href']
                        event_id = re.search('[0-9]+', link).group(0)
                        event_type = re.search('/[a-z]+/', link).group(0).replace('/', '')
                        if event_id not in self.events:
                            new_event = SpielerplusEvent(event_id, event_type)
                            events.append(new_event)
                            self.events[event_id] = new_event
                    except:
                        pass

        # get event details
        for event in events:
            # get participation
            participation_req = self.client.post("{}/events/ajaxgetparticipation".format(self.baseurl),
                                             data={'eventid': event.eid, 'eventtype': event.etype})
            participation_reply = json.loads(participation_req.text)['html'].replace('\n', '')
            participation_modal = BeautifulSoup(participation_reply, 'html.parser')

            # event time and date
            event_header_subline = participation_modal.select('.participation-header .subline')
            datetimestring = event_header_subline[0].text
            # todo: parse date and time
            event.date = datetimestring

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


if __name__ == "__main__":
    print("main:")
    helper = SpielerplusHelper()
    helper.login()
    helper.get_all_events()
    print(helper.events)

