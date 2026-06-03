# Transformer AI Backend (Teacher Guide)

This folder is the "brain" of the project.
It does 2 jobs:

- Predicts transformer health from test values
- Answers chat questions using transformer documents (RAG)

follow the steps exactly in order.

## What you need first

- Python installed (recommended: Python 3.10 or newer)
- A Google AI API key (only needed for the chat feature)

## Step 1: Open this folder in Terminal

Open VS Code Terminal and go to this backend folder:


## Step 2: Install Python packages (first time only)

```bash
pip install -r requirements.txt
```

Wait until installation finishes.

## Step 3: Add your Google API key (for chat)

Create a file named `.env` inside this backend folder.

Put this line inside it:

```env
GOOGLE_API_KEY=your_real_key_here
```

Important:

- No spaces around `=`
- Keep the key private

If you only want prediction and do not need chat, you can skip this step.

## Step 4: Build the document database (first time only)

This creates a searchable database from the PDF files in `rag/data`.

```bash
python build_chroma.py
```

You should see a success message like: `Chroma DB built successfully`

## Step 5: Start the backend server

```bash
uvicorn main:app --reload
```

Keep this terminal open while using the app.

When it is running, backend address is:

- `http://localhost:8000`

Quick check in browser:

- Open `http://localhost:8000`
- You should see: `Transformer AI Backend Running`

## How to use with the frontend

1. Start backend first (Step 5).
2. Start frontend in a second terminal (see frontend README).
3. Open frontend page in browser.
4. Use sliders and click Analyze.
5. For chat, make sure your API key is set and Chroma was built.

## Daily use (after first setup)

Each time you use the system:

1. Open terminal in backend folder
2. Run:

```bash
uvicorn main:app --reload
```

That is all.

## If something goes wrong

### Error: `No module named ...`

Run again:

```bash
pip install -r requirements.txt
```

### Error related to API key or chat not answering

- Check `.env` file exists in this folder
- Check key name is exactly `GOOGLE_API_KEY`
- Restart backend after editing `.env`

### Error: Chroma or retrieval not working

Run again:

```bash
python build_chroma.py
```

### Port already in use

If `8000` is busy, start with another port:

```bash
uvicorn main:app --reload --port 8001
```

Then update frontend API URL to the same port.

## Files used by backend

- `main.py` -> API endpoints (`/predict`, `/chat`)
- `build_chroma.py` -> builds document database
- `rag/chatbot.py` -> chat logic
- `requirements.txt` -> Python packages
