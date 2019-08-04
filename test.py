class abc():
    def f1(self):
        print ("f1")

    def f2(self):
        print("f2")
        self.f1()

a = abc()
a.f2()
