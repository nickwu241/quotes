HEROKU_APP_NAME=goody-quotes
LATEST_IMAGE:=$(HEROKU_APP_NAME):latest
DEV_PORT=8080

run:
	FLASK_ENV=development flask run

deploy: docker-build
	docker tag $(LATEST_IMAGE) registry.heroku.com/$(HEROKU_APP_NAME)/web
	docker push registry.heroku.com/$(HEROKU_APP_NAME)/web
	heroku container:release web --app $(HEROKU_APP_NAME)

docker-build:
	docker build --rm -f Dockerfile -t $(LATEST_IMAGE) .

docker-run:
	docker run --rm -it -p $(DEV_PORT):$(DEV_PORT) $(LATEST_IMAGE)
