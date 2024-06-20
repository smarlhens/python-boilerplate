def hello_world() -> str:
    return "Hello World"


def main() -> None:
    print(hello_world())  # noqa: T201 print only used as placeholder :)


if __name__ == "__main__":
    main()
