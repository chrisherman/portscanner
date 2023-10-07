import pyfiglet, os
print(pyfiglet.figlet_format("PORT SCANNER", font="slant"))

import socket
import sys
import webbrowser
from concurrent.futures import ThreadPoolExecutor

def test_open_port(ip, port, timeout=1):
    """Test if port is open."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            s.connect((ip, port))
            return True
        except (socket.timeout, socket.error):
            return False

def generate_html_file(ip_port_mapping, original_cmd):
    """Generate an HTML file with the IPs and ports as clickable links."""
    with open("output.html", "w") as file:
        file.write("<html><body>")
        file.write(f"<p><strong>{original_cmd}</strong></p><br/>")
        for ip, ports in ip_port_mapping.items():
            file.write(f"{ip}: ")
            for port in ports:
                link = f"http://{ip}:{port}"
                file.write(f'<a href="{link}" target="_blank">{port}</a> ')
            file.write('<br/>')
        file.write("</body></html>")


def generate_ips(target):
    """Generate a list of IPs based on the provided target."""
    if '*' in target:
        base_ip = target.split('.')[0:3]
        return [f"{'.'.join(base_ip)}.{i}" for i in range(1, 256)]
    elif '-' in target:
        base_ip, ip_range = target.rsplit('.', 1)
        start, end = map(int, ip_range.split('-'))
        return [f"{base_ip}.{i}" for i in range(start, end+1)]
    else:
        return [target]

def generate_ports(port_arg):
    """Generate a list of ports based on the provided argument."""
    if ',' in port_arg:
        return list(map(int, port_arg.split(',')))
    elif '-' in port_arg:
        start, end = map(int, port_arg.split('-'))
        return list(range(start, end+1))
    else:
        return [int(port_arg)]

def main(target, ports):
    open_ports = {}
    ips = generate_ips(target)

    # Scan IPs for open ports using threads for faster scanning
    for ip in ips:
        open_ports_for_ip = []
        for port in ports:
            if test_open_port(ip, port):
                print(f"Port {port} open on {ip}")
                open_ports_for_ip.append(port)
        if open_ports_for_ip:
            open_ports[ip] = open_ports_for_ip

    # Generate an HTML file with open port IPs
    if open_ports:
        original_cmd = ' '.join(sys.argv)
        generate_html_file(open_ports, original_cmd)

        # Open the generated HTML file in the default web browser
        os.system('open output.html')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <IP_address_or_range_or_wildcard> [port_or_range_or_list]")
        print("\nExamples:")
        print("  python script_name.py 192.168.1.10")
        print("  python script_name.py 192.168.1.* 80-85")
        print("  python script_name.py 192.168.1.45-67 80,81,82")
        sys.exit(1)

    target = sys.argv[1]
    ports_arg = sys.argv[2] if len(sys.argv) > 2 else "80"
    ports = generate_ports(ports_arg)

    main(target, ports)

