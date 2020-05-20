import jenkins


JENKINS_TEST_URL = 'http://tjenkins.shudoon.com/'
JENKINS_TEST_USER = 'weidalian'
JENKINS_TEST_PASS = 'sys1991419'

def get_server_instance():
	jenkins_url = JENKINS_TEST_URL
	jenkins_user = JENKINS_TEST_USER
	jenkins_pass = JENKINS_TEST_PASS
	server = jenkins.Jenkins(jenkins_url, username=jenkins_user, password=jenkins_pass)
	return server


def build_job(job_name):
	try:
		server = get_server_instance()
		server.build_job(job_name)
	except Exception as e:
		print(e)


def get_job_build_result(space, job_name, build_number):
	try:
		server = get_server_instance(space)
		result = server.get_build_info(job_name, build_number)['result']
		return result
	except Exception as e:
		return None


def get_last_build_number(job_name):
	try:
		server = get_server_instance()
		last_build_number = server.get_job_info(job_name)['lastCompletedBuild']['number']
		return last_build_number
	except Exception as e:
		return None


def get_job_build_info(job_name, build_number):
	try:
		server = get_server_instance()
		build_info = server.get_build_info(job_name, build_number)
		return build_info
	except Exception as e:
		return None


job_name = 'test-env/tongfen-service_2'
print(get_last_build_number(job_name))
server = get_server_instance()
#get_last_build_number(job_name)
print(server.get_build_info(job_name,13)['duration'])
#print(next_bn)
#print(server.get_whoami())
#print(server.get_version())
#print(server.get_build_info(job_name,35)['result'])
#server.set_next_build_number(job_name, 28)
#java -jar jenkins-cli.jar -s http://tjenkins.shudoon.com/ -auth weidalian:11951d21e3d4af90c5a61dd0651abd1d66 -webSocket set-next-build-number test-env/sms-service_2 30
#print(help(server.set_next_build_number))
#build_job(job_name,{"branch_tag","refs/tags/v1.1.40"})
#print(server.get_build_console_output(job_name,23))
#server.build_job(job_name,{"branch_tag":"*/master"})
#获取job名为job_name的job的最后次构建号
#server.get_job_info(job_name)['lastBuild']['number']
#获取job名为job_name的job的某次构建的执行结果状态
#server.get_build_info(job_name,build_number)['result']　　
#判断job名为job_name的job的某次构建是否还在构建中
#server.get_build_info(job_name,build_number)['building']
