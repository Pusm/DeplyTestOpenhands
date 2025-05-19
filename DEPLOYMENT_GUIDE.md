# Deployment Guide

## Prerequisites
- Docker installed on host machine
- Proper permissions to run Docker commands

## Building the Container
```bash
docker build -t fullstack-app .
```

## Running the Container
```bash
docker run -d \
  -p 54935:54935 \
  -p 59175:59175 \
  --name fullstack-app \
  fullstack-app
```

## Accessing the Application
- Frontend: http://localhost:59175
- Backend API: http://localhost:54935

## Production Considerations
1. Use a reverse proxy (Nginx) in front
2. Configure proper logging
3. Set up monitoring
4. Use Docker Compose for multi-container setups
5. Consider database containerization if needed

## Troubleshooting
- Check logs: `docker logs fullstack-app`
- Verify ports: `docker port fullstack-app`
- Inspect running container: `docker exec -it fullstack-app sh`