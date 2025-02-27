# Scapy port scanner

from scapy.all import *

ports = [25,80,53,443,445,8080,8443] # Ports to be scanned

def SynScan(host):
	ans,unans = sr(IP(dst=host)/TCP(sport=5555,dport=ports,flags="S"),timeout=2,verbose=0) # Send specified packets to defined ports and wait for replies, answered (open) and unanswered
	print("Open ports at %s:" % host)
	for (s,r,) in ans:
		if s[TCP].dport == r[TCP].sport: # Verify that we receive a response from a port where we sent a packet to
			print(s[TCP].dport) # Display the result, which ports are open

def DNSScan(host):
	ans,unans = sr(IP(dst=host)/UDP(sport=5555,dport=53)/DNS(rd=1,qd=DNSQR(qname="google.com")),timeout=2,verbose=0) # DNS query for google.com
	if ans:
		print("DNS Server at %s"%host)

host = "8.8.8.8" # Google DNS server

SynScan(host)
DNSScan(host)
