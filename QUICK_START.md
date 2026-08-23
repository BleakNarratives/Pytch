# Pytch Quick Start

## Setup (FIRST TIME)
```bash
# Set email credentials
export PYTCH_EMAIL="your@email.com"
export PYTCH_EMAIL_PASSWORD="your-app-password"

# Initialize database
python pytch.py --init
```

## Daily Commands

**See all wrappers:**
```bash
python pytch_wrapper_campaigns.py --list-wrappers
```

**Create campaigns for ready products:**
```bash
python pytch_wrapper_campaigns.py --create-campaigns
```

**Generate a pitch:**
```bash
python pytch_wrapper_campaigns.py --generate-pitch studio_ai \
  --persona "Music production schools"
```

**See priority ranking:**
```bash
python pytch_wrapper_campaigns.py --prioritize
```

**Send pending emails (WHEN YOU HAVE WIFI):**
```bash
python pytch.py --send-outreach
```

**Check metrics:**
```bash
python pytch.py --metrics
```

## Emergency: Quick Manual Pitch

If Pytch fails, write emails manually using this template:

**Subject:** [Product] - [One compelling benefit]

**Body:**
Hey [Name],

[Pattern interrupt - specific observation about their business]

I built [Product Name] - [what it does in 10 words].

The result: [Specific benefit with number]

Here's a 2-minute demo: [link]

Worth a look?

[Your name]

P.S. [Social proof or urgency]
