from src import DetectInkyBoard
from src.inkyimpressions.BuildInkyImpressionImages import BuildInkyImpressions


def main():
    board = DetectInkyBoard()
    x = BuildInkyImpressions()
    x.prepare_canvas()


if __name__ == '__main__':
    main()
