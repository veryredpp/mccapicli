from .mccapicli import main


def run():
    while True:
        if main() == -1:
            break


if __name__ == "__main__":
    run()
