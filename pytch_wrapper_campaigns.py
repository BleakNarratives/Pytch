"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: pytch_wrapper_campaigns.py
LAST_SYNC: 2026-08-02T01:12:58Z
[/DNA_TAG]
"""
#!/usr/bin/env python3
"""
Pytch Wrapper Campaigns Manager
Manage product wrappers and generate targeted pitch campaigns

Usage:
    python pytch_wrapper_campaigns.py --list-wrappers       # List all wrappers
    python pytch_wrapper_campaigns.py --create-campaigns    # Create campaigns for ready products
    python pytch_wrapper_campaigns.py --generate-pitch WRAPPER --persona PERSONA
    python pytch_wrapper_campaigns.py --prioritize           # Show priority ranking
"""

import argparse
import sqlite3
import json
from pathlib import Path
from datetime import datetime

# Configuration
DB_PATH = Path(__file__).parent / "pytch" / "pytch.db"
WRAPPERS_DIR = Path(__file__).parent / "syntax_pytch" / "src" / "pytch_modules"


class WrapperCampaignManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.wrappers_dir = WRAPPERS_DIR
    
    def _get_connection(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn
    
    def _get_wrappers(self):
        """Get list of available wrapper modules"""
        if not self.wrappers_dir.exists():
            return []
        
        wrappers = []
        for py_file in self.wrappers_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue
            wrappers.append(py_file.stem)
        return sorted(wrappers)
    
    def _load_wrapper_config(self, wrapper_name):
        """Load wrapper configuration"""
        # Try to get info from the wrapper module
        try:
            import importlib.util
            module_path = self.wrappers_dir / f"{wrapper_name}.py"
            spec = importlib.util.spec_from_file_location(wrapper_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Extract docstring as description
            description = getattr(module, "__doc__", "") or ""
            if description:
                description = description.strip().split("\n")[0]
            
            return {
                "name": wrapper_name,
                "description": description,
                "module": module
            }
        except Exception as e:
            return {
                "name": wrapper_name,
                "description": f"Wrapper module: {wrapper_name}",
                "error": str(e)
            }
    
    def list_wrappers(self):
        """List all available wrapper modules"""
        wrappers = self._get_wrappers()
        
        print("\n" + "="*60)
        print("AVAILABLE PYTCH WRAPPERS")
        print("="*60)
        
        if not wrappers:
            print("No wrappers found. Check syntax_pytch/src/pytch_modules/")
            return False
        
        for i, wrapper in enumerate(wrappers, 1):
            config = self._load_wrapper_config(wrapper)
            print(f"\n{i}. {wrapper}")
            print(f"   {config.get('description', 'No description')}")
        
        print(f"\nTotal: {len(wrappers)} wrappers")
        print("="*60 + "\n")
        return True
    
    def create_campaigns(self):
        """Create campaigns for all ready wrappers"""
        wrappers = self._get_wrappers()
        
        print("\n" + "="*60)
        print("CREATING CAMPAIGNS FOR ALL WRAPPERS")
        print("="*60)
        
        created_count = 0
        for wrapper in wrappers:
            try:
                # Check if campaign already exists
                with self._get_connection() as conn:
                    existing = conn.execute(
                        "SELECT id FROM campaigns WHERE wrapper_name = ?",
                        (wrapper,)
                    ).fetchone()
                    
                    if existing:
                        print(f"✗ Campaign already exists for: {wrapper}")
                        continue
                    
                    # Create new campaign
                    conn.execute(
                        "INSERT INTO campaigns (wrapper_name, target_persona, status, created_at) VALUES (?, ?, ?, ?)",
                        (wrapper, "General", "active", datetime.now().isoformat())
                    )
                    conn.commit()
                    created_count += 1
                    print(f"✓ Created campaign for: {wrapper}")
            except Exception as e:
                print(f"✗ Error creating campaign for {wrapper}: {e}")
        
        print(f"\nCreated {created_count} new campaigns")
        print("="*60 + "\n")
        return created_count > 0
    
    def generate_pitch(self, wrapper_name, persona=None):
        """Generate a pitch for a specific wrapper and persona"""
        wrapper_config = self._load_wrapper_config(wrapper_name)
        
        if not wrapper_config:
            print(f"Error: Wrapper '{wrapper_name}' not found")
            return False
        
        # Generate pitch based on wrapper type
        pitches = {
            "brander": {
                "subject": "Your Brand, Weaponized",
                "body": """Hey {name},

We noticed {company} is {pain_point}.

I built {wrapper_name} - it transforms your brand identity into a competitive weapon.

The result: 300% more memorable customer touchpoints and 2x engagement.

Here's a 2-minute demo: {demo_link}

Worth a look?

{pytch_signature}

