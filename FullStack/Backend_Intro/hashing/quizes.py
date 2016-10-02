import hashlib

def hash_str(s):
    return hashlib.md5(s).hexdigest()

# -----------------
# User Instructions
# 
# Implement the function make_secure_val, which takes a string and returns a 
# string of the format: 
# s,HASH

def make_secure_val(s):
    code = s + ',' + hash_str(s)
    return code

#OR
def make_secure_val(s):
    return "%s,%s" % (s, hash_str(s))
    
print make_secure_val('alix')


#################################################################
# User Instructions
# 
# Implement the function check_secure_val, which takes a string of the format 
# s,HASH
# and returns s if hash_str(s) == HASH, otherwise None 

def check_secure_val(h):
    code = make_secure_val(h)
    if hash_str(code.split(',')[0]) == code.split(',')[1]:
        return code.split(',')[0]
    else:
        return 'nope'

#OR
def check_secure_val(h):
	val = h.split(',')[0]
	if h == make_secure_val(val):
		return val
    
print check_secure_val('alix')


##################################################################
import hmac

# Implement the hash_str function to use HMAC and our SECRET instead of md5
SECRET = 'imsosecret'
def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()
        
def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val



print check_secure_val('alix|7b7b78271f8734b8b156669ecd3a66d0')



###################################################################
import random
import string
import hashlib

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

# implement the function make_pw_hash(name, pw) that returns a hashed password 
# of the format: 
# HASH(name + pw + salt),salt
# use sha256

# Salt is used as 'secret' but is different for each stored name and pw combo

def make_pw_hash(name, pw):
    salt = make_salt()
    return hashlib.sha256(name+pw+salt).hexdigest()+','+salt
    
print make_pw_hash('alix', 'cool')



###################################################################
import random
import string
import hashlib

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

# Implement the function valid_pw() that returns True if a user's password 
# matches its hash. You will need to modify make_pw_hash.

def make_pw_hash(name, pw, salt):
    if salt == '':
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)

def valid_pw(name, pw, h):
    salt = h.split(',')[1]
    if make_pw_hash(name, pw, salt) == h:
        return True


h = make_pw_hash('spez', 'hunter2', '')
print valid_pw('spez', 'hunter2', h)
