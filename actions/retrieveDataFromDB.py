from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet

from rasa_sdk.executor import CollectingDispatcher

import pymongo

# your code here

class RetrieveDataFromDB(Action):
    def __init__(self):

        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["trading-cbe"]
        collection = db["CommonBackend-Security"]
        data = collection.find({}, {"Name": 1, "Symbol": 1})
        print("hello")
        symbol_name_map = {}
        for item in data:
            symbol = item["Symbol"]
            name = item["Name"]
            symbol_name_map[symbol] = name
        self.symbol_name_map=symbol_name_map

        # Store the database output in the tracker object as an attribute
        
    def name(self) -> Text:
        return "action_retrieve_data"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [SlotSet("stock_map", self.symbol_name_map)]


