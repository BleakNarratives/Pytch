"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: wit_factory.py
LAST_SYNC: 2026-08-02T01:13:34Z
[/DNA_TAG]
"""
import random

class WitFactory:
    def __init__(self):
        self.joke_formats = [
            "Why did the {subject} cross the road? To {punchline}",
            "How many {subject}s does it take to screw in a lightbulb? {number}: one to {action1} and {number_minus_one} to {action2}",
            "I'm not saying our {subject} is {quality}, but {hyperbole}",
            "What do you call a {subject} that {does_thing}? {answer}"
        ]
        
        self.tech_roasts = [
            "Our code is so clean, it makes hospital operating rooms look messy.",
            "Their MVP has more bugs than a rainforest floor.",
            "That deployment was smoother than a VC's pickup line.",
            "Our scalability makes their architecture look like a house of cards in a hurricane."
        ]
        
        self.business_snark = [
            "That business model has more holes than Swiss cheese.",
            "Their growth strategy is basically hopes and prayers with a spreadsheet.",
            "That valuation isn't optimistic, it's delusional with a side of crazy.",
            "Their moat is so small, a determined duck could cross it."
        ]
    
    def generate_meeting_icebreaker(self, context):
        icebreakers = [
            f"Before we start, I just want to say {context['project_name']} is so disruptive, it makes Uber look like a taxi company with an app.",
            f"I was going to prepare slides, but then I realized {context['project_name']} sells itself. Unlike my last startup.",
            f"Quick housekeeping: phones on silent, judgments on hold, and checkbooks at the ready."
        ]
        return random.choice(icebreakers)
    
    def generate_investor_zinger(self, question_type):
        zingers = {
            'valuation': [
                "Our valuation isn't a number, it's a vibe. And the vibe is: expensive but worth it.",
                "We're not overvalued, you're just thinking too small. Think bigger. Then think bigger than that."
            ],
            'traction': [
                "Traction? We've got more traction than a tractor pull in mud season.",
                "Our user growth looks like a hockey stick that's been to the gym."
            ],
            'competition': [
                "Competition? You mean the amateurs we use for target practice?",
                "They're not competitors, they're feature suggestions waiting to happen."
            ],
            'timeline': [
                "Our timeline is aggressive, but so was my ex and look how that turned out. Successful.",
                "We'll be ready yesterday, but the market needs to catch up to tomorrow."
            ]
        }
        return random.choice(zingers.get(question_type, ["Excellent question. Let me answer with equal excellence."]))
    
    def generate_self_deprecating_humor(self):
        lines = [
            "I'm so confident in this, I'd bet my mother's good china on it. And she loves that china.",
            "This idea is so good, even my imposter syndrome took the day off.",
            "I've made worse decisions. Like that time I tried to code a social network in COBOL.",
            "If this fails, I'll just say it was performance art about startup culture."
        ]
        return random.choice(lines)
    
    def add_humor_to_pitch(self, pitch_text):
        """Inject humor into boring pitch content"""
        replacements = {
            'paradigm shift': 'glorious revolution that makes other paradigms look basic',
            'synergy': 'magical business fairy dust', 
            'disrupt': 'aggressively improve while making incumbents cry',
            'innovative': 'so new it still has that new car smell',
            'enterprise-ready': 'tougher than a two-dollar steak'
        }
        
        for boring, funny in replacements.items():
            pitch_text = pitch_text.replace(boring, funny)
            
        return pitch_text
