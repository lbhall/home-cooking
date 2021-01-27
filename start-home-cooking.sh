#!/bin/bash
echo "Starting Home Cooking Functional Test Suite"
echo "Building..."
docker-compose build
echo "Bringing up containers..."
docker-compose up --detach
echo "Sleeping, waiting for containers to come up..."
sleep 25
echo "Loading recipe data..."
psql "postgresql://home_cooking_user:home_cooking_password@localhost:5405/home_cooking_test" -f create_schema.sql