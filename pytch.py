"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: pytch.py
LAST_SYNC: 2026-08-02T01:12:58Z
[/DNA_TAG]
"""
#!/usr/bin/env python3
"""
Pytch - Pitch Generation & Outreach Automation Engine
The "I Fucking Can't" Bypass System for developers who ship code but not companies

Usage:
    python pytch.py --init                    # Initialize database
    python pytch.py --send-outreach           # Send pending outreach emails
    python pytch.py --metrics                 # Show campaign metrics
"""

import argparse
import sqlite3
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from pathlib import Path

# Configuration
DB_PATH = Path(__file__).parent / "pytch" / "pytch.db"
EMAIL = os.getenv("PYTCH_EMAIL")
EMAIL_PASSWORD = os.getenv("PYTCH_EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("PYTCH_SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("PYTCH_SMTP_PORT", 587))


class PytchEngine:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()
    
    def _get_connection(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_db(self):
        """Initialize database tables if they don't exist"""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS campaigns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    wrapper_name TEXT,
                    target_persona TEXT,
                    status TEXT DEFAULT 'active',
                    emails_sent INTEGER DEFAULT 0,
                    replies INTEGER DEFAULT 0,
                    demos_booked INTEGER DEFAULT 0,
                    deals_closed INTEGER DEFAULT 0,
                    revenue INTEGER DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company TEXT,
                    contact_name TEXT,
                    email TEXT UNIQUE,
                    source TEXT,
                    industry TEXT,
                    pain_points TEXT,
                    status TEXT DEFAULT 'new',
                    priority INTEGER DEFAULT 50,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS outreach (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lead_id INTEGER,
                    campaign TEXT,
                    subject TEXT,
                    body TEXT,
                    sent_at DATETIME,
                    opened BOOLEAN DEFAULT 0,
                    replied BOOLEAN DEFAULT 0,
                    reply_content TEXT,
                    next_followup DATETIME,
                    FOREIGN KEY (lead_id) REFERENCES leads(id)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS deals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lead_id INTEGER,
                    amount INTEGER,
                    stage TEXT,
                    status TEXT DEFAULT 'negotiating',
                    closed_at DATETIME,
                    FOREIGN KEY (lead_id) REFERENCES leads(id)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE,
                    emails_sent INTEGER DEFAULT 0,
                    emails_opened INTEGER DEFAULT 0,
                    replies_received INTEGER DEFAULT 0,
                    demos_booked INTEGER DEFAULT 0,
                    deals_closed INTEGER DEFAULT 0,
                    revenue_generated INTEGER DEFAULT 0
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS social_posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    platform TEXT,
                    content TEXT,
                    media_url TEXT,
                    scheduled_for DATETIME,
                    posted_at DATETIME,
                    engagement_count INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'scheduled'
                )
            """)
            conn.commit()
    
    def init(self):
        """Initialize the Pytch database"""
        print("Initializing Pytch database...")
        self._init_db()
        
        # Create default campaign if none exists
        with self._get_connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM campaigns").fetchone()[0]
            if count == 0:
                conn.execute(
                    "INSERT INTO campaigns (wrapper_name, target_persona, status) VALUES (?, ?, ?)",
                    ("default", "General", "active")
                )
                conn.commit()
                print("✓ Default campaign created")
        
        print("✓ Pytch database initialized")
        return True
    
    def send_pending_outreach(self, limit=10):
        """Send pending outreach emails"""
        if not EMAIL or not EMAIL_PASSWORD:
            print("ERROR: Email credentials not set")
            print("Set PYTCH_EMAIL and PYTCH_EMAIL_PASSWORD environment variables")
            return False
        
        with self._get_connection() as conn:
            # Get pending outreach (not sent or needs followup)
            cursor = conn.execute("""
                SELECT o.id, o.lead_id, o.campaign, o.subject, o.body, 
                       l.email, l.contact_name, l.company
                FROM outreach o
                JOIN leads l ON o.lead_id = l.id
                WHERE o.sent_at IS NULL
                ORDER BY l.priority DESC, o.id
                LIMIT ?
            """, (limit,))
            
            sent_count = 0
            for row in cursor:
                try:
                    # Send email
                    msg = MIMEText(row['body'])
                    msg['Subject'] = row['subject']
                    msg['From'] = EMAIL
                    msg['To'] = row['email']
                    
                    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                        server.starttls()
                        server.login(EMAIL, EMAIL_PASSWORD)
                        server.send_message(msg)
                    
                    # Mark as sent
                    conn.execute(
                        "UPDATE outreach SET sent_at = ?, next_followup = ? WHERE id = ?",
                        (datetime.now().isoformat(), 
                         datetime.now().isoformat(),  # Set followup for tomorrow
                         row['id'])
                    )
                    
                    # Update metrics
                    conn.execute(
                        "UPDATE campaigns SET emails_sent = emails_sent + 1 WHERE wrapper_name = ?",
                        (row['campaign'],)
                    )
                    
                    sent_count += 1
                    print(f"✓ Sent to {row['contact_name']} at {row['company']} ({row['email']})")
                    
                except Exception as e:
                    print(f"✗ Failed to send to {row['email']}: {e}")
            
            conn.commit()
            print(f"Sent {sent_count} outreach emails")
            return sent_count > 0
    
    def show_metrics(self):
        """Display campaign metrics"""
        with self._get_connection() as conn:
            # Overall metrics
            total_leads = conn.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
            total_campaigns = conn.execute("SELECT COUNT(*) FROM campaigns").fetchone()[0]
            total_outreach = conn.execute("SELECT COUNT(*) FROM outreach").fetchone()[0]
            total_sent = conn.execute("SELECT COUNT(*) FROM outreach WHERE sent_at IS NOT NULL").fetchone()[0]
            total_replies = conn.execute("SELECT COUNT(*) FROM outreach WHERE replied = 1").fetchone()[0]
            total_deals = conn.execute("SELECT COUNT(*) FROM deals").fetchone()[0]
            total_revenue = conn.execute("SELECT SUM(deal_value) FROM deals WHERE stage = 'closed'").fetchone()[0] or 0
            
            print("\n" + "="*60)
            print("PYTCH METRICS DASHBOARD")
            print("="*60)
            print(f"\n📊 OVERVIEW")
            print(f"  Campaigns: {total_campaigns}")
            print(f"  Leads: {total_leads}")
            print(f"  Outreach: {total_outreach} ({total_sent} sent)")
            print(f"  Replies: {total_replies}")
            print(f"  Deals: {total_deals}")
            print(f"  Revenue: ${total_revenue:,.0f}")
            
            # Campaign breakdown
            print(f"\n📈 CAMPAIGN PERFORMANCE")
            campaigns = conn.execute(
                "SELECT wrapper_name, emails_sent, replies, demos_booked, deals_closed, revenue FROM campaigns"
            ).fetchall()
            
            for camp in campaigns:
                print(f"\n  {camp['wrapper_name']}:")
                print(f"    Emails sent: {camp['emails_sent']}")
                print(f"    Replies: {camp['replies']}")
                print(f"    Demos booked: {camp['demos_booked']}")
                print(f"    Deals closed: {camp['deals_closed']}")
                print(f"    Revenue: ${camp['revenue']:,.0f}")
            
            # Recent activity
            print(f"\n📝 RECENT ACTIVITY")
            recent = conn.execute(
                "SELECT l.company, l.contact_name, o.subject, o.sent_at FROM outreach o JOIN leads l ON o.lead_id = l.id WHERE o.sent_at IS NOT NULL ORDER BY o.sent_at DESC LIMIT 5"
            ).fetchall()
            
            for row in recent:
                sent_date = row['sent_at'][:10] if row['sent_at'] else 'Not sent'
                print(f"  {sent_date}: {row['company']} - {row['subject']}")
            
            print("="*60 + "\n")
            return True


def main():
    parser = argparse.ArgumentParser(description='Pytch - Pitch Generation & Outreach Automation')
    parser.add_argument('--init', action='store_true', help='Initialize database')
    parser.add_argument('--send-outreach', action='store_true', help='Send pending outreach emails')
    parser.add_argument('--metrics', action='store_true', help='Show campaign metrics')
    
    args = parser.parse_args()
    
    engine = PytchEngine()
    
    if args.init:
        engine.init()
    elif args.send_outreach:
        engine.send_pending_outreach()
    elif args.metrics:
        engine.show_metrics()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
