
from typing import Dict, Text, Any, List, Union,Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType,AllSlotsReset,ActionExecuted
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import FormValidationAction
from rasa_sdk.types import DomainDict

from .verif_params.CheckParamsAction import CheckFilteredObj,CheckCreterias,CheckPage,CheckSecurity
import json
import random
import yfinance as yf
class BuyStockAction(Action):

    def name(self) -> Text:
        return "action_buy_stock"
    
    def dispatchMessage(self,dispatcher,intent,stock_number,stock_company,response_message):
         
        response_dict = {"intent": intent, "entities": [{"stock_number":stock_number},{"stock_company":stock_company}], "response": response_message}

        dispatcher.utter_message(json.dumps(response_dict))
        return []

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get latest user message
        latest_message = tracker.latest_message
        
        # Get intent and extracted entities
        intent = latest_message['intent']['name']
        stock_number = tracker.get_slot("stock_number")
        stock_company = tracker.get_slot("stock_company")
        
        if stock_company:
            event = ActionExecuted("action_check_security")
            if not event:
                response_message="Please enter a valid security name"
                return[]
            tracker.slots['stock_company'] = stock_company
        if stock_number:
            tracker.slots['stock_number'] = stock_number

        if not stock_company and not stock_number:

            response_message="Please provide the stocks number and the name of the security"
            event=self.dispatchMessage(dispatcher,intent,stock_number,stock_company,response_message)
            return []

        elif not stock_company:
            response_message="Please provide the name of the security"
            event=self.dispatchMessage(dispatcher,intent,stock_number,stock_company,response_message)
            return [SlotSet("stock_company", stock_company), SlotSet("stock_number", stock_number)]

        elif not stock_number:

            response_message="Please provide the number of stocks"
            event=self.dispatchMessage(dispatcher,intent,stock_number,stock_company,response_message)
            return [SlotSet("stock_company", stock_company), SlotSet("stock_number", stock_number)]
        
        # Generate response message
        response_message = f"processing command..."
        event=self.dispatchMessage(dispatcher,intent,stock_number,stock_company,response_message)


        return [AllSlotsReset()]
    
   
    

class NavigateAction(Action):

    def name(self) -> Text:
        return "action_navigate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get latest user message
        latest_message = tracker.latest_message
        
        # Get intent and extracted entities
        intent = latest_message['intent']['name']
        page =tracker.get_slot("page")
        
        # Save extracted entities in slots
        if page:
            checkPage = CheckPage()
        # call the run method of CheckPage
            is_valid=checkPage.run(dispatcher, tracker, domain)["is_valid_page"]
            if not is_valid:
                response_message = f"{page} is not present in the application, please specify a valid page"
            else:
                response_message = f"navigating to {page}"     
            # Generate response message
        else:
            response_message = f"please specify the name of the page"
        response_dict = {"intent": intent, "entities": {"page":page}, "response": response_message}
        # Send response message using dispatcher
        dispatcher.utter_message(json.dumps(response_dict))

        return []
        

class FilterAction(Action):

    def name(self) -> Text:
        return "action_filter"
    
    def dispatchMessage(self,dispatcher,intent,filtered_obj,criteria_list,stock_list,response_message):
         
        # Create the response dictionary with the retrieved lists
        response_dict = {"intent": intent, 
                 "entities": [{"filtered_obj":filtered_obj},
                              {"criteria":criteria_list},
                              {"stock_list":stock_list}],
                 "response": response_message}

        # Send the response back to the user
        dispatcher.utter_message(json.dumps(response_dict))
        return []

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get latest user message
        latest_message = tracker.latest_message
        
        # Get intent and extracted entities
        intent = latest_message['intent']['name']
        filtered_obj = tracker.get_slot("filtered_obj")
        criteria_list = tracker.get_slot("criteria")
        stock_list=tracker.get_slot("stock_list")
        #check filtered obj
        if filtered_obj:
            checkFilteredObj = CheckFilteredObj()
            # call the run method of CheckPage
            is_valid=checkFilteredObj.run(dispatcher, tracker, domain)["is_valid_filtered_obj"]
            if not is_valid:
                response_message="Please enter a valid object to filter"
                self.dispatchMessage(dispatcher,intent,filtered_obj,criteria_list,stock_list,response_message)
                return []
            tracker.slots['filtered_obj'] = filtered_obj
        #check criteria_list
        if criteria_list:
            tracker.slots['criteria'] = criteria_list
        if not filtered_obj:

            response_message="Please specify what you need to filter"
            event=self.dispatchMessage(dispatcher,intent,filtered_obj,criteria_list,stock_list,response_message)
            return []
        
        # Generate response message
        response_message = f"processing command..."
        event=self.dispatchMessage(dispatcher,intent,filtered_obj,criteria_list,stock_list,response_message)


        return [AllSlotsReset()]

