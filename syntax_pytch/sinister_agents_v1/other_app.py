"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: other_app.py
LAST_SYNC: 2026-08-02T01:13:33Z
[/DNA_TAG]
"""
class JaneBot:
    def __init__(self, username):
        self.username = username
        self.memory = []

    def greet(self):
        print(f"Hi {self.username}, I'm JaneBot – your personal AI companion.")
        self.vibe_check()

    def vibe_check(self):
        feeling = input("How are you feeling today? ")
        self.memory.append({'vibe': feeling})
        print(f"Thank you for sharing. I'll keep that in mind.")

    def planner(self):
        task = input("What would you like to plan today? ")
        self.memory.append({'task': task})
        print(f"Got it! Let's make progress on: {task}")

if __name__ == "__main__":
    username = input("Enter your name: ")
    agent = JaneBot(username)
    agent.greet()
    agent.planner()
