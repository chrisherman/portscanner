import sys
import socket
import os
import pyfiglet

print(pyfiglet.figlet_format("PORT SCANNER", font="slant"))

def test_open_port(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex((ip, port))
        return result == 0

def generate_ips(target):
    if '*' in target:
        base_ip = target.replace('*', '{}')
        return [base_ip.format(i) for i in range(1, 256)]
    elif '-' in target:
        base_ip, range_end = target.split('-')
        base_parts = base_ip.split('.')
        start = int(base_parts[-1])
        end = int(range_end.split('.')[-1])
        return ['.'.join(base_parts[:-1] + [str(i)]) for i in range(start, end + 1)]
    else:
        return [target]

def generate_html_file(open_ports, cmd):
    with open("output.html", "w") as f:
        f.write("<html><head><title>Open Ports</title></head><body>")
        f.write(f"<h2>Command: {cmd}</h2>")
        for ip, ports in open_ports.items():
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                display_name = f"{ip} ({hostname})" if hostname != ip else ip
            except socket.herror:
                display_name = ip
            for port in ports:
                f.write(f"<p><a href='http://{ip}:{port}' target='_blank'>{display_name}:{port}</a></p>")
        f.write("</body></html>")


def parse_ports(ports_str):
    ports = []
    if "," in ports_str:
        for part in ports_str.split(","):
            if "-" in part:
                start, end = map(int, part.split("-"))
                ports.extend(range(start, end + 1))
            else:
                ports.append(int(part))
    elif "-" in ports_str:
        start, end = map(int, ports_str.split("-"))
        ports.extend(range(start, end + 1))
    else:
        ports.append(int(ports_str))
    
    return ports

def main(target, ports):
    open_ports = {}
    ips = generate_ips(target)
    total_ips = len(ips)

    progress_count = 0

    for ip in ips:
        open_ports[ip] = []
        for port in ports:
            sys.stdout.write(f"\rScanning {ip}:{port}...                 ")  # Pad to overwrite longer lines
            sys.stdout.flush()
            
            if test_open_port(ip, port):
                open_ports[ip].append(port)
                sys.stdout.write(f"\rPort {port} open on {ip}\n")
        
        progress_count += 1

    # Clear the last status message
    sys.stdout.write("\r" + " " * 50 + "\r")
    sys.stdout.flush()

    if open_ports:
        original_cmd = ' '.join(sys.argv)
        generate_html_file(open_ports, original_cmd)
        os.system('open output.html')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: script.py [IP or IP range with * or -] [optional ports or port ranges separated by ,]")
        sys.exit(1)
    
    target_ip = sys.argv[1]
    target_ports = parse_ports(sys.argv[2]) if len(sys.argv) > 2 else [80]

    main(target_ip, target_ports)
