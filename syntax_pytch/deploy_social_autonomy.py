"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: deploy_social_autonomy.py
LAST_SYNC: 2026-08-02T01:13:33Z
[/DNA_TAG]
"""
#!/usr/bin/env python3
import sys
import os
import json
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from pytch_modules.social_autonomy import SocialAutonomy
    print("✅ Social autonomy module loaded!")
except ImportError:
    print("❌ Social module missing - creating minimal version...")
    # Fallback class
    class SocialAutonomy:
        def generate_30_day_calendar(self):
            return [{'day': 1, 'content': 'Fallback content - check module installation'}]

def main():
    print("""
    🤖 P Y T C H   S O C I A L   D E P L O Y M E N T
    ===============================================
    """)
    
    social = SocialAutonomy()
    
    print("📅 GENERATING 30-DAY CONTENT CALENDAR...")
    calendar = social.generate_30_day_calendar()
    
    print("💼 CREATING FIVERR GIG TEMPLATES...")
    gigs = social.generate_fiverr_gigs()
    
    print("🎯 GENERATING AD COPY...")
    facebook_ad = social.generate_ad_copy('facebook')
    twitter_ad = social.generate_ad_copy('twitter')
    
    # Save everything to files
    with open('social_calendar.json', 'w') as f:
        json.dump(calendar, f, indent=2)
    
    with open('fiverr_gigs.json', 'w') as f:
        json.dump(gigs, f, indent=2)
    
    print(f"✅ Generated {len(calendar)} social media posts")
    print(f"✅ Created {len(gigs)} Fiverr gig templates")
    print(f"✅ Prepared ad copy for Facebook & Twitter")
    print("")
    print("📁 Files saved:")
    print("   - social_calendar.json (30 days of content)")
    print("   - fiverr_gigs.json (ready-to-use gig templates)")
    print("")
    print("🚀 NEXT STEPS:")
    print("1. Create accounts from ACCOUNT_SETUP_CHECKLIST.md")
    print("2. Use the generated files to populate your platforms")
    print("3. Run daily: python3 post_daily_content.py")
    print("")
    print("🎯 Remember: Consistency beats perfection!")
    print("   Post daily, engage with comments, and watch the leads roll in.")

if __name__ == "__main__":
    main()
