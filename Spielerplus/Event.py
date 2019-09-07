class SpielerplusEvent:
    def __init__(self, event_id, event_type):
        self.eid = event_id
        self.etype = event_type
        self.name = ""
        self.date = ""
        self.start = ""
        self.end = ""
        self.isTracked = False
        self.participants = {}
        self.absents = {}
        self.unassigned = {}
        self.unsafe = {}
