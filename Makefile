
build:
	docker compose build

start:
	docker compose up -d

stop:
	docker compose down 

restart:
	docker compose restart

index:
	python indexwiki.py