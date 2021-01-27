#!/bin/bash
start-home-cooking.sh
echo "Sleeping, waiting for containers to come up..."
sleep 25
echo "Loading recipe data..."
psql "postgresql://home_cooking_user:home_cooking_password@localhost:5405/home_cooking_test" -f create_schema.sql
echo "Stopping containers..."
docker-compose down
echo "Tests Done..."