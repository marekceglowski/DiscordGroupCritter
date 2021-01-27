class Submission:
    def __init__(self, id, message_id, user_id, jump_url, created_at, status):
        self.id = id
        self.message_id = message_id
        self.user_id = user_id  # FK users.id
        self.jump_url = jump_url
        self.created_at = created_at
        self.status = status
