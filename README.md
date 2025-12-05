# Smart Form Backend - Nuit de l'Info 2025

Hey there! This is the backend for our intelligent form system built for *Nuit de l'Info 2025*. It's a FastAPI application that uses AI to make forms actually smart and dynamic.

## What does it do?

Imagine you're visiting a website and you type something like "I'd like to volunteer" in a text box. Instead of giving you a boring, static form, this backend:

1. **Figures out what you want** - It reads your message and understands if you want to contact us, make a donation, volunteer, or just get information
2. **Builds a custom form** - Based on what you wrote, it creates form fields that make sense for your specific request
3. **Saves your submission** - Stores everything in MongoDB with metadata
4. **Sends you a personalized message** - Uses AI to generate a fun, themed confirmation message

Pretty cool, right?

## The AI Magic

We're using **Groq's LLM API** (specifically the Llama 3.3 70B model) to power three main features:

### 1. Mission Classification
When you type something, the AI analyzes it and categorizes your intent into one of four missions:
- **Contact** - You want to chat or ask a question
- **Donation** - You're thinking about donating money
- **Volunteer** - You want to help out and get involved
- **Information** - You need details about the project

The AI doesn't just guess—it gives us a confidence score and explains its reasoning.

### 2. Dynamic Field Generation
Once we know your mission, the AI looks at what you wrote and generates additional form fields that make sense. For example:
- If you want to donate, it might add fields for amount and payment method
- If you're volunteering, it might ask about your skills and availability
- The base fields (name, email, message) are always there, but the AI adds what's relevant

### 3. Personalized Confirmations
After you submit the form, the AI generates a custom confirmation message. It's themed around "The Nexus" (our sci-fi adventure vibe), mentions your name, explains what happens next, and keeps things engaging.

## The APIs

Here's what you can do with our backend:

### `POST /api/classify`
Send a message, get back what mission it represents.

**Example request:**
```json
{
  "prompt": "I'd like to make a donation",
  "language": "en"
}
```

**Response:**
```json
{
  "mission": "donation",
  "confidence": 0.95,
  "reasoning": "User explicitly mentions wanting to donate"
}
```

### `POST /api/generate-fields`
Give it a mission and context, get back form fields.

**Example request:**
```json
{
  "mission": "volunteer",
  "prompt": "I'm a developer and want to help on weekends",
  "language": "en"
}
```

**Response:**
```json
{
  "mission": "volunteer",
  "base_fields": [
    {"name": "name", "label": "Your Name", "type": "text", "required": true},
    {"name": "email", "label": "Email", "type": "email", "required": true}
  ],
  "extra_fields": [
    {"name": "skills", "label": "Your Skills", "type": "text", "required": false},
    {"name": "availability", "label": "When are you available?", "type": "select", "options": ["Weekdays", "Weekends", "Flexible"], "required": true}
  ]
}
```

### `POST /api/submit`
Submit the completed form and get a confirmation.

**Example request:**
```json
{
  "mission": "donation",
  "values": {
    "name": "Alice",
    "email": "alice@example.com",
    "amount": 50
  },
  "username": "Alice",
  "language": "en"
}
```

**Response:**
```json
{
  "mission": "donation",
  "year": 2025,
  "confirmation_message": "Greetings, Alice! Your generous offering of 50 credits has been received by the Nexus. Your support fuels our mission throughout 2025. Stay connected for updates on how your contribution makes an impact!"
}
```

### Other endpoints:
- `GET /api/submissions` - Retrieve submitted forms (with pagination)
- `GET /api/submissions/stats` - Get statistics on submissions
- `DELETE /api/submissions/{id}` - Delete a submission
- `GET /health` - Check if the server is running

## Rate Limiting

We've added rate limiting to prevent abuse. Each IP address has limits per minute:
- Classification: 30 requests/min
- Field generation: 20 requests/min  
- Form submission: 10 requests/min
- Fetching submissions: 60 requests/min

If you exceed the limit, you'll get a 429 error with headers telling you when you can try again.

## Getting Started

**Requirements:**
- Python 3.8+
- MongoDB running somewhere
- A Groq API key ([get one here](https://console.groq.com))

**Setup:**

1. Clone and enter the project:
```bash
cd formulaire-intelligent
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your credentials:
```env
GROQ_API_KEY=your_groq_api_key_here
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=formMagique
FRONTEND_ORIGIN=http://localhost:5173
MODEL_NAME=llama-3.3-70b-versatile
```

5. Start MongoDB (if running locally):
```bash
brew services start mongodb-community  # macOS
# or just: mongod
```

6. Run the server:
```bash
uvicorn app.main:app --reload --port 8000
```

Visit `http://localhost:8000/docs` to see the interactive API documentation!

## How It Works Behind the Scenes

1. **User types a message** → Frontend sends it to `/api/classify`
2. **AI analyzes the text** → Returns mission type with confidence
3. **Frontend requests form fields** → `/api/generate-fields` creates custom fields
4. **User fills out the form** → Frontend sends everything to `/api/submit`
5. **Backend saves to MongoDB** → Stores submission with IP, timestamp, etc.
6. **AI generates confirmation** → Returns a personalized message
7. **User sees confirmation** → Frontend displays the response

The whole flow is designed to feel magical—like the form is reading your mind and adapting to what you need.

## Tech Stack

- **FastAPI** - Modern Python web framework
- **Groq API** - Fast LLM inference (Llama 3.3 70B)
- **MongoDB + Motor** - Async database operations
- **Pydantic** - Data validation
- **SlowAPI** - Rate limiting
- **CORS enabled** - Works with frontend on different port

## Project Structure

```
app/
├── routers/          # API endpoints (classify, generate, submit, submissions)
├── services/         # Business logic and AI integration
├── schemas/          # Pydantic models for request/response
├── constants/        # Mission types and base field definitions
├── middleware/       # Rate limiting configuration
├── config.py         # Environment variables
├── database.py       # MongoDB connection
├── models.py         # Database models
└── main.py          # FastAPI app setup
```

## Why This Matters

Traditional forms are static and boring. You fill out fields that might not even apply to you. This project flips that around—the form adapts to *you*. It's a small example of how AI can make web interactions more human and contextual.

Built with ❤️ for Nuit de l'Info 2025
