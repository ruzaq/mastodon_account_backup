#!/usr/bin/python

from mastodon import Mastodon, MastodonAPIError
import os
import configparser
import datetime
import argparse
import requests
from requests.exceptions import RequestException

# Command-line arguments setup
parser = argparse.ArgumentParser(description="Mastodon Backup Script")
parser.add_argument('-c', '--config', type=str, required=True, help='Path to the configuration file')
parser.add_argument('-l', '--limit', type=int, help='Limit the number of statuses to fetch (optional)')

# Process arguments
args = parser.parse_args()
config_file = args.config
limit = args.limit

# Load configuration from config.ini
config = configparser.ConfigParser()
try:
    config.read(config_file)
    api_base_url = config['mastodon']['api_base_url']
    access_token = config['mastodon']['access_token']
except KeyError:
    print("Error: Config file is missing required fields. Ensure 'api_base_url' and 'access_token' are present.")
    exit(1)

# Set up Mastodon API
try:
    mastodon = Mastodon(
        access_token=access_token,
        api_base_url=api_base_url
    )
except MastodonAPIError as e:
    print(f"Error initializing Mastodon API: {e}")
    exit(1)

# Get account username to use in the backup folder name
try:
    account_info = mastodon.account_verify_credentials()
    username = account_info['username']
except MastodonAPIError as e:
    print(f"Error verifying account credentials: {e}")
    exit(1)

# Get current date to use in the backup folder name
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Create the backup directory inside 'out/' folder with secure permissions
backup_dir = f'./out/mastodon_backup_{username}_{current_date}/'
try:
    os.makedirs(backup_dir, exist_ok=True)
    # Restricting access to the user (read and write access only for the user)
    os.chmod(backup_dir, 0o700)
except OSError as e:
    print(f"Error creating backup directory: {e}")
    exit(1)

# Backup summary
backup_summary = []

