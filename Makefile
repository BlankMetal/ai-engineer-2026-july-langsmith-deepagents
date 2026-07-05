LAB_PORT ?= 8888

.PHONY: jupyter-start jupyter-stop

jupyter-start:
	@nohup uv run jupyter lab deep_agent.ipynb --port $(LAB_PORT) > jupyterlab.log 2>&1 &
	@echo "JupyterLab starting on port $(LAB_PORT) — log: jupyterlab.log"

jupyter-stop:
	uv run jupyter lab stop $(LAB_PORT)
