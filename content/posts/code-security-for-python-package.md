+++
title = 'Code Security Python Package'
date = 2026-01-23T17:52:39+07:00
draft = false
tags = ['python', ]
+++
# Code Security for Python Package

```
# audit
uv add --dev pip-audit
pip-audit

# available versions
pip index versions urllib3

# installed version
uv pip freeze | grep urllib3
poetry show urllib3

# why package is installed
uv tree --invert --package urllib3
poetry show --tree --why urllib3

# installs and adds to pyproject.toml
uv add urllib3~=1.2.3
poetry add urllib3~=1.2.3

# requirements.txt if needed
uv export --no-hashes > requirements.txt
poetry export --without-hashes --format=requirements.txt > requirements.txt

# after git pull
uv sync
poetry install --sync
```
