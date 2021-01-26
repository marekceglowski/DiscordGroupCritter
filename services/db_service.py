import datetime
from pymongo import MongoClient
from models.submission import Submission
from models.user import User
from models.rank import Rank

client = MongoClient('mongodb://localhost:27017')
db = client['lmy']


# General #

def get_max_id(db_table):
    return db_table.find().sort({id: -1}).limit(1)


# Submissions #

def add_submission(message):
    submission = Submission(
        get_max_id(db.submissions) + 1,
        message.id,
        message.author,
        message.content,
        message.jump_url,
        datetime.now()
    )

    db.submissions.insert_one(submission)
    return submission


def add_submission_obj(submission):
    if isinstance(submission, Submission):
        db.submissions.insert_one(submission)
    return submission


def find_submissions_by_user_id(user_id):
    submissions = db.submissions.find({'user_id': user_id}) # find() returns a cursor
    if submissions.count() < 1:
        return None
    else:
        return list(submissions)


# Users #

def user_exists(discord_user_id):
    user = db.users.find_one({'discord_user_id': discord_user_id})
    if user is None:
        return False
    else:
        return True


def find_user_by_id(discord_user_id):
    return db.users.find_one({'discord_user_id': discord_user_id})


def add_new_user(discord_user_id):
    user = user_exists(discord_user_id)
    if user is not None:
        return user
    user = User(
        get_max_id(db.users) + 1,
        discord_user_id,
        0,
        1,
        1  # Lowest level rank
    )
    return user


# Ranks #

def get_rank_by_name(name):
    rank = db.ranks.find_one({'rank_name': name})
    if rank is None:
        return None
    return rank


# Feedbacks #

def get_feedbacks_received(discord_user_id):
    user = find_user_by_id(discord_user_id)
    if user is None:
        user = add_new_user(discord_user_id)
    submissions = find_submissions_by_user_id(user.id)
    if submissions is None:
        return None
    feedbacks = []
    for submission in submissions:
        sub_feedbacks = db.feedbacks.find({'submission_id': submission.id})
        for sub_feedback in sub_feedbacks:
            feedbacks.append(sub_feedback)
    return feedbacks
