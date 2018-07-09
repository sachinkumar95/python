from datetime import datetime



class secret:
    def __init__(self, m, name, age):
        self.m = m
        self.name = name
        self.age = age
        self.is_online = True
        self.chats = []
        self.current_status_message = None


class friend:
    def __init__(self,m,name,age,chat):
        self.m=m
        self.name=name
        self.age=age
        self.chat=chat
        self.current_status_message=None


s = secret('mr.','amit',23)

friend_one = secret('mr.', 'rana', 23)
friend_two = secret('ms.', 'neha', 22)

friends = [friend_one, friend_two]


class chatmessage:
    def __init__(self, message, sent_by_me):
        self.message = message
        self.time = datetime.now()
        self.sent_by_me = sent_by_me
