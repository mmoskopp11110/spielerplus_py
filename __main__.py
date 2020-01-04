import jsonpickle
from Spielerplus.Helper import SpielerplusHelper


if __name__ == "__main__":
    print("main:")
    helper = SpielerplusHelper()
    helper.login()
    helper.load_events('events.json')
    helper.joinEvents(helper.events, 936886)
    #helper.get_all_events()
    print(helper.events)
    #with open('events.json', 'w') as f:
    #    f.write(jsonpickle.encode(helper.events))

