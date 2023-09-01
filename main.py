import asyncio
import configparser
from msgraph.generated.models.o_data_errors.o_data_error import ODataError
from graph import Graph
from team_calendar import TeamCalendar

async def main():
    print('TeamView\n')

    # Load settings
    config = configparser.ConfigParser()
    config.read(['config.cfg', 'config.dev.cfg'])
    azure_settings = config['azure']

    graph: Graph = Graph(azure_settings)

    # Greet user and store user's name
    user_name = await greet_user(graph)

    # Business Team Names
    business_team_list = ["Analytics", "Events", "Feasibility Studies", "Fundraising", "Internal Development", "Media", "Procurement"]

    # Engineering Team Names
    engineering_team_list = ["Active Guidance", "Breaking", "Communications", "Electromagnetics", "Electronics", "Embedded Systems", "Frame", "Infrastructure", "Manufacturing", "Mechanical Design", "Power Electronics", "Propulsion", "Shell", "Suspension", "Track"]

    user_team = ""

    while user_team == "":
        print("Select your current team(s)")

        # Temp user string input selector (will implement drop down select later)
        try:
            user_team = input()
            if user_team not in business_team_list and user_team not in engineering_team_list:
                raise ValueError
        except ValueError:
            print("Invalid input: ", user_team)

    print("Team: ", user_team)

    team_calendar = TeamCalendar(user_team)

    print("Click on the link to get added to the", user_team, "calendar.")
    print("Link:", team_calendar.link)

    user_input = 0
    while user_input == 0:
        try:
            user_input = int(input("Enter 1 once you have been added to the calendar: "))
        except ValueError:
            user_input = 0

    team_calendar_id = await get_team_calendar_id(graph, user_team)
    if team_calendar_id is None:
        print("Could not find ", user_team, " calendar")
        raise RuntimeError
    
    team_calendar.set_id(team_calendar_id)
    
    print("ID: ", team_calendar.id)
    print("Link: ", team_calendar.link)

    print("\n")

    # TODO: Give user link to accept invitation to team calendar

    '''
    Get list of user's calendars
    Ask users to select calendar to add to group calendar
    Add events from the calendar to the group calendar

    '''

    choice = -1
    while choice != 0:
        print("0. Exit")
        print("1. Run program\n")

        try:
            choice = int(input("INPUT: "))
        except ValueError:
            choice = -1

        print("\n")

        try:
            if choice == 0:
                print("Goodbye...")
            elif choice == 1:
                # TODO: Write Program code HERE

                # Get list of user's calendars
                calendar_dict = await get_calendars(graph)

                # Ask user to select calendar
                for calendar_name in calendar_dict.keys():
                    print(calendar_name, "\n")

                print("Select the calendar you want to add to the \"", user_team, "\" calendar")
                user_calendar = None
                try:
                    user_calendar = input("INPUT: ")
                    if user_calendar not in list(calendar_dict.keys()):
                        raise ValueError
                except ValueError:
                    print("Invalid input: ", user_calendar)

                # Get all events from the calendar 
                # print(user_calendar, "id:", calendar_dict[user_calendar])
                events = await get_events(graph, calendar_dict[user_calendar])
                
                print("\n")

                # Add events to calendar
                for event in events:
                    await add_event(graph, user_name, team_calendar.id, event)
                print("\n", "All events from the", user_calendar, "calendar has been added to the", user_team, "calendar.")

        except ODataError as odata_error:
            print('Error:')
            if odata_error.error:
                print(odata_error.error.code, odata_error.error.message)

async def greet_user(graph: Graph):
    user = await graph.get_user()
    if user:
        print('Hello,', user.display_name)
        # For Work/school accounts, email is in mail property
        # Personal accounts, email is in userPrincipalName
        print('Email:', user.mail or user.user_principal_name, '\n')
    
    return user.display_name

async def get_team_calendar_id(graph: Graph, user_team: str):
    calendars_page = await graph.get_calendars()
    page_count = 0

    # Iterate through calendar pages
    while calendars_page and calendars_page.value:
        page_count += 1
        for calendar in calendars_page.value:
            # print("Name: ", calendar.name, " | id: ", calendar.id)
            if(calendar.name == user_team):
                return calendar.id
        
        # Get next page of calendars
        if(calendars_page.odata_next_link is not None):
            calendars_page = await graph.get_calendars(5 * page_count)
        else:
            calendars_page = None
    
    return None

async def get_calendars(graph: Graph):
    calendar_dict = {}
    calendars_page = await graph.get_calendars()
    page_count = 0
    
    # Iterate through calendar pages
    while calendars_page and calendars_page.value:
        page_count += 1
        for calendar in calendars_page.value:
            # print("Name: ", calendar.name, " | id: ", calendar.id)
            calendar_dict[calendar.name] = calendar.id
        
        # Get next page of calendars
        if(calendars_page.odata_next_link is not None):
            calendars_page = await graph.get_calendars(5 * page_count)
        else:
            calendars_page = None

    # Return dictionary of calendar name (key) and id (value)
    return calendar_dict

async def get_events(graph: Graph, id: str = None):
    events_list = []
    events_page = await graph.get_events(id)
    page_count = 0

    # Itreate through events pages
    while events_page and events_page.value:
        page_count += 1
        for event in events_page.value:
            events_list.append(event)
        
        # Get next page of events
        if(events_page.odata_next_link is not None):
            events_page = await graph.get_events(id, 5 * page_count)
        else:
            events_page = None
    
    # Return list of Event objects with attributes "Start time" and "End time" 
    return events_list

async def add_event(graph: Graph, user_name: str = None, id: str = None, user_event = None):
    await graph.add_event(user_name, id, user_event)
    print("Event Added")


# Run main
asyncio.run(main())