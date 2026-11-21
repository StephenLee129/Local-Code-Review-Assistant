# Setup Guide

This guide walks through installing and running the Local Code Review Assistant on your machine.

## Prerequisites

You'll need:

- **Python 3.12**
- **Git**
- **Ollama** — used to run the AI model locally
- An internet connection for the initial setup and model download

A dedicated NVIDIA GPU is recommended for faster inference, but GPU acceleration is not a requirement of the application.

## 1. Install Ollama and download the model

Download and install Ollama from:

[https://ollama.com/download](https://ollama.com/download)

Once installed, open a terminal and download the model:

```bash
ollama pull qwen2.5-coder:7b
```

This downloads the Qwen2.5-Coder 7B model to your machine. The initial download may take a few minutes.

Verify that the model is available:

```bash
ollama list
```

Keep Ollama running while using the application. On Windows, the Ollama application normally runs its local service in the background.

## 2. Clone the repository

Open a terminal and run:

```bash
git clone https://github.com/StephenLee129/Local-Code-Review-Assistant.git
cd Local-Code-Review-Assistant
```

## 3. Create a Python virtual environment

A virtual environment keeps this project's Python dependencies separate from other Python applications on your machine.

Create the environment:

**Windows:**

```bash
py -3.12 -m venv .venv
```

**macOS / Linux:**

```bash
python3.12 -m venv .venv
```

Activate it.

**Windows — Git Bash:**

```bash
source .venv/Scripts/activate
```

**Windows — PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

Once activated, your terminal should indicate that the `.venv` environment is active.

## 4. Install Python dependencies

With the virtual environment activated, run:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

This installs the dependencies needed for the frontend, backend, local model integration, and tests.

## 5. Start the backend

Open a terminal from the project root, activate the virtual environment if necessary, and run:

```bash
python -m uvicorn backend.app.main:app --reload
```

The FastAPI backend will start at:

[http://127.0.0.1:8000](http://127.0.0.1:8000)

You can verify that it's running by opening:

[http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

You can also explore the API documentation at:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

**Leave this terminal running.**

## 6. Start the frontend

Open a second terminal from the project root and activate the virtual environment.

Run:

```bash
streamlit run frontend/app.py
```

Streamlit will open the application in your browser, normally at:

[http://localhost:8501](http://localhost:8501)

Paste some source code into the editor, click **Review Code**, and wait for the model to generate its analysis.

That's it! You now have a locally running AI code review application.

## Troubleshooting

| Problem | What to check |
|---|---|
| Cannot connect to the backend | Make sure the FastAPI terminal is still running. |
| Cannot connect to Ollama | Make sure the Ollama application and local service are running. |
| Model not found | Run `ollama pull qwen2.5-coder:7b`. |
| Python package errors | Verify that your virtual environment is activated and dependencies are installed. |
| Inference is slow | Model loading and inference speed depend on your hardware. The first request may take longer. |

## Running tests

From the project root, with the virtual environment activated, run:

```bash
python -m pytest -v
```

To run the evaluation example:

```bash
python -m evaluation.run_evaluation
```