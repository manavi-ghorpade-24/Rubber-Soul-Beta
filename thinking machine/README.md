# Rubber Soul Beta - Web Application

**The Trust Architecture Engine**  
AI-Assisted. Human-Souled.

A web application that helps you create viral social media content using the Claude API. Built on 7M+ impressions, 215 scoring factors, and refined trust architecture patterns.

## Features

- **Three Modes**: Ideation, Development, and Optimization
- **Multi-Platform Support**: LinkedIn, X/Twitter, Medium, Blog, Video Scripts
- **215-Factor Scoring**: 16 craft dimensions + 14 trust patterns
- **Socratic Inquiry**: Deep questioning to excavate your best ideas
- **Predictive Analytics**: Impression forecasting based on content quality

## Project Structure

```
thinking machine/
├── backend/
│   └── main.py          # FastAPI server with Claude API integration
├── frontend/
│   └── app.py           # Streamlit UI
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── README.md           # This file
├── README.txt          # Original Rubber Soul documentation
└── RUBBERSOUL-BETA.txt # System prompt specification
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and add your Anthropic API key:

```bash
cp .env.example .env
```

Edit `.env`:
```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

Get your API key from: https://console.anthropic.com/

### 3. Start the Backend Server

```bash
cd backend
python3 -m uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### 4. Start the Frontend

In a new terminal:

```bash
cd frontend
streamlit run app.py
```

The UI will open at `http://localhost:8501`

## Usage

1. Open the Streamlit app in your browser
2. Type `/rs` to launch Rubber Soul
3. Follow the prompts to:
   - Select your platform (LinkedIn, X/Twitter, etc.)
   - Choose a mode (Ideation, Development, or Optimization)
   - Create and refine your content

## Commands

- `/rs` - Launch Rubber Soul
- `/score` - Full 215-factor analysis
- `/trust` - Trust architecture deep dive
- `/reveal` - Analyze revelation structure
- `/coalition` - Analyze coalition breadth
- `/research` - Find supporting evidence
- `/hooks` - Generate alternative hooks
- `/draft` - Generate/regenerate draft
- `/publish` - Full publish prep
- `/help` - Show command list

## Modes

### Mode 1: IDEATION
Don't know what to write about? Start here.
- Guided topic discovery
- Angle generation
- Hook development
- Evidence gathering

### Mode 2: DEVELOPMENT
Have a rough idea? Refine it.
- Deep Socratic questioning
- Excavate your revelation
- Find your costly signal
- Build from insight

### Mode 3: OPTIMIZATION
Have a draft? Improve it.
- Full 215-factor scoring
- Specific fixes ranked by impact
- Predicted impression ranges

## Scoring System

### 16 Craft Dimensions (165 points)
1. Clarity (10 pts)
2. Structural Integrity (10 pts)
3. Narrative Cohesion (10 pts)
4. Hook Strength (15 pts)
5. Insight Density (10 pts)
6. Evidentiary Weight (15 pts)
7. Contrarian Value (10 pts)
8. Moral/Ethical Framing (10 pts)
9. Technical Accuracy (10 pts)
10. Tonal Coherence (5 pts)
11. Rhythm & Cadence (10 pts)
12. Platform Fit (10 pts)
13. Novelty (10 pts)
14. Memorability (10 pts)
15. Strategic Identity Alignment (5 pts)
16. Viral Dynamics Readiness (5 pts)

### 14 Trust Patterns (50 points)
1. Revelation Structure (8 pts)
2. Costly Signal (5 pts)
3. Coalition Breadth (5 pts)
4. Accusation-in-Hook (4 pts)
5. Evidence Position (3 pts)
6. Historical Triad (3 pts)
7. Pronoun Architecture (3 pts)
8. Negation Opening (2 pts)
9. Parenthetical Intimacy (2 pts)
10. Single-Sentence Punches (3 pts)
11. Turn Point Location (2 pts)
12. Metacognitive Interrupt (2 pts)
13. Agency Closing (5 pts)
14. Meta-Commentary (3 pts)

## Predictive Ranges

| Score | Tier | Predicted Impressions |
|-------|------|----------------------|
| 185+ | MEGA-VIRAL | 500K+ |
| 155-184 | VIRAL | 150K – 500K |
| 125-154 | STRONG | 50K – 150K |
| 100-124 | SOLID | 20K – 50K |
| Below 100 | NEEDS WORK | Under 20K |

## API Endpoints

- `GET /health` - Health check
- `POST /api/conversations/create` - Create new conversation
- `POST /api/messages/send` - Send message and get response
- `GET /api/conversations/{id}` - Get conversation history
- `GET /api/conversations/{id}/session` - Get session state
- `PUT /api/conversations/{id}/session` - Update session state

## Development

### Backend
The backend uses FastAPI and integrates with Anthropic's Claude API. The Rubber Soul system prompt is loaded from `RUBBERSOUL-BETA.txt`.

### Frontend
The frontend is built with Streamlit and provides a clean, minimal chat interface.

## Notes

- Currently uses in-memory storage for conversations (use a database in production)
- The system prompt is loaded from `RUBBERSOUL-BETA.txt` in the project root
- Make sure the `RUBBERSOUL-BETA.txt` file is accessible from the backend directory

## License

Created by Stephen Klein | Curiouser.AI

## Version

**RUBBER SOUL BETA**  
Last Updated: November 2024

AI-assisted. Human-souled. One revelation at a time.


