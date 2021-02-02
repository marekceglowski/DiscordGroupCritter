class Feedback:
    def __init__(self, message_id, submission_id, user_id, received_user_id, jump_url):
        self.message_id = message_id  # PK -- discord's message id
        self.submission_id = submission_id  # FK submissions.id
        self.user_id = user_id  # FK users.id
        self.received_user_id = received_user_id  # FK users.id
        self.jump_url = jump_url
