docker stop spider
docker rm -f spider
docker restart spider
docker logs -f --tail 50 spider
docker run -d -p 8000:8000 -e PROJECT_NAME=spider -e OPENAPI_PREFIX=/spider-v /var/log/:/home/log/ --privileged=true --name spider cent:uvicorn_prod sh -c "cd /home/ && rm -rf spider && git clone http://renqk:11111111@120.27.45.57:18080/renqk/spider.git && bash /home/spider/scripts/start.sh"