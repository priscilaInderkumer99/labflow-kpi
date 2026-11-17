.PHONY: setup data kpis validate test metrics dashboard all

PY ?= python
export PYTHONPATH := src

setup:
	$(PY) -m pip install -e ".[dev]"

data:
	$(PY) -m labflow.cli generate

kpis:
	$(PY) -m labflow.cli kpis

validate:
	$(PY) -m labflow.cli validate

test:
	$(PY) -m pytest --junitxml=reports/junit.xml

metrics:
	$(PY) -m labflow.cli project-metrics

dashboard:
	$(PY) -m streamlit run dashboard/app.py

all: data validate kpis test metrics
