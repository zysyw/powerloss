class PetFactory:
    def __init__(self):
        self._creators = {}

    def register_pet(self, pet_type):
        def decorator(creator):
            self._creators[pet_type] = creator
            return creator
        return decorator

    def get_pet(self, pet_type):
        creator = self._creators.get(pet_type)
        if not creator:
            raise ValueError(pet_type + ' is not registered!')
        return creator()

factory = PetFactory()

@factory.register_pet('dog')
class Dog:
    def __init__(self):
        self._name = 'Hope'

    def speak(self):
        return 'Woof!'

@factory.register_pet('cat')
class Cat:
    def __init__(self):
        self._name = 'Peace'

    def speak(self):
        return 'Meow!'

if __name__ == '__main__':
    d = factory.get_pet('dog')
    print(d.speak())  # Output: Woof!

    c = factory.get_pet('cat')
    print(c.speak())  # Output: Meow!
