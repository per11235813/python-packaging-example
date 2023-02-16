def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def hello():
    print("hello, world!")


def hello2():
    print(f"hello, world! {fib(14)=}")


if __name__ == "__main__":
    hello2()
