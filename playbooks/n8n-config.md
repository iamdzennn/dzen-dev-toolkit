# n8n Server Setup (Context File for ChatGPT)

Server:
- Hetzner Cloud VM
- Ubuntu 24.04.3 LTS
- Hostname: voora-n8n
- Public DNS: n8n.voora.live
- Public IPv4: 46.62.225.46
- SSH: ssh root@n8n.voora.live

Deployment:
- n8n runs as a single Docker container
- No docker-compose
- No reverse proxy
- No HTTPS/TLS
- UI URL: http://n8n.voora.live:5678/

Docker:
- Container name: n8n
- Docker image: n8nio/n8n:latest
- Port mapping: 5678:5678
- Persistent data stored on host: /root/.n8n
- Persistent data mounted into container: /home/node/.n8n
- Env variable: N8N_SECURE_COOKIE=false

Canonical run command:
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v /root/.n8n:/home/node/.n8n \
  -e N8N_SECURE_COOKIE=false \
  n8nio/n8n:latest

Useful Docker commands:
docker ps
docker stop n8n
docker rm n8n
docker pull n8nio/n8n:latest

Notes:
- All n8n data persists in /root/.n8n
- To update, pull new image, stop container, remove container, rerun with same command
- Cookie security is disabled intentionally due to HTTP-only setup