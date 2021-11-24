class Animal:
    def __init__(self, diet, height, weight, age):
        self.diet = diet
        self.height = height
        self.weight = weight
        self.age = age

    def get_height(self):
        return self.height


if __name__ == "__main__":
        sloth = Animal("leaves", 12, 13, 10)
        monkey = Animal("bananas", 3, 4, 2)
        print("Height of sloth : ", sloth.get_height())

