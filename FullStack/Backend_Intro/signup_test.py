import re

username = 'alix'
pass1 = 'alix'
pass2 = 'alix'
email = 'cavealix@gmail.com'

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    

def credentials(username, pass1, pass2, email):
	return [vname(username), vpass(pass1, pass2), vemail(email)]


def vname(username):
	if USER_RE.match(username):
		return True
	else:
		return False
	#if username and username.isalpha():
	#	return username
	#else:
	#	return 'Invalid Username'

def vpass(pass1, pass2):
	if pass1 and pass2:
		if (PASS_RE.match(pass1) and PASS_RE.match(pass2)) and (pass1 == pass2):
			return True
		else:
			return False
	else: return False

def vemail(email):
	if not email or EMAIL_RE.match(email):
		return True
	else:
		return False

print credentials(username, pass1, pass2, email)


#def vpass(pass1, pass2):
#	if pass1 and pass2:
#		if pass1.isalnum() and pass2.isalnum():
#			if pass1 == pass2:
#				return True
#			else: return False
#		else: return False
#	else: return False
	