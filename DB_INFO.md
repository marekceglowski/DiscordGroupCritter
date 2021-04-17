# MongoDB Database Structure:

Note: PK is treated as a primary key and FK is treated as a foreign key.

## submissions
- message_id [PK] -- message id from discord
- user_id [FK] -- user id from discord
- jump_url -- link to go to message
- created_at
- status -- queue status: options are 'pending', 'complete', or 'skip'

## users
- user_id [PK] -- user id from discord
- rank_id [FK] -- default: None
- dm_on_feedback -- default: True

## ranks
- role_id [PK] -- role id from discord
- rank_name
- feedback_count -- number of feedbacks to reach rank
- medal_code -- the medal emoji code (eg. :23:)

## feedbacks
- message_id [PK] -- message id from discord
- submission_id [FK] -- message id for the submission that was replied to
- user_id [FK] -- user id of the person that sent feedback
- received_user_id [FK] -- user id of the person that received feedback 
- jump_url
