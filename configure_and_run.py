import subprocess
import os
from pyngrok import ngrok

def main() -> None:
    """Start the bot."""

    http_tunnel = ngrok.connect(5000, bind_tls=True)
    f1 = subprocess.Popen(['python3', 'flask_server.py', http_tunnel.public_url])

    f1.wait()

if __name__ == '__main__':
    main()
