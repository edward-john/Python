
class MyClass:
    def __init__(self):
        self.method()
    def method(self):
        class SecondClass:
            def __init__(self):
                print(self.methodtwo())
            def methodtwo(self):
                return 'Wow you got me'
        SecondClass()

func = MyClass()
