
build:
	docker compose build

start:
	docker compose up -d

stop:
	docker compose down 

restart:
	docker compose restart

index:
	docker compose exec apiserver python manage.py build_index

shell:
	docker compose exec apiserver /bin/bash