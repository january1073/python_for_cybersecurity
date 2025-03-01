# Test default credentials

import paramiko
import telnetlib

def SSHLogin(host, port, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=username, password=password)
        ssh_session = ssh.get_transport().open_session()
        if ssh_session.active:
            print("SSH login successful on %s:%s with username %s and password %s" % (host, port, username, password))
        ssh.close()
    except Exception as e:
        print(f"SSH connection failed: {e}")
        return

def TelnetLogin(host, port, username, password):
    try:
        user = bytes(username + "\n", "utf-8")
        passwd = bytes(password + "\n", "utf-8")

        tn = telnetlib.Telnet(host, port)
        tn.read_until(bytes("login: ", "utf-8"))
        tn.write(user)
        tn.read_until(bytes("Password: ", "utf-8"))
        tn.write(passwd)
        
        result = tn.expect([bytes("Last login", "utf-8")], timeout=2)
        if result[0] >= 0:
            print("Telnet login successful on %s:%s with username %s and password %s" % (host, port, username, password))
        tn.close()
    except EOFError:
        print(f"Login failed for {username}:{password}")
    except Exception as e:
        print(f"Telnet connection error: {e}")

host = "127.0.0.1"  # IP address 
with open("defaults.txt", "r") as f:  # Make sure you have your defaults.txt at the right place
    for line in f:
        vals = line.strip().split()
        if len(vals) < 2:
            continue
        username, password = vals[0], vals[1]
        SSHLogin(host, 22, username, password)
        TelnetLogin(host, 23, username, password)
