from typing import Dict, List
from .User import SpielerplusUser as User


class SpielerplusEvent:
    def __init__(self, event_id: str, event_type: str):
        self.eid: str = event_id
        self.etype: str = event_type
        self.name: str = ""
        self.date: str = ""
        self.start: str = ""
        self.end: str = ""
        self.isTracked: bool = False
        self.notifiedUsers: List[str] = []
        self.participants: Dict[str, User] = {}
        self.absents: Dict[str, User] = {}
        self.unassigned: Dict[str, User] = {}
        self.unsafe: Dict[str, User] = {}
