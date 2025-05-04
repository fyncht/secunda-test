# secunda-test

### docker-compose down -v
### docker-compose up -d db
### docker-compose exec db pg_isready -U postgres
### docker-compose up -d web
### docker-compose exec web alembic upgrade head
### docker-compose exec web python -m app.scripts.seed_data
