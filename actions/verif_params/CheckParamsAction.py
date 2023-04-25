from typing import Dict, Text, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class CheckSecurity(Action):
    securities_list = ["google", "tesla", "nvidia","apple","microsoft","intel","ibm"]

    def name(self) -> Text:
        return "action_check_security"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        security_name = tracker.get_slot("stock_name")
        

        if security_name in self.securities_list:
            return {"is_valid_security":True}
        else:
           return {"is_valid_security":False}
    
class CheckPage(Action):
    pages_list = ["orders", "placements", "dashboard","setting","profile","portfolio"]

    def name(self) -> Text:
        return "action_check_page"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        page = tracker.get_slot("page")
        

        if page in self.pages_list:
            return {"is_valid_page":True}
        else:
           return {"is_valid_page":False}
        
class CheckCreterias(Action):
    creterias_list = ["closed", "filled", "working","paused","new","pending"]

    def name(self) -> Text:
        return "action_check_criteria"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        criteria = tracker.get_slot("criteria")
        

        if criteria in self.creterias_list:
            return {"is_valid_creterias":True}
        else:
           return {"is_valid_creterias":False}
        
class CheckFilteredObj(Action):
    filtered_obj_list = ["orders", "placements"]

    def name(self) -> Text:
        return "action_check_filtered_obj"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        filtered_obj = tracker.get_slot("filtered_obj")
        

        if filtered_obj in self.filtered_obj_list:
            return {"is_valid_filtered_obj":True}
        else:
           return {"is_valid_filtered_obj":False}
        
