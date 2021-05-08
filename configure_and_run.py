import subprocess
import os
from pyngrok import ngrok

def main() -> None:
    """Start the bot."""

    http_tunnel = ngrok.connect(5000, bind_tls=True)
    # f2 = subprocess.Popen(['python3', 'echobot.py', http_tunnel.public_url])
    f1 = subprocess.Popen(['python3', 'flask_server.py', http_tunnel.public_url])

    # f0.wait()
    f1.wait()
    # f2.wait()

if __name__ == '__main__':
    main()
