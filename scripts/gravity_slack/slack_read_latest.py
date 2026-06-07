import os
import json
import urllib.request
import urllib.error

# Load optional dotenv if exists (safely ignore if not installed)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def get_slack_token():
    token = os.environ.get("SLACK_BOT_TOKEN")
    if not token:
        print("ERROR: SLACK_BOT_TOKEN environment variable is missing. Failing closed.")
        exit(1)
    return token

def read_latest_messages(channel_id="C0B7HJLTDCZ", limit=5):
    token = get_slack_token()
    
    url = f"https://slack.com/api/conversations.history?channel={channel_id}&limit={limit}"
    
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-type", "application/json")
    
    try:
        with urllib.request.urlopen(req) as response:
            resp_data = response.read().decode('utf-8')
            parsed = json.loads(resp_data)
            
            if not parsed.get('ok'):
                print(f"Slack API Error: {parsed.get('error')}")
                # Do not log raw response to prevent accidental token/secret leakage
                exit(1)
                
            messages = parsed.get("messages", [])
            print(f"--- Latest {len(messages)} messages in {channel_id} ---")
            for msg in messages:
                # Basic text extraction, ensuring no raw market data dumping
                user = msg.get("user", "UnknownUser")
                text = msg.get("text", "")
                print(f"[{user}]: {text}")
                
    except urllib.error.URLError as e:
        print("Network error connecting to Slack API. Failing closed.")
        exit(1)
    except Exception as e:
        print("An unexpected error occurred during Slack read. Failing closed.")
        exit(1)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Read latest Gravity Slack instructions.")
    parser.add_argument("--channel", default="C0B7HJLTDCZ", help="Target Slack Channel ID")
    parser.add_argument("--limit", type=int, default=5, help="Number of messages to retrieve")
    args = parser.parse_args()
    
    read_latest_messages(args.channel, args.limit)
