## Setup

### venv
```bash
mv pyproject.pip.toml pyproject.toml
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
mv pyproject.toml pyproject.pip.toml
```

### pyenv and poetry
```bash
mv pyproject.poetry.toml pyproject.toml
pyenv virtualenv 3.10.4 trame_optimeyes
pyenv activate trame_optimeyes
poetry install
mv pyproject.toml pyproject.poetry.toml
```

## Run application

```bash
optimeyes --server --hot-reload --batch ./data/REFUGE_pure/glaucoma/images

# poetry
mv pyproject.poetry.toml pyproject.toml
poetry run optimeyes --server --hot-reload --batch ./data/REFUGE_pure/glaucoma/images
mv pyproject.toml pyproject.poetry.toml
```

Then connect to `http://localhost:8080/`