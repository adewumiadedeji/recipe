# Define variables for services and Docker registry
SERVICES = auth gateway ingredient mealplan rating recipe notification
REGISTRY = deeaxfun2

# Default target
.PHONY: all
all: build push deploy

# Build all services
.PHONY: build
build: $(SERVICES:%=build-%)

# Push all services
.PHONY: push
push: $(SERVICES:%=push-%)

# Deploy Kubernetes configuration
.PHONY: deploy
deploy:
	cd kubernetes && kubectl apply -f .

# Restart Kubernetes pods
.PHONY: refresh
refresh:$(SERVICES:%=refresh-%)

# Define build and push targets for each service
$(SERVICES:%=build-%): build-%:
	cd services/$* && docker build --platform linux/amd64 -t $*:latest .

$(SERVICES:%=push-%): push-%:
	cd services/$* && docker tag $*:latest eu-stockholm-1.ocir.io/axyklytnjcih/recipe-repo/$*:latest
	cd services/$* && docker push eu-stockholm-1.ocir.io/axyklytnjcih/recipe-repo/$*:latest

$(SERVICES:%=refresh-%): refresh-%:
	kubectl rollout restart deployment/$*-deployment

# Individual service build
.PHONY: $(SERVICES:%=build-%)
# Individual service push
.PHONY: $(SERVICES:%=push-%)
# Individual service restart
.PHONY: $(SERVICES:%=refresh-%)
