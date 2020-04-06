# app/email/messages.py

class Message:

    def __init__(self, code, subject, message):

        self.code = code
        self.subject = subject
        self.message = message


class MessageManager:

    def __init__(self):

        self.messages = list()

    def append(self, message):

        self.messages.append(message)

    def get(self, code):

        for message in self.messages:

            if message.code == code:

                return message


def build_manager():

    result = [
        {
            "code": "ASSIGN_RESEARCH",
            "subject": "You have been assigned a new order",
            "message": "You have been assigned order ID {} in the Property Management Addresses System, with a due date {}. Start your research as soon as posible."
        },

        {
            "code": "ASSIGN_DATA",
            "subject": "You have been assigned a new order",
            "message": "You have been assigned order ID {} in the Property Management Addresses System, with a due date {}. Start your tasks as soon as posible."
        },

        {
            "code": "NOTIFY_MANAGER",
            "subject": "An order have been marked as finished",
            "message": "Order ID {} have been finished go to the Property Management Addresses System, to search and create reports."
        }
    ]

    manager = MessageManager()

    for message in result:

        message = Message(message["code"], message["subject"], message["message"])

        manager.append(message)

    return manager
