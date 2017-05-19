class Fibonacci:
    n = None
    fibonacci_list = None

    def __init__(self, n):
        try:
            self.n = abs(int(float(n)))
            self.fibonacci_list = list()
        except ValueError:
            raise ValueError('Write correct element number, NOT STRING')
        self._start()

    def __str__(self):
        text = ''
        for index, fibonacci_number in self.fibonacci_list:
            text += '{i:3}: {f:3}'.format(i=index, f=fibonacci_number) + '\n'
        return text

    def _fib(self):
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

    def _start(self):
        for index, fibonacci_number in enumerate(self._fib()):
            self.fibonacci_list.append((index, fibonacci_number))
            if index == self.n:
                break

if __name__ == '__main__':
    print(Fibonacci(10))
