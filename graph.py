from configparser import SectionProxy
from azure.identity import DeviceCodeCredential
from kiota_authentication_azure.azure_identity_authentication_provider import (
    AzureIdentityAuthenticationProvider)
from msgraph import GraphRequestAdapter, GraphServiceClient
from msgraph.generated.me.me_request_builder import MeRequestBuilder

from msgraph.generated.me.calendars.item.events.events_request_builder import (
    EventsRequestBuilder)

from msgraph.generated.me.calendars.calendars_request_builder import (
    CalendarsRequestBuilder)

from msgraph.generated.models.event import Event
# from msgraph.generated.models.item_body import ItemBody
# from msgraph.generated.models.body_type import BodyType
from msgraph.generated.models.date_time_time_zone import DateTimeTimeZone


class Graph:
    settings: SectionProxy
    device_code_credential: DeviceCodeCredential
    adapter: GraphRequestAdapter
    user_client: GraphServiceClient

    def __init__(self, config: SectionProxy):
        self.settings = config
        client_id = self.settings['clientId']
        tenant_id = self.settings['tenantId']
        graph_scopes = self.settings['graphUserScopes'].split(' ')

        self.device_code_credential = DeviceCodeCredential(client_id, tenant_id = tenant_id)
        auth_provider = AzureIdentityAuthenticationProvider(
            self.device_code_credential,
            scopes=graph_scopes)
        self.adapter = GraphRequestAdapter(auth_provider)
        self.user_client = GraphServiceClient(self.adapter)

    async def get_user_token(self):
        graph_scopes = self.settings['graphUserScopes']
        access_token = self.device_code_credential.get_token(graph_scopes)
        return access_token.token

    async def get_user(self):
        # Only request specific properties using $select
        query_params = MeRequestBuilder.MeRequestBuilderGetQueryParameters(
            select=['displayName', 'mail', 'userPrincipalName']
        )
        request_config = MeRequestBuilder.MeRequestBuilderGetRequestConfiguration(
            query_parameters=query_params
        )

        user = await self.user_client.me.get(request_configuration=request_config)
        return user        
    
    async def get_calendars(self, skip_val: int = None):
        query_params = CalendarsRequestBuilder.CalendarsRequestBuilderGetQueryParameters(
            select = ["id", "name"],
            skip = skip_val,
            top = 5
        )

        request_config = CalendarsRequestBuilder.CalendarsRequestBuilderGetRequestConfiguration(
            query_parameters = query_params
        )

        calendars = await self.user_client.me.calendars.get(request_configuration = request_config)
        return calendars
    
    async def get_events(self, id: str = None, skip_val: int = None):
        # 1. CalendarRequestBuilder id method -> CalendarItemRequestBuilder
        # 2. CalendarItemRequestBuilder events method -> EventsRequestBuilder
        # 3. EventsRequestBuilder -> use normal process

        query_params = EventsRequestBuilder.EventsRequestBuilderGetQueryParameters(
            select = ["start", "end"],
            skip = skip_val,
            top = 5
        )

        request_config = EventsRequestBuilder.EventsRequestBuilderGetRequestConfiguration(
            query_parameters = query_params
        )

        # Use by_calendar_id() method to get specific calendar events
        events = await self.user_client.me.calendars.by_calendar_id(id).events.get(request_configuration = request_config)
        return events
    
    async def add_event(self, user_name: str = None, id: str = None, user_event = None):
        event = Event()
        event.subject = user_name

        # print(user_event.start.time_zone)
        event.start = DateTimeTimeZone()
        event.start.date_time = user_event.start.date_time
        event.start.time_zone = user_event.start.time_zone

        event.end = DateTimeTimeZone()
        event.end.date_time = user_event.end.date_time
        event.end.time_zone = user_event.end.time_zone

        # calendar_item_request_builder = CalendarsRequestBuilder.by_calendar_id(id)
        # calendar = calendar_item_request_builder.get()

        # event.calendar(calendar)

        # TODO: Make this POST in specific calendar using Cal ID 
        # Currently POST into default calendar
        await self.user_client.me.calendars.by_calendar_id(id).events.post(body=event)

        #request_body = 
        # Somehow need to retrieve a RequestBody for an event
        # for send mail it was SendMailPostRequestBody
        # IDK where request body is 
        # Poissibility 1: just have to use CalendarsRequestBuilderPostRequestConfiguration
        # but probably not since it is a request config.
        # Posibility 2: In some folder that has request body object for creating an event
        # more likely since the method to post needs a RequestBody

        '''
        BRUH the request body is the event object 

        read the method header for post --> async def post(self,body: Optional[event.Event] = None, ...

        ie. the body is the event.Event object which is from the models library (alr. imported)

        '''

        

