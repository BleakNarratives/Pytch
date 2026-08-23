"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: app.py
LAST_SYNC: 2026-08-02T01:13:33Z
[/DNA_TAG]
"""
def check_claim(claim):
    # Simple keyword check (placeholder)
    keywords = ["fake", "scam", "misleading"]
    for word in keywords:
        if word in claim.lower():
            return "Potential misinformation detected."
    return "Claim appears neutral."

if __name__ == "__main__":
    claim = input("Enter a statement for verification: ")
    print(check_claim(claim))
