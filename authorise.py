import ldap
#import os
from flask import Flask
from requests.auth import HTTPDigestAuth

def authorise_ldap(username, password, binddn, server, ent):
	res = false
	bind_rdn = ""
	server = ldap.initialize('ldap://' + 'ldapserver')
  putenv("TLS_REQCERT=never")
	ds = ldap_connect(server, 636)
	if (ds):
 		server.protocol_version = ldap.VERSION3
 		server.set_option(ldap.OPT_REFERRALS, 0)
    #server.simple_bind_s(binddn, passwor)

 		r = ldap_bind(ds)
 		if (r):
   			sr = ldap_search(ds, binddn, ent.u)
   			if sr and ldap_count_entries(ds, sr) == 1:
          info = ldap_get_entries(ds, sr)
          bind_rdn = info[0]["dn"]
    ldap_close(ds)
 	
  if bind_rdn != "":
 		ds = ldap_connect(server, 636)
 		if (ds):
 			ldap_set_option(ds, LDAP_OPT_PROTOCOL_VERSION, 3)
   		ldap_set_option(ds, LDAP_OPT_REFERRALS, 0)
   		r = ldap_bind(ds)
   		if (ldap_bind(ds, bind_rdn, password)):
     			res = true
    ldap_close (ds)
  
  return res

def information_ldap(user, binddn, server, entry):
	info = NULL
 	server = ldap.initialize('ldap://' + address)
 	putenv("TLS_REQCERT=never")
 	ds = ldap_connect(server, 636)
 	if (ds):
    server.protocol_version = 3
    server.set_option(ldap.OPT_REFERRALS, 0)
    r = ldap_bind(ds)
   		if r:
     	  sr = ldap_search(ds, binddn, ent. "=".u)
     		if sr and ldap_count_entries(ds, sr) == 1
       			info = ldap_get_entries(ds, sr)
      ldap_close(ds)

  return info




#
# Testing
#

# User and Password verification

# call to authorise_ldap(username, password, binddn, server, ent)

         authorise_ldap("user","pass","ou=people,dc=cs,dc=cardiff.ac.uk","ldap.cs.cf.ac.uk", "uid")
         authorise_ldap("user", "pass", "t=uk-ac-jccs", "ldap-jccs.cf.ac.uk", "cn")

# TRUE is returned if the access is successful



# LDAP information query

 information_ldap("user", "t=uk-ac-jccs", "ldap-jccs.cf.ac.uk/", "sn")
 information_ldap("user", "ou=people,dc=cs,dc=cardiff.ac.uk", "ldap.cs.cf.ac.uk/", "mail")






