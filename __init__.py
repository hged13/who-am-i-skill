from mycroft import MycroftSkill, intent_file_handler
import pandas as pd


class WhoAmI(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('i.am.who.intent')
    def handle_i_am_who(self, message):
        self.speak_dialog('i.am.who')
        model = self.build_model()

    def build_model(self):
        file = self.open('/home/pi/.config/mycroft/skills/NewUserCreation/wav.csv', 'r')
        df = pd.read_csv(file)
        return df




def create_skill():
    return WhoAmI()
