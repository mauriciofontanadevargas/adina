# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa.shared.core.constants import ACTION_DEFAULT_FALLBACK_NAME
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, UserUtteranceReverted
import os.path
from os import path
import json
import actions.gpt3 as gpt3

class UserManager:

    def __init__(self, user_name="", last_issue = ""):
        self.user_name = user_name
        self.last_issue = last_issue

    def load_user(self):
        print("Loading user from disk")
        if path.exists("C:\\Users\\Mauricio\\OneDrive\\OneDrive - McGill University\\McGill\Adina\\rasa_demo\\actions\\userdb.json"):
            f = open("C:\\Users\\Mauricio\\OneDrive\\OneDrive - McGill University\\McGill\Adina\\rasa_demo\\actions\\userdb.json",'r+')
            try:
                data = json.load(f)
                u = UserManager(**data)
                self.user_name = u.user_name
                self.last_issue = u.last_issue
            except json.decoder.JSONDecodeError:
                print("No user in the db")
        else:
            f = open("C:\\Users\\Mauricio\\OneDrive\\OneDrive - McGill University\\McGill\Adina\\rasa_demo\\actions\\userdb.json",'w')

        f.close()

    def persist_user(self):
        with open("C:\\Users\\Mauricio\\OneDrive\\OneDrive - McGill University\\McGill\Adina\\rasa_demo\\actions\\userdb.json", 'w') as outfile:
          json.dump(self, outfile, default=vars)
        outfile.close()

# #
# def main():
#     u = UserManager()
#     u.load_user()
#
#     print(u.user_name)
#
#     u.user_name = "b"
#     u.persist_user()
#
#
# if __name__ == "__main__":
#     main()

class ActionGetUser(Action):

    # this name is what links the python code with the yml files
    def name(self) -> Text:
        return "action_get_user"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_db = UserManager()
        user_db.load_user()

        print("User: " + user_db.user_name)
        return [SlotSet("user_name", user_db.user_name if user_db.user_name != "" else None)]

class ActionRegisterUser(Action):

    # this name is what links the python code with the yml files
    def name(self) -> Text:
        return "action_register_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_db = UserManager()
        user_db.load_user()
        if next(tracker.get_latest_entity_values("user_name"), None) is not None:
            user_db.user_name = next(tracker.get_latest_entity_values("user_name"), None)
            user_db.persist_user()

        print("User registered in the DB: " + user_db.user_name)
        return []

class ActionGetLastIssue(Action):

    # this name is what links the python code with the yml files
    def name(self) -> Text:
        return "action_get_last_issue"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_db = UserManager()
        user_db.load_user()

        print("Last issue: " + user_db.last_issue)
        return [SlotSet("last_issue", user_db.last_issue if user_db.last_issue !="" else None)]


class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    gpt3_handler = gpt3.gpt3Interface()

    def name(self) -> Text:
        return ACTION_DEFAULT_FALLBACK_NAME

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # dispatcher.utter_message(template="my_custom_fallback_template")
        print("Action Fallback called")
        print("Last message was: " + tracker.latest_message['text'])
        response = self.gpt3_handler.sendCompletionQuery(tracker.latest_message['text'])
        print("gpt3 response: " + response)
        dispatcher.utter_message(text=response)


        return [UserUtteranceReverted()]

    #EVENTS RETURNED BY A CUSTOM ULTIMATE FALLBACK ACTION
      # You should include UserUtteranceReverted() as one of the events returned by your custom action_default_fallback.
    #  Not including this event will cause the tracker to include all events that happened during the Two-Stage Fallback
    #  process which could interfere with subsequent action predictions from the bot's policy pipeline.
    #  It is better to treat events that occurred during the Two-Stage Fallback process as if they did not happen so that your bot can apply
    #  its rules or memorized stories to correctly predict the next action.

