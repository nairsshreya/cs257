class Tester:
    def __init__(self):
        self.temp1 = 10
    def changer(self):
         self.temp1 = self.temp1 + 1


test1 = Tester()
print(test1.temp1)
test1.changer()
print(test1.temp1)