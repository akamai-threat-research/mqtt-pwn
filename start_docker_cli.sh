echo "running mqtt-pwn cli..."

if [[ $(docker-compose ps | grep "mqtt-pwn_db_1") ]]; then
    echo "db exists, skipping creation..."
else
    echo "db not exists, creating it..."
    docker-compose up --build --detach
fi

docker-compose run --rm cli