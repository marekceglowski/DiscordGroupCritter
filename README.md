# GroupCritter (for LMY Patreon)

This is a discord bot that will assist with doing group crits as well as tracking feedback in the LMY Patreon channel `#group-crit-submissions`.

GroupCritter does the following:
- lets user keep track of submissions and feedback given
- post milestone announcements in the `#general` chat (eg. User1 has given feedback for 20 group crit submissions! 🎉)
- award ranks and medals for reaching milestones
- lets the admin (@la_meme_young) manage a livestream crit queue

Commands:

- `!add <text>` - adds a new submission to the group crit queue
- `!count` - counts the number of submissions currently in the queue
- `!crit random` - sends you a random submission from the queue to critique (always returns a submission you haven't reviewed)
- `!crit next` - sends you the next submission from the the queue to critique (doesn't shift the queue position, useful if you want to do them in order)
- `!skipadd <text>` - adds a new submission with status 'skip' so it's not in the livestream queue
- `!stats` - displays your level and how much feedback you have given
- `!submissions` - displays your crit submissions and feedback received

Admin Commands:

- `!next` - moves the queue up one spot and displays a link to the submission
- `!feedback` - shows a list of all feedback given to the current submission

Database Structure can be found here:

https://github.com/marekceglowski/DiscordGroupCritter/blob/master/DB_INFO.md

Medal Ranking rules and commands can be found here:

https://github.com/marekceglowski/DiscordGroupCritter/blob/master/medals/MEDALS.md
