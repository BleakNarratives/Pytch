"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: psych_engine.py
LAST_SYNC: 2026-08-02T01:13:34Z
[/DNA_TAG]
"""
import random

class PsychEngine:
    """Psychological profiling and influence tactics for business"""
    
    def __init__(self):
        self.archetypes = {
            'visionary': ['big picture', 'impact', 'legacy', 'change the world'],
            'operator': ['efficiency', 'metrics', 'scalability', 'process'],
            'money': ['roi', 'valuation', 'multiple', 'liquidity'],
            'hustler': ['growth', 'acquisition', 'virality', 'hacking']
        }
    
    def profile_investor(self, public_data):
        """Analyze investor psychology from available data"""
        # In reality, this would scrape LinkedIn, Twitter, podcast appearances
        traits = {
            'risk_tolerance': random.uniform(0.3, 0.9),
            'pattern_recognition': random.choice(['technical', 'market', 'team']),
            'decision_style': random.choice(['data_driven', 'gut_feeling', 'social_proof']),
            'hot_buttons': random.sample(['traction', 'team', 'technology', 'market_size'], 2)
        }
        return traits
    
    def generate_influence_strategy(self, profile, project_data):
        """Custom influence approach for each investor type"""
        if profile['risk_tolerance'] > 0.7:
            approach = "Go big: Emphasize massive market disruption and 100x potential"
        elif profile['decision_style'] == 'data_driven':
            approach = "Data first: Lead with metrics, traction, and clear milestones"
        else:
            approach = "Social proof: Highlight other investors, customer testimonials"
        
        return {
            'opening_line': self.custom_opening(profile),
            'key_arguments': self.prioritize_arguments(profile, project_data),
            'close_technique': self.select_close(profile),
            'follow_up_strategy': self.follow_up_cadence(profile)
        }
    
    def custom_opening(self, profile):
        openings = {
            'visionary': "I want to show you something that will change how we think about...",
            'operator': "The numbers here are unlike anything I've seen in this space...",
            'money': "The ROI math on this is almost hard to believe...",
            'hustler': "We've found a growth loophole that nobody else has figured out..."
        }
        return random.choice(list(openings.values()))
    
    def prioritize_arguments(self, profile, project_data):
        if profile['risk_tolerance'] > 0.7:
            return ["Market disruption potential", "First-mover advantage", "Vision scale"]
        else:
            return ["Current traction", "Revenue model", "Customer validation"]
    
    def select_close(self, profile):
        closes = {
            'visionary': "Help us build the future",
            'operator': "Let's build something massive together", 
            'money': "This is the best risk-reward you'll see all year",
            'hustler': "Let's go make some noise and money"
        }
        return random.choice(list(closes.values()))
    
    def follow_up_cadence(self, profile):
        return f"Follow up in {random.randint(1,3)} days with {random.choice(['additional data', 'customer case study', 'competitive analysis'])}"
