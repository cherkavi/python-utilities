# pip3 install docker
import docker
print(docker.from_env().containers.list())
