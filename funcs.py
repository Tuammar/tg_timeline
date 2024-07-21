from json import load
import datetime


class Huinya:
    def __init__(self, data):
        self.data = data

        self.chats = self.data['chats']['list']
        self.chat_ids = [i['id'] for i in self.chats]
        for i in range(len(self.chats)):
            self.chats[i]['messages'] = sorted(self.chats[i]['messages'], key=lambda x: x['date'])
            # messages are sorted by send-time
            for j in range(len(self.chats[i]['messages'])):
                self.chats[i]['messages'][j]['date'] = datetime.datetime.strptime(self.chats[i]['messages'][j]['date'], '%Y-%m-%dT%H:%M:%S')

        self.frequent_contacts = self.data['frequent_contacts']['list']
        self.frequent_ids = [contact['id'] for contact in self.frequent_contacts]
        # dict_keys(['id', 'category', 'type', 'name', 'rating'])

        self.all_contacts = self.data['contacts']['list']
        # dict_keys(['first_name', 'last_name', 'phone_number', 'date', 'date_unixtime'])
    
    def get_frequent_contacts(self):
        return self.frequent_contacts
    
    def get_all_contacts(self):
        return self.all_contacts

    def get_chat_by_id(self, id):
        self.chat = [i['messages'] for i in self.chats if i['id'] == id][0]
        return self.chat
        # dict_keys(['name', 'type', 'id', 'messages'])

    def get_chat_by_phone_number(self, phone_number):
        for i in self.chats:
            print(i.keys())

    def zalupa(self):
        for i in range(len(self.frequent_contacts)):
            self.frequent_contacts[i]['messages'] = [j['messages'] for j in self.chats
                                                     if j['id'] == self.frequent_contacts[i]['id']]
            # dict_keys(['id', 'category', 'type', 'name', 'rating', 'messages'])
    
    def get_chat_timeline(self, chat):
        self.chat = chat # ИСПРАВИТЬ!!! ГОВНО!!! ОЧЕНЬ ПЛОХО!!!!
        days_number = (self.chat[-1]['date'] - self.chat[0]['date']).days
        self.days_dict = {self.chat[0]['date'].date(): []}
        self.timeline_dict = {self.chat[0]['date'].date(): dict()}
        current_date = self.chat[0]['date'].date()
        for day in range(days_number + 1): # странный ренж
            current_date += datetime.timedelta(days=1)
            self.days_dict[current_date] = []
            self.timeline_dict[current_date] = dict()
        # self.days_dict[current_date]
        for i in range(len(self.chat)):
            message = self.chat[i]
            message_content = message['text']
            message_text = ''
            for j in message_content:
                if isinstance(j, dict):
                    message_text += j['text']
                elif isinstance(j, str):
                    message_text += j
            message['plain_text'] = message_text
            self.days_dict[message['date'].date()].append(message_text)
        return self.days_dict
    
    def analyse_messages(self, timeline):
        for i in timeline.keys():
            if len(timeline[i]) != 0:
                self.timeline_dict[i]['average_message_length'] = round(len(''.join(timeline[i]))/len(timeline[i]), 2)
                self.timeline_dict[i]['number_of_messages'] = len(timeline[i])
            else:
                self.timeline_dict[i]['average_message_length'] = 0
                self.timeline_dict[i]['number_of_messages'] = 0
        return self.timeline_dict
    

file = load(open('result.json'))
z = Huinya(file)
# z.get_chat_by_phone_number(1)
# chat = z.get_chat_by_id(925408615)
# print(z.get_frequent_contacts())
# ac = z.get_all_contacts()
# for i in ac:
#     print(i['phone_number'])
# tl = z.get_chat_timeline()
# z.analyse_messages(tl)
