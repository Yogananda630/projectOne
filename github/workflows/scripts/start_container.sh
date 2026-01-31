#!/bin/bash
set -e

# Authenticate Docker with ECR
/usr/bin/aws ecr-public get-login-password --region us-east-1 | \
docker login --username AWS --password-stdin public.ecr.aws/g2a3v3g3

# Pull Docker image
/usr/bin/docker pull public.ecr.aws/g2a3v3g3/python/flask/repo:latest

# Stop old container (optional but best practice)
docker stop flask-app || true
docker rm flask-app || true

# Run container with NEW PORT
/usr/bin/docker run -d \
--name flask-app \
-p 9000:5000 \
public.ecr.aws/g2a3v3g3/python/flask/repo:latest
