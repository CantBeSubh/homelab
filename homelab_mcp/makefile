run:
	uv run main.py

proxy-run:
	uv run fastmcp_proxy.py

dbuild:
	@echo "Building..."
	docker build -t homelab-mcp:latest .


drun:
	@echo "Running..."
	docker run --rm --env-file ./.env --name homelab-mcp homelab-mcp


dpush:
	@echo "Getting git commit hash..."
	$(eval COMMIT_HASH := $(shell git rev-parse --short HEAD))
	@echo "Building..."
	docker build -t holyc0w/homelab-mcp:${COMMIT_HASH} -t holyc0w/homelab-mcp:latest .
	@echo "Pushing..."
	docker push holyc0w/homelab-mcp:${COMMIT_HASH}
	docker push holyc0w/homelab-mcp:latest


debug:
	bunx @modelcontextprotocol/inspector