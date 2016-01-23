# /usr/bin/python
# coding=utf-8
'''help me to git add changes '''
from gittle import Gittle
import  sys

conf = [
    ['/home/zhang/www/php', 'git@git.oschina.net:tianyunchong/php.git']
]
for con in conf:
	repo = Gittle(con[0], con[1])
	#拉取远程代码到本地
	key_file = open("/home/zhang/.ssh/id_rsa")
	repo.auth(key_file)
	repo.pull(con[1], "origin/master")
	sys.exit()
	untracks = repo.untracked_files
	if not untracks:
		print "暂时没有文件新增!"
	changes = repo.modified_files
	print changes