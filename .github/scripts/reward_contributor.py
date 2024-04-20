import sys


def main():
    modified_files = sys.argv[1:]
    for file in modified_files:
        print(file)


if __name__ == "__main__":
    main()