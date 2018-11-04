#!/usr/bin/env python


###
# the following function creates a yaml object based on the values retrieved
#   from the directory. be sure to use spaces and not tabs or the YAML parser
#   from logstash will not be amused
###
def format_output(user_entry):
  entry_string = str(user_entry['samaccountname']) + ":\n"
  entry_string += "  dn: " + str(user_entry['distinguishedname']) + "\n"
  entry_string += "  displayname: " + str(user_entry['displayname']) + "\n"
  entry_string += "  memberof: " + "\n"
  for i in user_entry['memberof']:
    entry_string += "    - " + str(i) + "\n"
  return entry_string

###
# make sure we can work with AD and LDAP
###
from ldap3 import Server, Connection, ALL, NTLM

###
# import the connection information
# doesn't everyone separate usernames/passwords/etc from their scripts?!
###
import conn_info

###
# connect to the directory and then bind to it
# auto_bind saves an extra function call for the programmer
###
server = Server(conn_info.ad_server, get_info=ALL)
conn = Connection(server, conn_info.ad_search_user, conn_info.ad_search_pass, auto_bind=True, auto_range=True)
try:

  # out_string will grow with each object retrieved and will be written to file
  out_string = "" 

  # if you want to search for computer objects, change that here
  searchString = "(objectclass=user)"

  # begin retrieving items from the directory
  # paged_size is especially useful for older LDAPs and for Active Directory
  # a more eficient value owuld be 1000, since that's the maximum number AD will send back
  conn.search(conn_info.ad_search_base, searchString, attributes=conn_info.ad_search_props, paged_size = 500)
  for entry in conn.entries:
    out_string = out_string + format_output(entry)

  # LDAP specification says this is the magic number for the paging cookie
  cookie = conn.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']
  while(cookie):
    conn.search(conn_info.ad_search_base, searchString, attributes=conn_info.ad_search_props, paged_size = 500, paged_cookie = cookie)
    for entry in conn.entries:
      out_string = out_string + format_output(entry)
    cookie = conn.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']

  # in production you may want this to be a separate try/except loop
  # for testing and quick scripting/samples, it's sufficient for me
  # note this replaces whatever exists in that file...don't give
  #   world write access to this file and then run it as root!!
  out_fh = open('ad_users_file.yml', 'w')
  out_fh.write(out_string)
  out_fh.close()
except Exception as e:
  print("error: " + e)

exit()
