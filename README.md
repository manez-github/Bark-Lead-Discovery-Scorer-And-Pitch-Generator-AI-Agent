# Bark-AI-Lead-Discovery-Scorer-And-AI-Pitch-Generator-Agent

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-purple)
![Groq](https://img.shields.io/badge/Groq-GPT--OSS--120B-orange)
![Playwright](https://img.shields.io/badge/Playwright-Automation-green)
![uv](https://img.shields.io/badge/uv-Package%20Manager-lightgrey)

An autonomous AI agent that logs into **Bark.com** via Google OAuth, scrapes buyer leads, scores them against an Ideal Customer Profile (ICP) using an LLM, and generates personalized pitches for high-quality leads — all without human intervention.

---

## 🎬 Demo Video

<video src="https://github.com/manez-github/Bark-Lead-Discovery-Scorer-And-Pitch-Generator-AI-Agent/raw/refs/heads/main/demo_video/bark-ai-agent-demo-video.mp4" controls="controls" style="max-width: 100%;"></video>
---
## ✨ What It Does

| Step | Action |
|------|--------|
| 1 | Launches a real browser and logs into Bark.com via **Google OAuth** |
| 2 | Scrapes all available leads from the seller dashboard |
| 3 | Scores each lead **(0.0 → 1.0)** against a predefined ICP using an LLM |
| 4 | Generates a personalized **3-paragraph pitch** for every lead scoring ≥ 0.8 |
| 5 | Saves everything to a local JSON database, skipping duplicates on future runs |
| 6 | Runs in a loop — automatically re-checks for new leads every **6 hours** |

---

## ✨ Features

- **Persistent Browser Session**: Uses Playwright's `launch_persistent_context` to store cookies, cache, local storage, and a full browser profile on disk — making the session indistinguishable from a legitimate returning user to Google's bot-detection systems.
- **Human-like Automation**: Implements randomized delays, character-by-character typing, and smooth mouse movements to mimic real human input patterns.
- **Intelligent Lead Scoring**: Utilizes an LLM to score leads based on a strict logic hierarchy (Budget overrides vs. Perfect Fit exceptions).
- **Automated Pitch Generation**: Generates 3-paragraph personalized cold outreach messages for qualified leads.
- **Graph-Based Architecture**: Built with LangGraph for robust state management and workflow orchestration.

---

## 📁 Project Structure

```
project_root/
├── main.py                          # Entry point — runs the agent in a continuous loop
├── graph/
│   ├── graph.py                     # LangGraph pipeline — wires all nodes together
│   ├── states.py                    # Defines AgentState and Pydantic models (LeadScore)
│   ├── prompts.py                   # ICP description + Pitch generation prompts
│   └── nodes/
│       ├── init_node.py             # Launches Playwright persistent browser context
│       ├── auth_check_node.py       # Checks if user is already logged in
│       ├── login_node.py            # Handles Google OAuth login flow
│       ├── scraper_node.py          # Scrapes lead data from the dashboard
│       ├── analyst_node.py          # Scores leads via LLM using structured output
│       ├── pitch_generator_node.py  # Generates pitches for qualified leads
│       └── close_node.py            # Closes browser and stops Playwright
├── utils/
│   ├── helpers.py                   # Humanization functions, Credentials, Keep Awake
│   └── database.py                  # Handles reading/writing to database
├── data/
│   └── leads.json                   # Local JSON database of scraped leads
├── browser_data/                    # Persistent browser session (stores login cookies)
├── .env                             # Credentials (never commit this)
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Browser Automation | Playwright (async) |
| Agent Orchestration | LangGraph |
| LLM | Groq API — GPT-OSS 120B |
| LLM Integration | LangChain + langchain-groq |
| Data Storage | JSON file (local) |
| Package Manager | uv |
| Language | Python 3.11 |

---

## ⚙️ Setup

### 1️⃣ Clone the repo

```bash
git clone https://github.com/yourusername/Bark-AI-Lead-Discovery-Scorer-And-AI-Pitch-Generator-Agent.git
cd Bark-AI-Lead-Discovery-Scorer-And-AI-Pitch-Generator-Agent
```

### 2️⃣ Install uv (if not already installed)

```bash
pip install uv
```

### 3️⃣ Install dependencies

```bash
uv sync
playwright install chromium
```

### 4️⃣ Create a `.env` file

```env
GMAIL_ID=your_gmail@gmail.com
GMAIL_PASS=your_google_password
GROQ_API_KEY=your_groq_api_key
```

> Get a free Groq API key at [console.groq.com](https://console.groq.com)

### 5️⃣ Run the agent

```bash
python -m main
```

> To stop the agent manually press `Ctrl + C`

---

## 🧠 Customization

Edit `graph/prompts.py` to tailor the agent's behavior:

- **`ICP_DESCRIPTION`**: Change the Ideal Customer Profile to target different project types, industries, or budget ranges.
- **`PITCH_PROMPT`**: Adjust the tone, structure, or length of the generated cold outreach messages.

---

## 🔄 How the Agent Pipeline Works

The agent follows a directed graph defined in `graph.py`:
```
Init → Auth Check → [Login] → Scraper → Analyst → Pitch Generator → Close
```

| Step | Node | Description |
|---|---|---|
| 1 | **Init** | Launches a Chromium browser with a persistent context (saving session to `./browser_data`) |
| 2 | **Auth Check** | Navigates to `bark.com/login` to verify if the user is already logged in |
| 3 | **Login** | If not logged in, performs a human-like Google OAuth login flow |
| 4 | **Scraper** | Navigates to the Sellers Dashboard, scrolls to load all leads, extracts Name, Budget, Category, and Q&A, then saves new leads to `data/leads.json` |
| 5 | **Analyst** | Reads unanalyzed leads and scores them (0.0–1.0) using an LLM with ICP logic |
| 6 | **Pitch Generator** | Creates a personalized 3-paragraph pitch for leads scoring `> 0.8` |
| 7 | **Close** | Safely closes the browser context and stops Playwright |

<div align="center">
  <img width="575" height="821" alt="Bark AI Agent drawio" src="https://github.com/user-attachments/assets/edca67fb-8add-42b3-8666-5fa2aeeb08d6" />
</div>

- `auth_check` routes to `login` or directly to `scraper` depending on session state
- `analyst` routes to `pitcher` if qualified leads exist, or `close` if none
- The persistent browser context in `browser_data/` stores your session so **login only happens once**
- After each full cycle, the agent sleeps for **6 hours** before running again

---

## 🎯 Ideal Customer Profile (ICP)

The agent scores leads based on the following criteria (defined in `prompts.py`):

- **📌 Project Type:** E-commerce, Custom Web App, or Bespoke Design. Rejects bug fixes and maintenance.
- **🏢 Business Type:** Established businesses. Rejects students and hobbyists.
- **💰 Budget Logic:**
  - Budget ≥ £999 → ✅ auto-qualify regardless of other factors
  - Perfect project + business type match → ✅ qualify regardless of budget
  - Otherwise → minimum **£750** required

---

## 📊 Lead Status Flow

Each lead in `leads.json` moves through these statuses:

```
🆕 NEW  →  🔍 ANALYZED  →  ✍️ PITCHED
```

> Duplicate leads are detected using a composite ID and skipped automatically.

---

## ⚠️ Anti-Detection Measures

### 🗂️ Persistent Browser Context

This is the most critical anti-detection mechanism in the project.

When Playwright launches a **normal browser context**, it creates a completely fresh, ephemeral session — no cookies, no cache, no local storage, no browsing history. Google and other platforms actively flag these sessions as suspicious because:

- No cookies means no prior session history with Google's servers
- Empty local storage means no saved preferences, tokens, or user fingerprints
- No cache means every asset is fetched fresh — atypical of a real returning user
- No browser profile data on disk — bots rarely persist data between sessions

Google's bot-detection systems (used during the OAuth login flow) check for all of the above. A clean-slate browser is a strong signal of automation.

**`launch_persistent_context`** solves this by saving the following to a directory on disk (`./browser_data/`):

| Data Type | What It Stores | Why It Matters to Google |
|---|---|---|
| **Cookies** | Session tokens, `GAPS`, `SIDCC`, `__Secure-1PSID` etc. | Proves prior authenticated sessions with Google |
| **Local Storage** | User preferences, app state, tokens | Indicates a returning, familiar browser environment |
| **Cache** | Previously fetched assets (JS, images, fonts) | Mimics a browser that has visited the site before |
| **IndexedDB** | Structured app data stored by web apps | Present in all real browsers that have used Google services |
| **Service Workers** | Background sync and push notification data | Absent in fresh contexts; present in real browsers |
| **Browser Profile on Disk** | The existence of a `browser_data/` folder on the filesystem | Google checks whether browser data is physically stored on disk — a legitimate user's browser always has a profile directory |

The mere existence of a populated profile directory on disk is itself a trust signal. Real users' browsers always have data saved locally. An ephemeral context with nothing on disk is a textbook bot fingerprint.

After the **first successful manual login**, all of this data is saved automatically to `./browser_data/`. Every subsequent run reuses this profile, making the browser appear as a legitimate returning user rather than a fresh automated session.

### 🤖 Human Behaviour Simulation

Beyond the browser context, the following helper functions in `utils/helpers.py` simulate real human interaction patterns at the input level:

- Random delays between all actions (`human_delay`)
- Character-by-character typing with variable speed (`human_type`)
- Smooth mouse movements impersonating an actual human moving the mouse (`human_mouse_move`)
- Real Chromium browser with a legitimate user agent string
- Windows sleep prevention via `keep_awake()` so long runs are uninterrupted

---

## 🙈 .gitignore

```
.env
browser_data/
data/
__pycache__/
*.pyc
```
