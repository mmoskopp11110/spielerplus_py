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
