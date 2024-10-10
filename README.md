# Mastodon Account Backup Script

This Python script allows you to back up key data from your Mastodon account, including:

- **Statuses (Posts)**
- **Followers**
- **Following Accounts**
- **Lists**
- **Muted Accounts**
- **Blocked Accounts**
- **Domain Blocks**
- **Bookmarks**
- **Media Attachments**

The script uses the Mastodon API to fetch and store your account data locally for reference purposes.

## Features

- **Backup Posts**: Fetch all or a limited number of posts (statuses) from your account.
- **Backup Follows**: Backup the list of accounts you follow and those that follow you.
- **Backup Media**: Downloads media attachments from your posts.
- **Backup Privacy Settings**: Backs up mutes, blocks, and domain blocks.
- **Customizable**: Supports configurable limits for the number of posts to fetch.

## Requirements

Before you run the script, ensure you have the following installed:

- Python 3.x
- `Mastodon.py` library
- `requests` library

You can install the required Python libraries with:

```bash
pip install Mastodon.py requests
```

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/ruzaq/mastodon_account_backup.git
   cd mastodon_account_backup
   ```

2. Create a configuration file (`config.ini`) in the script directory with the following structure:

   ```ini
   [mastodon]
   api_base_url = https://your.instance
   access_token = your_access_token_here
   ```

   Replace `https://your.instance` with your Mastodon instance URL and `your_access_token_here` with your API token. You can generate an API token from your Mastodon account under `Settings` > `Development` > `New Application`.

## Usage

The script can be run with the following options:

```bash
./mastodon_backup.py -c config.ini [-l limit]
```

- `-c` or `--config`: Path to your configuration file (required).
- `-l` or `--limit`: Limit the number of statuses (posts) to fetch. If not provided, the script will fetch all statuses.

### Examples

1. **Backup all posts and account data**:

   ```bash
   ./mastodon_backup.py -c config.ini
   ```

   This command will fetch all statuses, followers, following accounts, lists, mutes, blocks, domain blocks, media attachments, and bookmarks.

2. **Backup only the last 100 posts**:

   ```bash
   ./mastodon_backup.py -c config.ini -l 100
   ```

   This command will fetch only the last 100 posts while still backing up followers, following, and other account data.

## Output

The script stores all backup data in the `out/` directory. The directory structure is as follows:

```
out/
    mastodon_backup_<username>_<YYYY-MM-DD>/
        statuses_backup.txt
        followers_backup.txt
        following_backup.txt
        lists_backup.txt
        mutes_backup.txt
        blocks_backup.txt
        domain_blocks_backup.txt
        bookmarks_backup.txt
        media_<index>.jpg
```

- **statuses_backup.txt**: Contains your posts (statuses).
- **followers_backup.txt**: Contains the usernames of your followers.
- **following_backup.txt**: Contains the usernames of accounts you follow.
- **lists_backup.txt**: Contains your Mastodon lists.
- **mutes_backup.txt**: Contains usernames of muted accounts.
- **blocks_backup.txt**: Contains usernames of blocked accounts.
- **domain_blocks_backup.txt**: Contains the domain names you have blocked.
- **bookmarks_backup.txt**: Contains URLs of bookmarked posts.
- **media**: Media files attached to your posts are downloaded and saved with sequential filenames.

## Notes

- The script fetches all available data from your account using the Mastodon API and stores it locally.
- Please note that this script is for backup purposes only. It cannot re-import data into Mastodon.
