# secunda-test
```bash
docker-compose down -v
docker-compose up -d db
docker-compose exec db pg_isready -U postgres
docker-compose up -d web
docker-compose exec web alembic upgrade head
docker-compose exec web python -m app.scripts.seed_data
``` 


### Build & start all services:
```bash
docker-compose up -d --build
``` 
### Run migrations:
```bash
docker-compose exec web alembic upgrade head
``` 
### Seed the database with test data:
```bash
docker-compose exec web python -m app.scripts.seed_data
``` 
 ## ✅ Testing the API
```bash
chmod +x test_api.sh
./test_api.sh
``` 
```bash
curl -s -H "Accept: application/json" \
     -H "x-api-key: $API_KEY" \
     http://localhost:8000/buildings/ | jq
``` 


 ## 📖 API Documentation
Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc