import os
import json
import urllib.request
import urllib.error

# Load optional dotenv if exists
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

def post_completion_report(message, channel_id="C0B7HJLTDCZ"):
    token = get_slack_token()
    
    # Boundary: Ensure no large data dumps. Arbitrary safety limit on message length.
    if len(message) > 4000:
        print("ERROR: Message exceeds short report boundary (4000 chars). Failing closed to prevent data leaks.")
        exit(1)
        
    url = "https://slack.com/api/chat.postMessage"
    payload = {
        "channel": channel_id,
        "text": message
    }
    
    data = json.dumps(payload).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-type", "application/json; charset=utf-8")
    
    try:
        with urllib.request.urlopen(req) as response:
            resp_data = response.read().decode('utf-8')
            parsed = json.loads(resp_data)
            
            if not parsed.get('ok'):
                print(f"Slack API Error: {parsed.get('error')}")
                exit(1)
                
            print("Successfully posted report to Slack.")
            
    except urllib.error.URLError as e:
        print("Network error connecting to Slack API. Failing closed.")
        exit(1)
    except Exception as e:
        print("An unexpected error occurred during Slack post. Failing closed.")
        exit(1)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Post short Gravity status report to Slack.")
    parser.add_argument("--channel", default="C0B7HJLTDCZ", help="Target Slack Channel ID")
    parser.add_argument("--message", required=True, help="Short text status report")
    args = parser.parse_args()
    
    post_completion_report(args.message, args.channel)
