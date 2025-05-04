#!/usr/bin/env bash
API_KEY="SECRETLOVELYAPIKEY"

# helper: запрос + "красивый" UTF-8 JSON
call() {
  local method=$1 path=$2
  echo -e "\n=== $method $path ==="
  curl -s -X $method "http://localhost:8000$path" \
    -H "Accept: application/json" \
    -H "x-api-key: $API_KEY" \
  | python3 -c 'import sys, json; print(json.dumps(json.load(sys.stdin),ensure_ascii=False,indent=2))' \
    || echo "!!! не удалось распарсить JSON"
}

# 1) Все здания
call GET /buildings/

# 2) Орги в здании #1
call GET /buildings/1/organizations

# 3) Все организации
call GET /organizations/

# 4) Организация по ID=1
call GET /organizations/1

# 5) Поиск по части названия "Копыта"
echo -e "\n=== GET /organizations/?name=Копыта ==="
curl -s -G "http://localhost:8000/organizations/" \
  -H "Accept: application/json" \
  -H "x-api-key: $API_KEY" \
  --data-urlencode "name=Копыта" \
| python3 -c 'import sys, json; print(json.dumps(json.load(sys.stdin),ensure_ascii=False,indent=2))'

# 6) По виду деятельности activity_id=1
call GET "/organizations/?activity_id=1"

# 7) По радиусу (Москва, R=100 км)
call GET "/organizations/?lat=55.7558&lng=37.6173&radius=100"

# 8) По прямоугольнику
call GET "/organizations/?min_lat=55&max_lat=56&min_lng=37&max_lng=38"

# 9) Все виды деятельности
call GET /activities/

# 10) Орги по ровно activity_id=1
call GET /activities/1/organizations

# 11) Орги по activity_tree=1
call GET /activities/1/organizations_tree
