import sys
import docker
from redis import Redis, RedisError

def check_docker_id(contain_id):
	client = docker.from_env()
	container = client.containers.list()
	for contain in container:
		if contain_id == contain.id:
			return True
	return False

def connect_to_redis(contain_id):
	try:
		redis = Redis()
	except RedisError:
		print("Error in connecting to redis server")
		sys.exit(1)
	client = docker.from_env()

	container = client.containers.get(contain_id)

	check_redis_cli = container.exec_run('redis-cli').exit_code
	if check_redis_cli != 0:
		print("Installing redis tools")
		container.exec_run('apt-get update')
		container.exec_run('apt-get install redis-tools -y')
	out = container.exec_run('redis-cli -h 172.21.0.1 ping')
	print(out.output)

if __name__ == '__main__':
	#passing container id in the command line argument
	container_id = sys.argv[1]
	if check_docker_id(container_id):
		connect_to_redis(container_id)
	else:
		print("Enter a running conatiner id")
