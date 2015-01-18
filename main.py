#!/usr/bin/env python
import os
import sys
import re
from xml.dom import minidom

doc = minidom.parse('test.xml')
root = doc.documentElement
nodes = root.childNodes

def show_xml(user=None):
	s1 = '''<IfModule mod_proxy.c>
        ProxyRequests On
        <Proxy *>
           AddDefaultCharset off
           #Require all denied
           #Require local
           Order deny,allow
           Deny from all''' + '\n'*2 + '#'*80 + '\n'
 
	s2 = '\n' + '#'*80 + '\n'*2 + '''       </Proxy>\n\n</IfModule> '''

	if user:
		s = get_user_list()
		if user in s:
			print s1
			user = '# ' + user
			for node in nodes:
				if node.nodeType == node.ELEMENT_NODE:	
					if node.getAttribute('name') == user:
						print node.getAttribute('name')
						for i in node.childNodes:
							if i.nodeType == node.ELEMENT_NODE:
								print i.childNodes[0].data
			print s2
		else:
			print "Errors!Don't have %s user!" % user 
	else:	
		print s1
		for node in nodes:
			if node.nodeType == node.ELEMENT_NODE:
				print node.getAttribute('name')
				for i in node.childNodes:
					if i.nodeType == node.ELEMENT_NODE:
						print i.childNodes[0].data 
		print s2

def create_conf():
	output=sys.stdout
	outputfile = open('./conf/proxy.conf', 'w')
	sys.stdout = outputfile
	show_xml()
	outputfile.close()
	sys.stdout = output

def delete_ip(ip):
	for node in nodes:
                if node.nodeType == node.ELEMENT_NODE:
                        for i in node.childNodes:
                                if i.nodeType == node.ELEMENT_NODE:
					if ip in i.childNodes[0].data:
						s = i.childNodes[0].data
						s = s.replace(ip,'')
					        i.childNodes[0].data = s	
	f = open('test.xml', 'w')
	doc.writexml(f)
	f.close()

def get_user_list():
	user_list = []
	for node in nodes:
		if node.nodeType == node.ELEMENT_NODE:
			username = node.getAttribute('name')[2:]
			user_list.append(username)	
	return user_list

if __name__ == '__main__':
	while True:
		user = raw_input('Input username:')
		show_xml(user)
  	#create_conf()
	#delete_ip('192.168.1.1')