class SearchAction(Action):

    def name(self) -> Text:
        return "action_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get latest user message
        latest_message = tracker.latest_message
        
        # Get intent and extracted entities
        intent = latest_message['intent']['name']
        query =tracker.get_slot("query")
        #if term exists
        if query:
            tracker.slots['query'] = query
            response_message = f"searching for {query}"     
        else:
            response_message = f"please specify the search term"
        response_dict = {"intent": intent, "entities": {"query":query}, "response": response_message}
        # Send response message using dispatcher
        dispatcher.utter_message(json.dumps(response_dict))

        return [SlotSet("query", query)]
        


    

class SellStockAction(Action):

    def name(self) -> Text:
        return "action_sell_stock"
    
    def dispatchMessage(self,dispatcher,intent,stock_number,stock_company,response_message):
         
        response_dict = {"intent": intent, "entities": [{"stock_number":stock_number},{"stock_company":stock_company}], "response": response_message}

        dispatcher.utter_message(json.dumps(response_dict))
        return []

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get latest user message
        latest_message = tracker.latest_message
        # Get intent and extracted entities
        intent = latest_message['intent']['name']
        stock_number = tracker.get_slot("stock_number")
        stock_company = tracker.get_slot("stock_company")
        
        if stock_company:
            event = ActionExecuted("action_check_security")
            if not event:
                response_message="Please enter a valid security name"
                return[]
            tracker.slots['stock_company'] = stock_company
        if stock_number:
            tracker.slots['stock_number'] = stock_number

        if not stock_company and not stock_number:

            response_message="Please provide the stocks number and the name of the security"
            event=self.dispatchMessage(dispatcher,intent,stock_number,stock_company,response_message)
            return []

        elif not stock_company:
            response_message="Please provide the name of the security"
            event=self.dispatchMessage(dispatcher,intent,stock_number,stock_company,response_message)
            return [SlotSet("stock_company", stock_company), SlotSet("stock_number", stock_number)]

        elif not stock_number:

            response_message="Please provide the number of stocks"
            event=self.dispatchMessage(dispatcher,intent,stock_number,stock_company,response_message)
            return [SlotSet("stock_company", stock_company), SlotSet("stock_number", stock_number)]
        
        # Generate response message
        response_message = f"processing command..."
        event=self.dispatchMessage(dispatcher,intent,stock_number,stock_company,response_message)


        return [AllSlotsReset()]



class OtherAction(Action):

    def name(self) -> Text:
        return "action_other"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get latest user message
        latest_message = tracker.latest_message
        intent_template_map = {
            "greet": "utter_greet",
            "goodbye": "utter_goodbye",
        }
        # Get intent and extracted entities
        intent = latest_message['intent']['name']
        template_key = intent_template_map.get(intent, "utter_default")


        response = random.choice(domain["responses"][template_key])
        response_dict = {"intent": intent, "response":response["text"]}
        # Send response message using dispatcher
        dispatcher.utter_message(json.dumps(response_dict))

        return []
    
class FallbackAction(Action):

    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        default_message="default response"
        response_dict = {"intent": "fallback", "response":default_message}
        # Send response message using dispatcher
        dispatcher.utter_message(json.dumps(response_dict))

        return []
    
class StockPriceAction(Action):

    def name(self) -> Text:
        return "action_stock_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        latest_message = tracker.latest_message
        
        # Get intent and extracted entities
        intent = latest_message['intent']['name']
        stock_map =tracker.get_slot("stock_map")
        stock_name =str(tracker.get_slot("stock_company"))
        stock_name_list = list(stock_map[0].values())
        stock_symbol_list = [key for dict in stock_map for key in dict.keys()]
        #stock_symbol_list=['CW', 'EK','IBM', 'MSFT', 'AMR']
        if stock_name in stock_name_list:
            # If it is, get the symbol
            cw_symbol = next((key for key, value in stock_map[0].items() if value == stock_name), None)
            if cw_symbol is not None:
                ticker = yf.Ticker(cw_symbol)
                info = ticker.info 
                response_dict = {"intent": "stock_price", "response":f"the current price of {stock_name} is {info['currentPrice']}"}
            else:
                response_dict = {"intent": "stock_price", "response":f"{stock_name} stock symbol not found"}
        elif stock_name.upper() in stock_symbol_list:
            ticker = yf.Ticker(stock_name)
            info = ticker.info 
            response_dict = {"intent": "stock_price", "response":f"the current price of {stock_name} is {info['currentPrice']}"}
        else:
            response_dict = {"intent": "stock_price", "response":f"{stock_name} stock is not registered "}


        # Send response message using dispatcher
        dispatcher.utter_message(json.dumps(response_dict))

        return []