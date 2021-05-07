import subprocess

def main() -> None:
    """Start the bot."""

    # f0 = subprocess.Popen(['ngrok', 'http', '5000'])
    # os.system('curl http://localhost:4040/api/tunnels > tunnels')

    f1 = subprocess.Popen(['python3', 'flask_server.py'])
    f2 = subprocess.Popen(['python3', 'echobot.py'])

    # f0.wait()
    f1.wait()
    f2.wait()

if __name__ == '__main__':
    main()
