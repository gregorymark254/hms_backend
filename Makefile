SERVICE := hms_backend

docker_login:
	sudo docker login registry.gitlab.com

docker_build:
	sudo docker build -t registry.gitlab.com/gregorymark25/hms_bc .

docker_push:
	sudo docker push registry.gitlab.com/gregorymark25/hms_bc

build_service: docker_login docker_build docker_push