# portscanner
simple python port scanner with command line and html output, can scan IP and port ranges or lists

# Examples:
  python script_name.py 192.168.1.10
  
  python script_name.py 192.168.1.* 80-85
 
  python script_name.py 192.168.1.45-67 80,81,82


# Output:

Port 80 open on 192.168.1.9

Port 8080 open on 192.168.1.9

Port 80 open on 192.168.1.12

Port 8080 open on 192.168.1.12


# HTML file (output.html):
<html><body><i><p><strong>./portscanner.py 192.168.1.9-12 80,8000,8080</strong></p>192.168.1.9: <a href="http://192.168.1.9:80" target="_blank">80</a> <a href="http://192.168.1.9:8080" target="_blank">8080</a> <br/>192.168.1.12: <a href="http://192.168.1.12:80" target="_blank">80</a> <a href="http://192.168.1.12:8080" target="_blank">8080</a> <br/></i></body></html>
