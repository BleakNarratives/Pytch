"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: post_daily_content.py
LAST_SYNC: 2026-08-02T01:13:33Z
[/DNA_TAG]
"""
#!/usr/bin/env python3
import json
import datetime

try:
    with open('social_calendar.json', 'r') as f:
        calendar = json.load(f)
    
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    print(f"📅 DAILY CONTENT FOR {today}")
    print("=" * 40)
    
    for post in calendar:
        if post['date'] == today:
            print(f"Platform: {post['platform'].upper()}")
            print(f"Type: {post['content_type']}")
            print(f"Content: {post['content']}")
            print(f"Hashtags: {' '.join(post['hashtags'])}")
            print("")
            print("📋 Copy-paste the above to your social media!")
            break
    else:
        print("No content scheduled for today. Check social_calendar.json")
        
except FileNotFoundError:
    print("❌ social_calendar.json not found. Run deploy_social_autonomy.py first")
