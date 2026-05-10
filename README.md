# LLM Playground: Chatbot & Pipeline

Devscale ID #1 assignment - building a simple chatbot and a 3-step pipeline.

## What's Inside

Two tasks in one repo:

1. **Context-Aware Chatbot** - a customer service bot that only knows about a specific business
2. **LLM Pipeline** - chaining 3 functions where each output feeds into the next

---

## Case 1: Context-Aware Chatbot

A simple `input()` based chatbot that acts as customer service for **Lapau Bang Jack**, a small food court in Jakarta Pusat, DKI Jakarta.

### How it works

- Inject business info into the system prompt (context injection)
- User types questions
- Bot answers based *only* on that context
- If it doesn't know, it says so politely

### Example

```
User: Buka jam berapa?
Bot: Kami buka dari jam 6 pagi sampai jam 12 siang ya! 😊

User: Ada nasi padang?
Bot: Maaf, kami tidak menyediakan nasi padang. Menu kami Lontong Tauco, 
Lontong Cubadak, dan Pical saja 🙏
```

The injected context contains menu, prices, location, opening hours - everything the bot needs.

---

## Case 2: LLM Pipeline

Three functions, each calling the LLM, chained together:

```
generate() → summarize() → structurize()
```

### Step by step

| Step | What it does |
|------|-------------|
| `generate()` | Creates long articles about 5 cities |
| `summarize()` | Takes the articles, condenses them |
| `structurize()` | Extracts info into structured JSON |

### The actual code flow

```python
article = generate()           # raw long-form content
summary = summarize(article)   # condensed version
result = structurize(summary)  # structured output (Pydantic → JSON)
```

The final output uses Pydantic so the JSON is properly typed:

```python
class City(BaseModel):
    name: str
    country: str
    iconic_foods: list[str]
    landmarks: list[str]
    # ...
```

---

## Setup

```bash
pip install openai python-dotenv pydantic
```

Create a `.env` file:

```
OPENAI_API_KEY=your_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
BASE_MODEL=gpt-4o-mini
```

## Run

```bash
# Chatbot
python chatbot.py

# Pipeline
python pipeline.py
```

Pipeline saves the structured result to `output.txt`.
