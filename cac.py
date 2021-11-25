class Cities:
    def __init__(self, user1, user2):
        self.city_user = [user1, user2]
        self.current_step = 0
        self.user_cities = []
        self.last_char = None

    def is_correct_first_char(self, char):
        return self.last_char is None or char == self.last_char

    def is_unused_city(self, city):
        return city in self.used_cities


    def change_last_char(self, city):
        unchar = ["ы", "й", "ъ", "ь", "ы"]
        for char in city[::-1]:
            if char not in unchar:
                self.last_char = char
                break

