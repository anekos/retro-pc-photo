.PHONY: deploy
deploy: lint
	sam deploy

.PHONY: lint
lint:
	cfn-lint template.yaml
