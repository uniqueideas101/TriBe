# TriBe – AI Hotel Discovery Agent
> Find your vibe. Book your stay.

## Setup

**1. Install dependencies**
```bash
pip install streamlit anthropic
```

**2. Run the app**
```bash
streamlit run tribe_app.py
```

Opens at http://localhost:8501

---

## How it works

1. User enters **location**, **budget**, and **trip vibe**
2. Rule-based filter narrows the mock hotel dataset
3. Claude generates a personalised explanation for each shortlisted hotel
4. User sees 3–5 hotels with vibe reasoning, guest photo notes, and nearby places

## Supported locations (mock data)
Jaipur, Goa, Rishikesh, Manali, Coorg, Pondicherry, Spiti, Chettinad

## Stack
- Streamlit (UI)
- Anthropic Claude Sonnet (vibe explanations)
- Mock hotel dataset (8 hotels across India)
