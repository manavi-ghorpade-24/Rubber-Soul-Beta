# Quick Setup Guide

## Prerequisites

- Python 3.8 or higher
- An Anthropic API key (get one at https://console.anthropic.com/)

## Step-by-Step Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=sk-ant-api03-...
```

### 3. Start the Backend

**Option A: Using the script**
```bash
./start_backend.sh
```

**Option B: Manual**
```bash
cd backend
python3 -m uvicorn main:app --reload
```

The backend will run at `http://localhost:8000`

### 4. Start the Frontend

**Option A: Using the script (in a new terminal)**
```bash
./start_frontend.sh
```

**Option B: Manual (in a new terminal)**
```bash
cd frontend
streamlit run app.py
```

The frontend will open at `http://localhost:8501`

## Usage

1. Open `http://localhost:8501` in your browser
2. Type `/rs` to launch Rubber Soul
3. Follow the prompts to create your content

## Troubleshooting

### "Cannot connect to API server"
- Make sure the backend is running on port 8000
- Check that `ANTHROPIC_API_KEY` is set in `.env`
- Verify the backend started without errors

### "ANTHROPIC_API_KEY not found"
- Make sure you created a `.env` file
- Check that the `.env` file is in the project root
- Verify the key is correctly formatted (starts with `sk-ant-`)

### "RUBBERSOUL-BETA.txt not found"
- Make sure `RUBBERSOUL-BETA.txt` is in the project root directory
- The backend will use a fallback prompt if the file isn't found

## Testing the API

You can test the API directly:

```bash
# Health check
curl http://localhost:8000/health

# Create conversation
curl -X POST http://localhost:8000/api/conversations/create

# Send message (replace CONVERSATION_ID)
curl -X POST http://localhost:8000/api/messages/send \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": "CONVERSATION_ID", "content": "/rs", "ai_mode": "claude"}'
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out [README.txt](README.txt) for the original Rubber Soul specification
- Explore the three modes: Ideation, Development, and Optimization

