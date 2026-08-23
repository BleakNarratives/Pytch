"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: deck_matic.py
LAST_SYNC: 2026-08-02T01:13:34Z
[/DNA_TAG]
"""
"""
DeckMatic 5000 - Generates pitch decks while you procrastinate
"""
import json
from pathlib import Path

class DeckMatic5000:
    def __init__(self, project_path, brand_assets):
        self.project_path = Path(project_path)
        self.brand_assets = brand_assets
        self.decks_dir = self.project_path.parent / "exports" / "pitch_decks"
        self.decks_dir.mkdir(parents=True, exist_ok=True)
    
    def build_pitch_deck(self, audience="vc"):
        """Builds a complete pitch deck - ready for investor eyes"""
        print("📊 DeckMatic 5000: Building your billion-dollar pitch")
        
        deck_content = {
            "company_name": self.brand_assets["name"],
            "tagline": self.brand_assets["taglines"][0],
            "slides": self._generate_slides(audience)
        }
        
        # Save deck content
        deck_file = self.decks_dir / f"{self.brand_assets['name'].lower().replace(' ', '_')}_pitch_deck.json"
        with open(deck_file, 'w') as f:
            json.dump(deck_content, f, indent=2)
        
        # Create a simple text version for now (PPT generation would go here)
        text_deck = self.decks_dir / f"{self.brand_assets['name'].lower().replace(' ', '_')}_pitch.txt"
        with open(text_deck, 'w') as f:
            f.write(self._generate_text_deck(deck_content))
        
        print(f"✅ Pitch deck created: {text_deck}")
        return str(text_deck)
    
    def _generate_slides(self, audience):
        """Generate the actual slide content"""
        slides = []
        
        # Slide 1: Title
        slides.append({
            "title": self.brand_assets["name"],
            "content": self.brand_assets["taglines"][0],
            "type": "title"
        })
        
        # Slide 2: Problem
        slides.append({
            "title": "The Problem",
            "content": "Developers are drowning in AI conversations and lost code snippets. Valuable insights disappear into chat history.",
            "type": "problem"
        })
        
        # Slide 3: Solution
        slides.append({
            "title": "Our Solution",
            "content": f"{self.brand_assets['name']} automatically captures, organizes, and weaponizes AI-generated code. From conversation to executable knowledge in seconds.",
            "type": "solution"
        })
        
        # Slide 4: Market Size
        slides.append({
            "title": "Market Opportunity",
            "content": "$47B Total Addressable Market in developer tools and AI productivity. 30M+ developers worldwide experiencing AI conversation fatigue.",
            "type": "market"
        })
        
        # Slide 5: Business Model
        slides.append({
            "title": "Business Model",
            "content": "Freemium SaaS: Free for individuals, $15/month for pros, $50/seat for teams. Enterprise contracts starting at $50k/year.",
            "type": "business_model"
        })
        
        # Slide 6: The Ask
        slides.append({
            "title": "The Opportunity",
            "content": "Seeking $1.5M for 15% to scale engineering, grow community, and capture the AI productivity tooling market.",
            "type": "ask"
        })
        
        return slides
    
    def _generate_text_deck(self, deck_content):
        """Generate a text version of the pitch deck"""
        text = f"PITCH DECK: {deck_content['company_name']}\n"
        text += "=" * 50 + "\n\n"
        
        for i, slide in enumerate(deck_content['slides']):
            text += f"Slide {i+1}: {slide['title']}\n"
            text += f"{slide['content']}\n\n"
        
        text += "END OF DECK - Now go raise some money! 🚀"
        return text
