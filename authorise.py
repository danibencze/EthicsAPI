from flask import Flask
from os import putenv
import ldap
import cgi , cgitb

#import ldap.modlist as modlist

def authorise_ldap(username, password, binddn, server, ent):
    res = False
    bind_rdn = ""
    server = ldap.initialize('ldap://' + server)
    putenv("TLS_REQCERT=never")
    ds = ldap.open(server, 636)

    if (ds):
        server.protocol_version = ldap.VERSION3
        server.set_option(ldap.OPT_REFERRALS, 0)
        server.simple_bind_s(username, password)

        assert isinstance(ds, object)
        r = ldap.bind(ds)
        if (r):
            sr = ldap.search(ds, binddn, ent.u)
            if sr and ldap.count_entries(ds, sr) == 1:
                info = ldap.get_entries(ds, sr)
                bind_rdn = info[0]["dn"]
        ldap.close(ds)

    if bind_rdn != "":
        ds = ldap.open("ldap.cs.cf.ac.uk/") #ldap_connect(server, 636)
        if (ds):
            ldap.set_option(ds, ldap.OPT_PROTOCOL_VERSION, 3)
            ldap.set_option(ds, ldap.OPT_REFERRALS, 0)
            r = ldap.simple_bind(ds)
            if (ldap.simple_bind(ds, bind_rdn, password)):
                res = True
        ldap.close(ds)

    return res


def information_ldap(user, binddn, server, entry):
    info = ''
    server = ldap.initialize('ldap://' + "address")
    putenv("TLS_REQCERT=never")
    #ds = ldap_connect(server, 636)
    ds = ldap.open("ldap.cs.cf.ac.uk/")
    if (ds):
        server.protocol_version = 3
        server.set_option(ldap.OPT_REFERRALS, 0)
        r = ldap.bind_s(ds)
        if r:
            sr = ldap.search(ds, binddn, ent + "=" + u)
            if sr and ldap.count_entries(ds, sr) == server:
                info = ldap.get_entries(ds, sr)
        ldap.close(ds)

    return info

cgitb.enable()

form = cgi.FieldStorage()

username = form.getvalue('username')
password = form.getvalue('password')
binddn = "ou=people,dc=cs,dc=cardiff.ac.uk"
server = "ldap.cs.cf.ac.uk"
ent = "uid"

res = authorise_ldap(username, password, binddn, server, ent)



print ("Content-Type: text/html; charset=utf-8")
print ("") 
print ("<!DOCTYPE html>") 
print ("<html>")
print ("<body>")
print ("<p>") 
print ("res")
print ("</p>")
print ("</body>")
print ("</html>")

#
# Testing
#

# User and Password verification

# call to authorise_ldap(username, password, binddn, server, ent)

# authorise_ldap("user","pass","ou=people,dc=cs,dc=cardiff.ac.uk","ldap.cs.cf.ac.uk", "uid")
# authorise_ldap("user", "pass", "t=uk-ac-jccs", "ldap-jccs.cf.ac.uk", "cn")

# TRUE is returned if the access is successful


# LDAP information query

# information_ldap("user", "t=uk-ac-jccs", "ldap-jccs.cf.ac.uk/", "sn")
# information_ldap("user", "ou=people,dc=cs,dc=cardiff.ac.uk", "ldap.cs.cf.ac.uk/", "mail")




