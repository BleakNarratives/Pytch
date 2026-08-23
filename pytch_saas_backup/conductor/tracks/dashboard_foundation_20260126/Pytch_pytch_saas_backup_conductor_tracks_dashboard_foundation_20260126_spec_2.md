# Specification: Dashboard Foundation

## Overview
This track focuses on creating the initial web-based interface for the Lead Gen SaaS. It bridges the gap between the existing Python-based `pytch.py` engine and a browser-accessible dashboard.

## Functional Requirements
- **FastAPI Backend:** Create an API wrapper around the `pytch.py` logic.
- **Campaign Trigger:** API endpoint to start the `send-outreach` process.
- **Basic UI:** A simple web dashboard showing campaign metrics (emails sent, reply rate).
- **Existing IP Integration:** Import and use the core functions from `pytch.py`.

## Non-Functional Requirements
- **Response Time:** UI should update promptly when actions are triggered.
- **Portability:** Must run within the current environment (Termux/Python).

## Acceptance Criteria
- User can open a web page and see the current campaign metrics.
- User can click a button to trigger the outreach sending process.
- All new code meets the 90% test coverage threshold.
