###
# A really 'simple' script to connect to a logstash instance using a TCP listener
# This connects over IPv4 and can use either a hostname (that the system can resolve)
#   or an IP address
###

###
# only needed because of json.dumps
# if you create a JSON string without using json.dumps then this is unnecessary
###
import json

###
# necessary for the network connection to work
###
import socket

###
# this can be an IP address or any hostname the system can resolve via DNS
###
ls_server_host = '1.2.3.4'

###
# this will usually be a high-numbered port (> 1024)
###
ls_server_port = 1234

###
# .connect() would really look like .connect((host, port))
# to me this is cleaner to debug at 3.30 AM
###
ls_connect_string = (ls_server_host, ls_server_port)

###
# an example of how a dictionary with two items would look
# in production a dictionary may be an entire log event with dozens of fields
# it may also be as simple as a single message field
###
sample_message  = { 'user_name':      'Demo User',
                    'email_address':  'demo@my-email-domain.com' }

###
# this converts the dictionary to a json string
# if building msg manually as a properly-formatted json object,
#   this may be unnecessary
# the new-line at the end of each json string is required for logstash
#   to parse it correctly
###
msg = json.dumps(sample_message) + "\n"

###
# this actually creates the socket *and leaves it open*
# there are other ways to send data (e.g., sendto()) that do
#   not require leaving a socket open
# I like this approach because I can create as many messages as
#   I want and send them over a single TCP session
# this should be wrapped in a 'try'/'except' block!!
###
simple_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
simple_socket.connect(ls_connect_string)
simple_socket.sendall(msg.encode('utf-8'))
simple_socket.close()

exit()
