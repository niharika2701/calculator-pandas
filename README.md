# Calculator App Using Pandas

A sophisticated modular calculator with REPL interface, design patterns, and persistent history.

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Usage
```bash
python -m app.calculator_repl
```

## Testing
```bash
pytest --cov=app tests/
```