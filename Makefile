.PHONY: vendor-go test-structure

vendor-go:
	go run ./cmd/vendor-profiles -manifest scripts/go-vendor-manifest.yml
	bash test/test-plugin-structure.sh

test-structure:
	bash test/test-plugin-structure.sh
