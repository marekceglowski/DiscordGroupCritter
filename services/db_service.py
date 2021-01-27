import datetime
from pymongo import MongoClient
from models.submission import Submission
from models.user import User
from models.rank import Rank
from models.submission_info import SubmissionInfo

client = MongoClient('mongodb://localhost:27017')
db = client['lmy']


# General #

def get_max_id(db_table):
    return db_table.find().sort({id: -1}).limit(1)


# Submissions #

def add_submission(message, status):
    if status is None:
        status = 'pending'

    submission = Submission(
        get_max_id(db.submissions) + 1,
        message.id,
        message.author,
        message.content,
        message.jump_url,
        datetime.now(),
        status
    )

    db.submissions.insert_one(submission)
    return submission


def add_submission_obj(submission):
    if isinstance(submission, Submission):
        db.submissions.insert_one(submission)
    return submission


def get_submissions_by_user_id(user_id):
    submissions = db.submissions.find({'user_id': user_id})  # find() returns a cursor
    if submissions.count() < 1:
        return None
    else:
        return list(submissions)


def get_ordered_queue_submissions():
    submissions = db.submissions.find({'status': 'pending'}).sort({id: -1})
    if submissions.count < 1:
        return None
    else:
        return list(submissions)


def get_submission_position_in_queue(submission_id):
    submission = db.submissions.find_one({'id': submission_id})
    if submission is None:
        return -1
    else:
        queue_subs = get_ordered_queue_submissions()
        if queue_subs is None:
            return -1
        else:
            for idx, item in enumerate(queue_subs):
                if submission.id == item.id:
                    return idx
            return -1


def get_submission_positions_in_queue_multi(submission_list):
    subs_and_positions = []  # list of tuples (submission, queue_pos)

    queue_subs = get_ordered_queue_submissions()
    if queue_subs is None:
        return None
    else:
        for idx, item in enumerate(queue_subs):
            current_pos = -1
            for submission in submission_list:
                if submission.id == item.id:
                    current_pos = idx
            subs_and_positions.append((submission, current_pos))
        return subs_and_positions


def get_submissions_with_info_by_user_id(user_id):
    user_sub_infos = []  # list(SubmissionInfo() obj)
    user_subs = get_submissions_by_user_id(user_id)
    user_subs_with_positions = get_submission_positions_in_queue_multi(user_subs)
    feedbacks = db.feedbacks.find({'received_user_id': user_id})

    for user_sub_with_pos in user_subs_with_positions:
        sub_feedbacks = []
        for fb in feedbacks:
            if fb.submission_id == user_sub_with_pos[0].id:
                sub_feedbacks.append(fb)
        user_sub_infos.append(SubmissionInfo(
            user_sub_with_pos[0],
            sub_feedbacks,
            user_sub_with_pos[1]
        ))
    return user_sub_infos


# Users #

def user_exists(discord_user_id):
    user = db.users.find_one({'discord_user_id': discord_user_id})
    if user is None:
        return False
    else:
        return True


def get_user_by_author_id(discord_user_id):
    user = db.users.find_one({'discord_user_id': discord_user_id})
    if user is None:
        user = add_new_user(discord_user_id)
    return user


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

def get_rank_by_user(user_id):
    user = db.users.find_one({'id': user_id})
    return db.ranks.find_one({'id': user.rank_id})


def get_rank_by_name(name):
    rank = db.ranks.find_one({'rank_name': name})
    if rank is None:
        return None
    return rank


# Feedbacks #

def get_feedbacks_received(user_id):
    feedbacks = db.feedbacks.find({'received_user_id': user_id})
    if feedbacks.count() < 1:
        return None
    else:
        return list(feedbacks)


def get_feedbacks_given(user_id):
    feedbacks = db.feedbacks.find({'user_id': user_id})  # returns a cursor
    if feedbacks.count() < 1:
        return None
    else:
        return list(feedbacks)
