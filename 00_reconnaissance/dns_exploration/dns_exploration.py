# DNS exploration for common subdomains

import dns
import dns.resolver
import socket

def ReverseDNS(ip):
	try:
		result = socket.gethostbyaddr(ip)
		return [result[0]]+result[1]
	except socket.herror:
		return []

def DNSRequest(domain):
	try:
		result = dns.resolver.resolve(domain, 'A')
		if result:
			print(domain)
			for answer in result:
				print(answer)
				print("Domain Names: %s" % ReverseDNS(answer.to_text()))
	except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.Timeout, dns.resolver.LifetimeTimeout):
		pass 
	except Exception:
		pass

def SubdomainSearch(domain, dictionary, nums):
	for word in dictionary:
		subdomain = word+"."+domain
		DNSRequest(subdomain)
		if nums:
			for i in range(0,10):
				s = word+str(i)+"."+domain
				DNSRequest(s)

domain = "google.com" # Enter target domain here
d = "subdomains.txt" # Make sure you have your subdomains.txt at the right place
dictionary = []
with open(d,"r") as f:
	dictionary = f.read().splitlines()
SubdomainSearch(domain, dictionary, True)
