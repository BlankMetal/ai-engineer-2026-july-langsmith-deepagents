LAB_PORT ?= 8888

.PHONY: start stop

start:
	@nohup uv run jupyter lab deep_agent.ipynb --port $(LAB_PORT) > jupyterlab.log 2>&1 &
	@echo "JupyterLab starting on port $(LAB_PORT) — log: jupyterlab.log"

stop:
	uv run jupyter lab stop $(LAB_PORT)
