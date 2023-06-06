import requests

def get_public_ip():
    response = requests.get('https://api.ipify.org')
    return response.text

def main():
    ip_file = 'last_ip.txt'
    current_ip = get_public_ip()

    try:
        with open(ip_file, 'r') as f:
            last_ip = f.read()
    except FileNotFoundError:
        last_ip = ''

    if current_ip != last_ip:
        print(f"IP has changed from {last_ip} to {current_ip}")
    else:
        print('IP is not changed')

    with open(ip_file, 'w') as f:
        f.write(current_ip)

if __name__ == "__main__":
    main()