P.S. We're booking demos next week - limited slots available."""
            },
            "deck_matic": {
                "subject": "Pitch Decks That Close Deals",
                "body": """Hey {name},

Struggling with pitch decks that don't convert?

I built {wrapper_name} - an AI-powered pitch deck generator that creates investor-ready decks in minutes.

The result: 40% higher demo booking rates and 3x faster funding rounds.

Here's a 2-minute demo: {demo_link}

Worth a look?

{pytch_signature}"""
            },
            "deploy_butler": {
                "subject": "Deployment So Easy It's Unfair",
                "body": """Hey {name},

Deployment headaches killing your velocity?

I built {wrapper_name} - one-command deployment to any platform.

The result: 10x faster deployments and zero DevOps stress.

Here's a 2-minute demo: {demo_link}

Worth a look?

{pytch_signature}"""
            }
        }
        
        # Default pitch template
        pitch_template = pitches.get(wrapper_name, {
            "subject": f"Introducing {wrapper_name}",
            "body": f"""Hey {{name}},

I built {wrapper_name} - {wrapper_config.get('description', 'a powerful solution')}.

The result: Better outcomes with less effort.

Here's a 2-minute demo: {{demo_link}}

Worth a look?

{{pytch_signature}}

P.S. Limited time offer - early adopter pricing available."""
        })
        
        # Customize for persona if provided
        if persona:
            pitch_template["subject"] = f"{pitch_template['subject']} for {persona}"
            pitch_template["body"] = pitch_template["body"].replace(
                "I built", f"I built (perfect for {persona})"
            )
        
        # Create sample lead and outreach
        with self._get_connection() as conn:
            # Reuse the existing sample lead if present — leads.email is
            # UNIQUE and hardcoding the same address made every generation
            # after the first crash with IntegrityError.
            lead = conn.execute(
                "SELECT id FROM leads WHERE email = ?",
                ("decision@example.com",)
            ).fetchone()
            if lead:
                lead_id = lead["id"]
            else:
                lead_id = conn.execute(
                    "INSERT INTO leads (company, contact_name, email, source, industry, pain_points, priority) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    ("Example Company", "Decision Maker", "decision@example.com", "pytch", "Technology", "Needs better outreach", 100)
                ).lastrowid
            
            # Insert outreach with generated pitch
            conn.execute(
                "INSERT INTO outreach (lead_id, campaign, subject, body, sent_at, next_followup) VALUES (?, ?, ?, ?, ?, ?)",
                (lead_id, wrapper_name, pitch_template["subject"], pitch_template["body"], None, datetime.now().isoformat())
            )
            
            conn.commit()
            print(f"\n✓ Generated pitch for: {wrapper_name}")
            print(f"  Subject: {pitch_template['subject']}")
            print(f"  Campaign: {wrapper_name}")
            print(f"  Target: {persona or 'General'}")
            print(f"\n  Sample pitch preview:")
            print(f"  {pitch_template['body'][:200]}...")
        
        return True
    
    def prioritize(self):
        """Show priority ranking of all campaigns"""
        with self._get_connection() as conn:
            campaigns = conn.execute("""
                SELECT wrapper_name, target_persona, status, 
                       emails_sent, replies, demos_booked, deals_closed, revenue
                FROM campaigns
                ORDER BY 
                    CASE status 
                        WHEN 'active' THEN 1 
                        WHEN 'paused' THEN 2 
                        ELSE 3 
                    END,
                    revenue DESC,
                    deals_closed DESC
            """).fetchall()
            
            print("\n" + "="*80)
            print("CAMPAIGN PRIORITY RANKING")
            print("="*80)
            print(f"\n{'Rank':<6} {'Campaign':<25} {'Status':<12} {'Emails':<8} {'Replies':<8} {'Deals':<8} {'Revenue':<12}")
            print("-"*80)
            
            for i, camp in enumerate(campaigns, 1):
                print(f"{i:<6} {camp['wrapper_name']:<25} {camp['status']:<12} "
                      f"{camp['emails_sent']:<8} {camp['replies']:<8} {camp['deals_closed']:<8} "
                      f"${camp['revenue']:>10,.0f}")
            
            print("="*80)
            
            # Recommendations
            active_count = sum(1 for c in campaigns if c['status'] == 'active')
            paused_count = sum(1 for c in campaigns if c['status'] == 'paused')
            
            print(f"\n💡 RECOMMENDATIONS:")
            if active_count == 0:
                print("  → Create campaigns for your wrappers using --create-campaigns")
            else:
                print(f"  → {active_count} active campaigns - keep the momentum going!")
                if paused_count > 0:
                    print(f"  → {paused_count} paused campaigns - consider resuming")
            
            print("="*80 + "\n")
            return True


def main():
    parser = argparse.ArgumentParser(
        description='Pytch Wrapper Campaigns Manager - Generate and manage pitch campaigns'
    )
    parser.add_argument('--list-wrappers', action='store_true', help='List all available wrappers')
    parser.add_argument('--create-campaigns', action='store_true', help='Create campaigns for all wrappers')
    parser.add_argument('--generate-pitch', nargs='+', metavar=('WRAPPER', 'PERSONA'),
                        help='Generate a pitch for a wrapper (optional: --persona PERSONA)')
    parser.add_argument('--prioritize', action='store_true', help='Show priority ranking')
    
    args = parser.parse_args()
    
    manager = WrapperCampaignManager()
    
    if args.list_wrappers:
        manager.list_wrappers()
    elif args.create_campaigns:
        manager.create_campaigns()
    elif args.generate_pitch:
        wrapper_name = args.generate_pitch[0]
        persona = args.generate_pitch[1] if len(args.generate_pitch) > 1 else None
        manager.generate_pitch(wrapper_name, persona)
    elif args.prioritize:
        manager.prioritize()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
