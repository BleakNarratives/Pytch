#!/usr/bin/env python3
"""Stage the release-kit POSTING_PLAN.md content into Pytch social_posts.

Pulled straight from ~/MikeySwarm/release/POSTING_PLAN.md. Nothing here is
auto-posted — every row lands with status='ready' and scheduled_for=NULL.
The plan itself mandates one venue at a time, read the room, human-gates
the trigger. This just makes the content reviewable in one place.

Usage: python3 stage_posting_plan.py
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "pytch" / "pytch.db"
COMM_LOG = Path.home() / "MikeySwarm" / "logs" / "communications" / "orchestrator_to_freebuff.log"

REPO = "https://github.com/BleakNarratives/MikeySwarm"
PAPER = f"{REPO}/blob/main/MikeySwarm/WHITE_PAPER.md" if False else "~/MikeySwarm/WHITE_PAPER.md"

# ── Content per venue (from release/POSTING_PLAN.md) ────────────────────
POSTS = [
    {
        "platform": "show_hn",
        "status": "ready",
        "content": (
            "Title: Show HN: Persona injection doubles behavioral alignment in LLM agents "
            "(77-run study)\n\n"
            "Post the GitHub repo, not a blog. First commenter = the caveats section verbatim "
            "(pre-empt methodological criticism). Windows: Tue-Thu 7-9am Central.\n\n"
            "Repo: https://github.com/BleakNarratives/MikeySwarm\n"
            "Expected pushback: 'n=5 is tiny' (own it), 'prompt engineering, so what?' "
            "(answer: it's behavioral signature preservation, not task completion)."
        ),
    },
    {
        "platform": "reddit_localllama",
        "status": "ready",
        "content": (
            "Frame: 'What 6 rounds of persona-injection experiments on a 2.6GB Chromebook VM "
            "taught me about agent alignment.'\n\n"
            "Include the MemGuard duress data (hardware war stories land with this crowd): "
            "duress does NOT degrade persona behavior across all measured rounds "
            "(full-corpus audit: 23/96 runs instrumented, PRESSURE 0.856 vs NOMINAL 0.884, "
            "within noise). R8 lesion collapse ran entirely NOMINAL — hardware-clean.\n"
            "MemGuard: https://github.com/BleakNarratives/MemGuard"
        ),
    },
    {
        "platform": "reddit_machinelearning",
        "status": "ready",
        "content": (
            "Tier 2 — ONLY if HN response shows genuine interest. Strict sub; lead with "
            "methodology, not findings. The roles-only stress test (Round 4) is the most "
            "defensible result — lead with that: structure gets you 82% of alignment, identity "
            "the final 18%, and that 18% is entirely communication register (directness, "
            "anti_larp, no_hedging)."
        ),
    },
    {
        "platform": "zenodo",
        "status": "ready",
        "content": (
            "Upload WHITE_PAPER.md + persona_runs.db snapshot as a citable preprint (free DOI). "
            "Version per major round. Current corpus: 96 runs, 11 groups (A-H, I/J/K lesions).\n"
            "Bundle exists at ~/MikeySwarm/release/zenodo/ (stale at 77 runs — regenerate "
            "before upload)."
        ),
    },
    {
        "platform": "lobsters",
        "status": "ready",
        "content": (
            "If invite available: the SYSTEMS angle plays better than the ML angle here — "
            "MemGuard OOM defense (session-shield pins oom_score_adj=-900, pressure-watch "
            "forensics, 6GB swapfile + swappiness=100), systemd timer round engine, cache "
            "guards, lean_mode. Link both repos."
        ),
    },
    {
        "platform": "x_thread",
        "status": "ready",
        "content": (
            "8-10 tweets, one finding per round:\n"
            "1. Persona injection doubles alignment (A=2.4x baseline)\n"
            "2. Contradictory conditions catastrophic (B=0.45x, below baseline)\n"
            "3. Systems thinking is the most trainable dimension (2.50x)\n"
            "4. Identity = register, not structure (E 0.832 vs A 0.920)\n"
            "5. Register traits are a bundle (F/G ≈ A, non-sufficient)\n"
            "6. Adversarial pressure doesn't break it (H 0.913)\n"
            "7. Lesions prove necessity (I/J/K collapse 0.577-0.738)\n"
            "8. Hardware duress doesn't degrade it (R6/R8 full-corpus audit)\n"
            "9. MemGuard shipped as the first public tool from the experiment\n"
            "Sparkline screenshot from guarddash, link at the end."
        ),
    },
    {
        "platform": "newsletter",
        "status": "ready",
        "content": (
            "Hacker Newsletter / TLDR AI — submit AFTER HN traction; they harvest HN anyway. "
            "One-paragraph pitch: 96-run behavioral experiment on a 2.6GB Crostini VM showing "
            "persona injection doubles agent alignment; register traits form a necessary bundle; "
            "hardware duress measured and ruled out as a confound."
        ),
    },
    {
        "platform": "lesswrong",
        "status": "ready",
        "content": (
            "Low priority — only if the paper's epistemics section is expanded first. LW wants "
            "decision-theory framing, not engineering logs. Hold."
        ),
    },
]


def main() -> int:
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS social_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT, content TEXT, media_url TEXT,
            scheduled_for DATETIME, posted_at DATETIME,
            engagement_count INTEGER DEFAULT 0, status TEXT)"""
    )
    now = datetime.now().isoformat()
    inserted = 0
    for post in POSTS:
        cur = conn.execute(
            "INSERT INTO social_posts (platform, content, media_url, scheduled_for, posted_at, engagement_count, status) "
            "VALUES (?, ?, ?, NULL, NULL, 0, ?)",
            (post["platform"], post["content"], None, post["status"]),
        )
        inserted += 1
        print(f"  staged: {post['platform']} (id {cur.lastrowid}, status={post['status']})")
    conn.commit()
    conn.close()

    # ── Comms log ────────────────────────────────────────────────────────
    entry = {
        "timestamp": now,
        "from": "orchestrator",
        "to": "freebuff",
        "agent_id": None,
        "message": (
            f"PYTCH_POSTING_PLAN_EXECUTED:staged={inserted}_venues:"
            f"show_hn,reddit_localllama,reddit_machinelearning,zenodo,lobsters,"
            f"x_thread,newsletter,lesswrong:status=ready:"
            f"pitches_generated=4(brander,social_soldier,wit_factory,deck_matic):"
            f"pipeline_bug_fixed=generate_pitch_UNIQUE_violation:"
            f"outreach_send=SKIPPED(no_smtp_creds):human_gate=required"
        ),
        "system": "orchestrator",
    }
    COMM_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(COMM_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"\n[COMMUNICATION] -> Freebuff: {entry['message'][:120]}...")
    print(f"Comms log: {COMM_LOG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
