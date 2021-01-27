#!/bin/bash
echo "Starting Home Cooking Functional Test Suite"
echo "Building..."
docker-compose build
echo "Bringing up containers..."
docker-compose up --detach
echo "Sleeping, waiting for containers to come up..."