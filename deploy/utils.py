import jenkins
from jenkinsapi.build import Build
from mysite.settings import JENKINS_PROD_URL,JENKINS_PROD_PASS,JENKINS_PROD_USER,JENKINS_TEST_URL,JENKINS_TEST_USER, JENKINS_TEST_PASS


def get_server_instance(space):
	if space.code == 'PROD':
		jenkins_url = JENKINS_PROD_URL
		jenkins_user = JENKINS_PROD_USER
		jenkins_pass = JENKINS_PROD_PASS
	elif space.code == 'TEST':
		jenkins_url = JENKINS_TEST_URL
		jenkins_user = JENKINS_TEST_USER
		jenkins_pass = JENKINS_TEST_PASS
	else:
		jenkins_url = JENKINS_TEST_URL
		jenkins_user = JENKINS_TEST_USER
		jenkins_pass = JENKINS_TEST_PASS
	server = jenkins.Jenkins(jenkins_url, username=jenkins_user, password=jenkins_pass)
	return server


def build_job_branch_tag(space, job_name, branch_tag):
	try:
		server = get_server_instance(space)
		server.build_job(job_name, {"branch_tag": branch_tag})
	except Exception as e:
		print(e)


def get_job_build_result(space, job_name, build_number):
	try:
		server = get_server_instance(space)
		result = server.get_build_info(job_name, build_number)['result']
		return result
	except Exception as e:
		return None


def get_last_build_number(space, job_name):
	try:
		server = get_server_instance(space)
		last_build_number = server.get_job_info(job_name)['lastCompletedBuild']['number']
		return last_build_number
	except Exception as e:
		return None


def get_next_build_number(space, job_name):
	try:
		server = get_server_instance(space)
		next_build_number = server.get_job_info(job_name)['nextBuildNumber']
		return next_build_number
	except Exception as e:
		return None


def get_job_build_console_output(space, job_name, build_number):
	try:
		server = get_server_instance(space)
		build_info = server.get_build_console_output(job_name, build_number)
		return build_info
	except Exception as e:
		return None


def get_job_build_info(space, job_name, build_number):
	try:
		server = get_server_instance(space)
		build_info = server.get_build_info(job_name, build_number)
		return build_info
	except Exception as e:
		return None

#server.get_job_info(job_name)
#获取job名为job_name的job的最后次构建号
#server.get_job_info(job_name)['lastBuild']['number']
#获取job名为job_name的job的某次构建的执行结果状态
#server.get_build_info(job_name,build_number)['result']　　
#判断job名为job_name的job的某次构建是否还在构建中
#server.get_build_info(job_name,build_number)['building']
