# Discord Vouch Bot

A simple Discord bot built with Disnake that allows server members to vouch for each other, leaving positive or negative feedback. The bot records each vouch in a SQLite database and provides a profile with reputation details on request.

## Features

- **Vouching System**: Members can leave positive or negative feedback on each other with optional comments.
- **Reputation Profile**: Each member has a profile showing their reputation score, positive and negative votes, and all associated comments.
- **Database Persistence**: Vouches are saved in a SQLite database for data persistence across bot restarts.
  
## Prerequisites

- Python 3.11+
- [Disnake](https://docs.disnake.dev/en/latest/)
- [Dotenv](https://pypi.org/project/python-dotenv/) for environment variables

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/discord-vouch-bot.git
    cd discord-vouch-bot
    ```

2. **Install required libraries**:
    You can install the required libraries by using the `requirements.txt` file provided:
    ```bash
    pip install -r requirements.txt
    ```

3. **Setup environment variables**:

   Create a `.env` file in the root directory and add your Discord bot token and the channel ID for logging vouches.

    ```plaintext
    TOKEN=your_discord_bot_token
    VOUCH_LOG_CHANNEL_ID=your_vouch_log_channel_id
    ```

4. **Run the bot**:
    ```bash
    python bot.py
    ```

## Commands

### `/vouch @member +/- comment`
Allows a member to leave a vouch for another member with a positive (+) or negative (-) vote, and an optional comment.

Example:
```plaintext
/vouch @JohnDoe + Great collaborator!
```

- **Arguments**:
  - `@member`: Mention the member to vouch for.
  - `+ / -`: Specify whether the vote is positive or negative.
  - `comment`: (Optional) Additional feedback about the member.

### `/profile @member`
Displays the reputation profile of a specified member, including their reputation score, positive/negative votes, and comments.

Example:
```plaintext
/profile @JohnDoe
```

## Project Structure

- **bot.py**: Main bot file containing commands and bot setup.
- **vouch_db.sqlite**: SQLite database file used to store all vouches.
- **.env**: Environment file holding sensitive information (like your bot token).
- **requirements.txt**: File listing all required Python packages for the bot.

## Contributing

If you'd like to contribute, feel free to fork the repository, make changes, and submit a pull request. Please make sure to update tests as appropriate.

## License

MIT License

