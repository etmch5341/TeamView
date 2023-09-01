class TeamCalendar:

    def __init__(self, team):
        team_cal_info = None
        if team == "Analytics":
            team_cal_info = self.get_analytics()
        elif team == "Events":
            team_cal_info = self.get_events()
        elif team == "Feasibility Studies":
            team_cal_info = self.get_feasibility_studies()
        elif team == "Fundraising":
            team_cal_info = self.get_fundraising()
        elif team == "Internal Development":
            team_cal_info = self.get_internal_development()
        elif team == "Media":
            team_cal_info = self.get_media()
        elif team == "Procurement":
            team_cal_info = self.get_procurement()
        else:
            raise ValueError

        self.id = team_cal_info[0]
        self.link = team_cal_info[1]

    def set_id(self, id:str = None):
        self.id = id

    def get_analytics(self):
        return ["AQMkADAwATMwMAItNWY0Zi1kYmQzLTAwAi0wMAoARgAAA8n1yLB8EIJLoqBGyWANtnQHAGD6PCQ31ktBkAdgzF7RLZEAAAIBBgAAAGD6PCQ31ktBkAdgzF7RLZEAAAADB-CSAAAA",
                "https://outlook.live.com/owa/calendar/665e3870-ebe5-4d2f-82c8-f3a43c214df9/58b1aaec-afd0-4973-a69b-f0de6f4f8d65/cid-348A43DBD86DF613/calendar.ics"]
    
    def get_events(self):
        return ["AQMkADAwATMwMAItNWY0Zi1kYmQzLTAwAi0wMAoARgAAA8n1yLB8EIJLoqBGyWANtnQHAGD6PCQ31ktBkAdgzF7RLZEAAAIBBgAAAGD6PCQ31ktBkAdgzF7RLZEAAAADB-CTAAAA",
                "https://outlook.live.com/owa/calendar/00000000-0000-0000-0000-000000000000/1106af64-35b1-4ed4-a2eb-96130328b802/cid-348A43DBD86DF613/calendar.ics"]
    
    def get_feasibility_studies(self):
        return ["AQMkADAwATMwMAItNWY0Zi1kYmQzLTAwAi0wMAoARgAAA8n1yLB8EIJLoqBGyWANtnQHAGD6PCQ31ktBkAdgzF7RLZEAAAIBBgAAAGD6PCQ31ktBkAdgzF7RLZEAAAADB-CUAAAA",
                "https://outlook.live.com/owa/calendar/00000000-0000-0000-0000-000000000000/497013c5-55d4-415f-9b6c-3abfd24e789c/cid-348A43DBD86DF613/calendar.ics"]
    
    def get_fundraising(self):
        return ["AQMkADAwATMwMAItNWY0Zi1kYmQzLTAwAi0wMAoARgAAA8n1yLB8EIJLoqBGyWANtnQHAGD6PCQ31ktBkAdgzF7RLZEAAAIBBgAAAGD6PCQ31ktBkAdgzF7RLZEAAAADB-CVAAAA",
                "https://outlook.live.com/owa/calendar/00000000-0000-0000-0000-000000000000/2341b980-fed2-41c7-8e96-eb5ac4c150f8/cid-348A43DBD86DF613/calendar.ics"]
    
    def get_internal_development(self):
        return ["AQMkADAwATMwMAItNWY0Zi1kYmQzLTAwAi0wMAoARgAAA8n1yLB8EIJLoqBGyWANtnQHAGD6PCQ31ktBkAdgzF7RLZEAAAIBBgAAAGD6PCQ31ktBkAdgzF7RLZEAAAADB-CWAAAA",
                "https://outlook.live.com/owa/calendar/00000000-0000-0000-0000-000000000000/6375e188-bdbc-4bde-bc69-8533f1e5b1aa/cid-348A43DBD86DF613/calendar.ics"]
    
    def get_media(self):
        return ["AQMkADAwATMwMAItNWY0Zi1kYmQzLTAwAi0wMAoARgAAA8n1yLB8EIJLoqBGyWANtnQHAGD6PCQ31ktBkAdgzF7RLZEAAAIBBgAAAGD6PCQ31ktBkAdgzF7RLZEAAAADB-CXAAAA",
                "https://outlook.live.com/owa/calendar/00000000-0000-0000-0000-000000000000/ff1f1856-2486-4f07-b51a-1fd075b34f4e/cid-348A43DBD86DF613/calendar.ics"]
    
    def get_procurement(self):
        return ["AQMkADAwATMwMAItNWY0Zi1kYmQzLTAwAi0wMAoARgAAA8n1yLB8EIJLoqBGyWANtnQHAGD6PCQ31ktBkAdgzF7RLZEAAAIBBgAAAGD6PCQ31ktBkAdgzF7RLZEAAAADB-CYAAAA",
                "https://outlook.live.com/owa/calendar/00000000-0000-0000-0000-000000000000/a56e02cd-3fa9-4da4-9486-3725bc119390/cid-348A43DBD86DF613/calendar.ics"]