init: clean
	uv run manage.py collectstatic --noinput

web: clean
	uv run manage.py collectstatic --noinput
	docker build --no-cache -t my-site-web:latest -f Dockerfile.web .

docker:
	docker build --no-cache -t my-site:latest .


docker-run:
	docker run -d --rm -p 8000:8000 my-site:latest


clean:
	rm -rf ./staticfiles