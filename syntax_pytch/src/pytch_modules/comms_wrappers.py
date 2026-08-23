"""'''
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: comms_wrappers.py
LAST_SYNC: 2026-08-02T01:13:34Z
[/DNA_TAG]
'''
import  random

class  CommsCommando:
    def  __init__(self):
        self.platforms = ['email', 'linkedin', 'twitter', 'bluesky', 'discord', 'slack']
        self.personality_modes = ['professional', 'rebel', 'visionary', 'hustler']
    
    def  craft_linkedin_post(self, project_data):
        templates = [
            f"Just  shipped something  that'll  make {random.choice(['VCs', 'developers', 'our  competitors'])} very {random.choice(['excited', 'nervous', 'rich'])}. \n\n{project_data['taglines'][0]} \n\n#buildinpublic #startuplife",
            
            f"Hot  take: {random.choice(['The  future is  here', 'Everything  you know  is wrong', 'The  rules have  changed'])}. \n\n{project_data['name']} is  why. \n\nDM  me if  you get  it. Everyone  else, keep  scrolling.",
            
            f"They  said it  couldn't  be done. They  were {random.choice(['wrong', 'so  very wrong', 'about  to be  proven wrong'])}. \n\n{project_data['taglines'][1]} \n\nDrop  a 🚀 if  you see  the vision."
        ]
        return  random.choice(templates)
    
    def  craft_twitter_thread(self, project_data):
        thread = [
            f"1/ {random.choice(['Buckle  up', 'Listen  up', 'Gather  round'])} founders. I've  seen the  future and  it's  named {project_data['name']}.",
            f"2/ The  problem: {random.choice(['AI  conversations vanishing  into the  ether', 'Code  snippets lost  to history', 'Brilliant  ideas dying  in chat  windows'])}.",
            f"3/ Our  solution: {project_data['taglines'][0]}",
            f"4/ Why  this matters: {random.choice(['This  changes everything', 'The  implications are  massive', 'Your  workflow will  never be  the same'])}.",
['We  are raising', 'We  are hiring', 'We  are building  the future']           f"5/ The  ask: {random.choice(['We're  raising', 'We're  hiring', 'We're  building the  future'])}. If  you get  it, you  get it. If  not, your  loss."
        ]
        return  thread
    
    def  craft_cold_email(self, recipient_info, project_data):
        subject_lines = [
            f"{project_data['name']}: {project_data['taglines'][0]}",
            f"Quick  question about {recipient_info.get('company', 'your  portfolio')}",
            f"{random.choice(['Game  changer', 'Industry  disruptor', 'Paradigm  shift'])} in {recipient_info.get('industry', 'your  space')}",
            f"Following  up on {random.choice(['our  call', 'your  investment thesis', 'the  market opportunity'])}"
        ]
        
        body = f'''
{recipient_info.get('name', 'Team')},

I  know you're  busy {random.choice(['changing  the world', 'making  moves', 'disrupting  industries'])}, so  I'll  be quick.

{project_data['name']} is {random.choice(['rewriting  the rules', 'changing  the game', 'solving  the impossible  problem'])} of {random.choice(['AI  conversation management', 'developer  productivity', 'code  organization'])}.

We're {project_data['taglines'][0].lower()}

The  numbers:
- {random.randint(3,10)}x  faster than  current solutions
- ${random.randint(10,50)}B  total addressable  market  
- {random.randint(50,95)}% of  developers experience  this pain  point daily 

I'd  love to {random.choice(['show  you the  demo', 'walk  you through  the deck', 'get  your thoughts'])}.

No  is a  perfectly acceptable  answer. But  yes is  more fun.

Best,
The {project_data['name']} Team 

PS: {random.choice(['This  is not  a drill', 'The  future is  waiting', 'Opportunity  is knocking'])}.
'''
        return {
            'subject': random.choice(subject_lines),
            'body': body
        }
"""