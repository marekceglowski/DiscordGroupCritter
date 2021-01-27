# This is a helper model that contains relevant info connected to a submission

class SubmissionInfo:
    def __init__(self, submission, feedbacks, queue_pos):
        self.id = id
        self.submission = submission  # Submission() object
        self.feedbacks = feedbacks  # list(Feedback() object)
        self.queue_pos = queue_pos  # int
