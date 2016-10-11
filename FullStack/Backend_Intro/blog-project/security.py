#SECURITY
import hashlib
import hmac
import re

SECRET = 'imsosecret'

#Hash
def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()
#Make Secure Cookie
def make_secure_val(uid):
    return "%s|%s" % (uid, hash_str(uid))
#Check Cookie
def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val


#VERIFY EACH INPUT
def vname(username):
	USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
	if USER_RE.match(username):
		return ''
	else:
		return 'Invalid Username'
def vpass(pass1, pass2):
	PASS_RE = re.compile(r"^.{3,20}$")
	if pass1 and pass2:
		if (PASS_RE.match(pass1) and PASS_RE.match(pass2)) and (pass1 == pass2):
			return ''
		else:
			return 'Invalid Password and Verification'
	else: return 'Password and Verification Required'
def vemail(email):
	EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
	if not email or EMAIL_RE.match(email):
		return ''
	else:
		return 'Invalid Email'