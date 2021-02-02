
class Rank:
    def __init__(self, role_id, rank_name, feedback_count, medal_code):
        self.role_id = role_id  # PK - discord's role id
        self.rank_name = rank_name
        self.feedback_count = feedback_count
        self.medal_code = medal_code
