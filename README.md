# GroupCritter (for LMY Patreon)

This is a discord bot that will assist with doing group crits as well as tracking feedback in the LMY Patreon channel `#group-crit-submissions`.

GroupCritter lets users keep track of their own submissions and feedback they have recieved and given. Anytime a submission is replied to using Discord's "reply" option, GroupCritter will count that as feedback. GroupCritter will also post milestones in the `#general` chat (eg. User1 has given feedback for 20 group crit submissions! 🎉)

Commands:

- `!add <text>` - adds a new submission to the group crit queue
- `!count` - counts the number of submissions currently in the queue
- `!check` - lists all of your submissions and all feedback recieved
- `!crit random` - sends you a random submission from the queue to critique
- `!crit next` - sends you the next submission from the the queue to critique (does not shift queue position)
- `!level` - checks your crit level (how much feedback you have given)
- Note on the `!crit` commands: they will always send you submissions you haven't already given feedback to

Admin Commands:

- `!next` - moves the queue up one spot and displays a link to the submission
- `!feedback` - shows a list of all feedback given to the current submission

TinyDB Database Structure:
(under development)

```
submissions
- id
- user_id
- jump_url
- created_at

feedback
- id
- submission_id
- user_id
- jump_url

crit_stats
- user_id
- completed_crits
- queue_pos

completed_crits
- user_id
- submission_id
```
