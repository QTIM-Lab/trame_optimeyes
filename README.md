## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Run application

```bash
optimeyes --server --hot-reload --batch ./data/REFUGE_pure/glaucoma/images
```

Then connect to `http://localhost:8080/`