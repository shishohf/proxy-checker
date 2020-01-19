#!/usr/bin/python
import Queue
import threading
import urllib2
import time
import sys

input_file = raw_input("Enter proxy file to be checked: ")
output_file = raw_input("Enter output file for checked proxies: ")
threads = input("Enter number of threads: ")

sys.stdout = open(output_file, 'a')

queue = Queue.Queue()
output = []

class ThreadUrl(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run(self):
		while True:
			proxy_info = self.queue.get()

			try:
	               		proxy_handler = urllib2.ProxyHandler({'http':proxy_info})
        	       		opener = urllib2.build_opener(proxy_handler)
               			opener.addheaders = [('User-agent','Mozilla/5.0')]
               			urllib2.install_opener(opener)
               			req = urllib2.Request("http://194.180.224.249")
               			sock=urllib2.urlopen(req, timeout= 7)
               			rs = sock.read(1000)
               			if 'this is a working proxy' in rs:
					output.append((proxy_info,''))
			except:
				pass

			self.queue.task_done()

def main():

	for i in range(threads):
		t = ThreadUrl(queue)
		t.setDaemon(True)
		t.start()

	hosts = [host.strip() for host in open(input_file).readlines()]

	for host in hosts:
		queue.put(host)

	queue.join()

main()
