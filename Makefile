LAB_PORT ?= 8888

.PHONY: jupyter-start jupyter-app jupyter-stop

jupyter-start:
	@nohup uv run jupyter lab deep_agent.ipynb --port $(LAB_PORT) > jupyterlab.log 2>&1 &
	@echo "JupyterLab starting on port $(LAB_PORT) — log: jupyterlab.log"

jupyter-app:
	@token=$$(uuidgen); \
	nohup uv run jupyter lab --port $(LAB_PORT) --no-browser --IdentityProvider.token="$$token" > jupyterlab.log 2>&1 & \
	for _ in $$(seq 1 60); do curl -sf -o /dev/null http://localhost:$(LAB_PORT)/api && break; sleep 0.5; done; \
	open -na "Google Chrome" --args --app="http://localhost:$(LAB_PORT)/lab/tree/deep_agent.ipynb?token=$$token"; \
	echo "JupyterLab starting on port $(LAB_PORT) in Chrome app mode — log: jupyterlab.log"

jupyter-stop:
	uv run jupyter lab stop $(LAB_PORT)
