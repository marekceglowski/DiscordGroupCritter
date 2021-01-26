class Feedback:
    def __init__(self, id, message_id, submission_id, user_id, jump_url):
        self.id = id
        self.message_id = message_id
        self.submission_id = submission_id  # FK submissions.id
        self.user_id = user_id  # FK users.id
        self.jump_url = jump_url
