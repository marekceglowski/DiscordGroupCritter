class Submission:
    def __init__(self, message_id, user_id, jump_url, created_at, status):
        self.message_id = message_id  # PK - discord's message id
        self.user_id = user_id  # FK users.user_id
        self.jump_url = jump_url
        self.created_at = created_at
        self.status = status
