#!/usr/bin/python
import Queue
import threading
import urllib2
import time
import sys

input_file = raw_input("Enter proxy file to be checked: ")
output_file = raw_input("Enter output file for checked proxies: ")
threads = input("Enter number of threads: ")
timeout = input("Enter the timeout in seconds for a proxy: ")

input = open(input_file, 'r')
output = open(output_file, 'a')

queue = Queue.Queue()

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
               			sock=urllib2.urlopen(req, timeout=timeout)
               			rs = sock.read(1000)
				total = total + 1
               			if 'this is a working proxy' in rs:
					found = found + 1
					print 'Proxy ' + counter + '/' + total + ' found:' + proxy_info
					output.write(proxy_info)
					output.flush()
			except:
				pass

			self.queue.task_done()

def main():

	for i in range(threads):
		t = ThreadUrl(queue)
		t.setDaemon(True)
		t.start()

	found = 0
	total = 0

	for line in input:
		queue.put(line.strip())

	queue.join()

main()
