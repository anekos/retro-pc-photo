.PHONY: deploy
deploy:
	sam build
	sam deploy

.PHONY: lint
lint:
	cfn-lint template.yaml
