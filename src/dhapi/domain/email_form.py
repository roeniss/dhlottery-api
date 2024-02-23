class EmailForm:
    def __init__(self, api_key, api_secret, sender_email, recipient_email):
        self.api_key = api_key
        self.api_secret = api_secret
        self.sender_email = sender_email
        self.recipient_email = recipient_email