# Function for secure downloading of media files
def download_media(url, file_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check if the request was successful
        with open(file_path, 'wb') as media_file:
            for chunk in response.iter_content(chunk_size=8192):
                media_file.write(chunk)
        # Ensure file permissions are secure (read and write access only for the user)
        os.chmod(file_path, 0o600)
        print(f"Downloaded {file_path}")
    except RequestException as e:
        print(f"Error downloading {url}: {e}")
    except OSError as e:
        print(f"Error saving media file {file_path}: {e}")

# 1. Backup statuses (posts)
try:
    if limit:
        statuses = mastodon.account_statuses(mastodon.me(), limit=limit)
        print(f"Fetching the last {limit} statuses.")
    else:
        # Fetch all statuses without a limit
        statuses = []
        max_id = None
        while True:
            batch = mastodon.account_statuses(mastodon.me(), max_id=max_id)
            if not batch:
                break
            statuses.extend(batch)
            max_id = batch[-1]['id'] - 1
        print(f"Fetched all {len(statuses)} statuses.")

    status_file_path = os.path.join(backup_dir, 'statuses_backup.txt')
    with open(status_file_path, 'w') as f:
        for status in statuses:
            f.write(f"{status['created_at']}: {status['content']}\n")
    # Secure permissions for the backup file
    os.chmod(status_file_path, 0o600)
    backup_summary.append(f"Statuses: {len(statuses)} backed up")
except MastodonAPIError as e:
    print(f"Error backing up statuses: {e}")
except OSError as e:
    print(f"Error writing status backup file: {e}")

# 2. Backup followers
try:
    followers = mastodon.account_followers(mastodon.me())
    followers_file_path = os.path.join(backup_dir, 'followers_backup.txt')
    with open(followers_file_path, 'w') as f:
        for follower in followers:
            f.write(f"{follower['username']}\n")
    # Secure permissions for the backup file
    os.chmod(followers_file_path, 0o600)
    backup_summary.append(f"Followers: {len(followers)} backed up")
except MastodonAPIError as e:
    print(f"Error backing up followers: {e}")
except OSError as e:
    print(f"Error writing followers backup file: {e}")

# 3. Backup following accounts
try:
    following = mastodon.account_following(mastodon.me())
    following_file_path = os.path.join(backup_dir, 'following_backup.txt')
    with open(following_file_path, 'w') as f:
        for account in following:
            f.write(f"{account['username']}\n")
    # Secure permissions for the backup file
    os.chmod(following_file_path, 0o600)
    backup_summary.append(f"Following: {len(following)} backed up")
except MastodonAPIError as e:
    print(f"Error backing up following: {e}")
except OSError as e:
    print(f"Error writing following backup file: {e}")

# 4. Backup lists
try:
    lists = mastodon.lists()
    lists_file_path = os.path.join(backup_dir, 'lists_backup.txt')
    with open(lists_file_path, 'w') as f:
        for list_item in lists:
            f.write(f"{list_item['title']}\n")
    # Secure permissions for the backup file
    os.chmod(lists_file_path, 0o600)
    backup_summary.append(f"Lists: {len(lists)} backed up")
except MastodonAPIError as e:
    print(f"Error backing up lists: {e}")
except OSError as e:
    print(f"Error writing lists backup file: {e}")

# 5. Backup muted accounts
try:
    mutes = mastodon.mutes()
    mutes_file_path = os.path.join(backup_dir, 'mutes_backup.txt')
    with open(mutes_file_path, 'w') as f:
        for mute in mutes:
            f.write(f"{mute['username']}\n")
    # Secure permissions for the backup file
    os.chmod(mutes_file_path, 0o600)
    backup_summary.append(f"Mutes: {len(mutes)} backed up")
except MastodonAPIError as e:
    print(f"Error backing up mutes: {e}")
except OSError as e:
    print(f"Error writing mutes backup file: {e}")

# 6. Backup blocked accounts
try:
    blocks = mastodon.blocks()
    blocks_file_path = os.path.join(backup_dir, 'blocks_backup.txt')
    with open(blocks_file_path, 'w') as f:
        for block in blocks:
            f.write(f"{block['username']}\n")
    # Secure permissions for the backup file
    os.chmod(blocks_file_path, 0o600)
    backup_summary.append(f"Blocks: {len(blocks)} backed up")
except MastodonAPIError as e:
    print(f"Error backing up blocks: {e}")
except OSError as e:
    print(f"Error writing blocks backup file: {e}")

# 7. Backup domain blocks
try:
    domain_blocks = mastodon.domain_blocks()
    domain_blocks_file_path = os.path.join(backup_dir, 'domain_blocks_backup.txt')
    with open(domain_blocks_file_path, 'w') as f:
        for domain in domain_blocks:
            f.write(f"{domain}\n")
    # Secure permissions for the backup file
    os.chmod(domain_blocks_file_path, 0o600)
    backup_summary.append(f"Domain blocks: {len(domain_blocks)} backed up")
except MastodonAPIError as e:
    print(f"Error backing up domain blocks: {e}")
except OSError as e:
    print(f"Error writing domain blocks backup file: {e}")

# 8. Backup media attachments
attachments = []
for status in statuses:
    if status['media_attachments']:
        attachments.extend(status['media_attachments'])

for idx, attachment in enumerate(attachments):
    media_url = attachment['url']
    media_filename = f"media_{idx}.jpg"  # or the appropriate extension based on media type
    media_path = os.path.join(backup_dir, media_filename)

    download_media(media_url, media_path)

backup_summary.append(f"Media attachments: {len(attachments)} downloaded")

# 9. Backup bookmarks
try:
    bookmarks = mastodon.bookmarks()
    bookmarks_file_path = os.path.join(backup_dir, 'bookmarks_backup.txt')
    with open(bookmarks_file_path, 'w') as f:
        for bookmark in bookmarks:
            f.write(f"{bookmark['url']}: {bookmark['content']}\n")
    # Secure permissions for the backup file
    os.chmod(bookmarks_file_path, 0o600)
    backup_summary.append(f"Bookmarks: {len(bookmarks)} backed up")
except MastodonAPIError as e:
    print(f"Error backing up bookmarks: {e}")
except OSError as e:
    print(f"Error writing bookmarks backup file: {e}")

# Print summary
print(f"Backup for {username} completed and stored in {backup_dir}!")
print("Backup summary:")
for item in backup_summary:
    print(item)
