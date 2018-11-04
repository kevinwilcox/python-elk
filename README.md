# python-elk
This is a super-basic set of scripts to show "simple" ways to get data into or out of the Elastic stack using python.

It is made up of the following:

/tcp_data_to_elk:

This directory contains a sample python script to connect to a logstash instance and send arbitrary data via TCP.

It also contains a sample logstash configuration to accept data over TCP.

Note there is no TLS in this configuration!!

No additional logstash plugins need to be installed.

/crawl_ad_ldap:

This directory contains a sample python script (and its requisite config file) to crawl an Active Directory or LDAP instance, retrieve "person" objects and write specific attributes to a YAML file.

It also contains a sample logstash configuration to load that YAML file into a RAM table via the translate filter and search it any time a field called "username" is seen in log metadata.

Note it would take very few changes to retrieve computer objects to a second YAML file and create another table whenever a Workstation field is seen...

The script requires the ldap3 package for python, which can be installed via pip/pip3. No additional logstash plugins need to be installed.
