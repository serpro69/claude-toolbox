.ONESHELL:
.SHELL      := $(shell which bash)
.SHELLFLAGS := -ec

.PHONY: vendor-profiles test-structure

vendor-profiles:
	go test ./cmd/vendor-profiles/...
	go run ./cmd/vendor-profiles -manifest scripts/go-vendor-manifest.yml
	$(MAKE) test-structure

test-structure:
	bash test/test-plugin-structure.sh
