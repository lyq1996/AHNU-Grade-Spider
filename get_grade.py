# -*-coding:utf-8-*-
import urllib2
import cookielib
import re
import string
import sys
cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
def login(us,ps):
	req = urllib2.Request('http://jwgl.ahnu.edu.cn/login/check.shtml',data = 'user=%s&pass=%s&usertype=stu'%(us,ps))
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0')
	content = opener.open(req).read()
	if 'fail' in content:
		print u'登录失败...'
		return False
	else:
		print u'登录成功...'
		return True
def getlist(y,st):
	if y == '0':
		year = '0000-0000'
		semester = st
	else:
		yearadd1 = int(y)+1
		year = y+'-'+str(yearadd1)
		semester = st
	req2 = urllib2.Request('http://jwgl.ahnu.edu.cn/query/cjquery/index?action=ok&xkxn=%s&xkxq=%s'%(year,semester))
	req2.add_header('Referer','http://jwgl.ahnu.edu.cn/')
	content = opener.open(req2).read().decode('utf-8')
	if u'平时成绩公示' in content:
		reg = re.compile('<td align="left">(.+?)</td>\s*<td>.*?</td>\s*<td>.*?</td>\s*<td>(.*?)</td>\s*<td>.*?</td>\s*<td>.*?</td>\s*<td>.*?</td>\s*<td>(.*?)</td>\s*<td>.*?</td>\s*<td>.*?</td>\s*</tr>')
	else:
		reg = re.compile('<td align="left">(.+?)</td>\s*<td>.*?</td>\s*<td>.*?</td>\s*<td>(.*?)</td>\s*<td>.*?</td>\s*<td>.*?</td>\s*<td>(.*?)</td>\s*<td>.*?</td>\s*<td>.*?</td>\s*</tr>')
	chengji = re.findall(reg,content)
	if len(chengji)==0:
		print u'并未查询到..请检查参数..'
	class_name = []
	credit = []
	grade = []
	grade2 = []
	for i in chengji:
		class_name.append(i[0])
		credit.append(i[1])
		grade.append(i[2])
	for i in grade:
		if i =='':
			i = u'暂无成绩'
			grade2.append(i)
		else:
			grade2.append(i)
	return [class_name, grade2, credit]
def display(result):
	name = result[0]
	grade = result[1]
	credit = result[2]
	for i in range(len(name)):
		str1 = u'课程名称:%s' % (name[i])
		str2 = u'成绩:%s'% (grade[i])
		str3 = u'学分:%s\n'% (credit[i])
		print str1
		print str2
		print str3
if len(sys.argv) == 9:
	if sys.argv[1] == '-u' and sys.argv[3] == '-p' and sys.argv[5] == '-y' and sys.argv[7] == '-g':
		u = sys.argv[2]
		p = sys.argv[4]
		if login(u,p) is True:
			y = sys.argv[6]
			st = sys.argv[8]
			print u'正在努力查询中...'
			result = getlist(y,st)
			display(result)
		else:
			print u'你输入的用户名和密码有错..'
	else:
		print u'Usage <-u username -p password -y firstyears -g grade!>'
else:
	print u'Usage <-u username -p password -y firstyears -g grade!>'