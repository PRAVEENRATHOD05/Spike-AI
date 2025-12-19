#!/usr/bin/env bash
set -e

echo "Starting Spike AI Backend Deployment..."

# -----------------------------
# 1. Create virtual environment
# -----------------------------
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv || python -m venv .venv
fi

# -----------------------------
# 2. Activate virtual environment (cross-platform)
# -----------------------------
if [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
  source .venv/Scripts/activate
else
  echo "Could not find virtual environment activation script"
  exit 1
fi

# -----------------------------
# 3. Upgrade pip
# -----------------------------
echo "Upgrading pip..."
python -m pip install --upgrade pip || true


# -----------------------------
# 4. Install dependencies
# -----------------------------
echo "Installing dependencies..."
pip install -r requirements.txt

# -----------------------------
# 5. Start FastAPI server
# -----------------------------
echo "Starting FastAPI server on port 8080..."
nohup uvicorn app.main:app --host 0.0.0.0 --port 8080 > server.log 2>&1 &

echo "Deployment complete. Server running on port 8080."
