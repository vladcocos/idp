class Room():
    def __init___(self, room_id, room_type, capacity, bathroom, balcony, price):
        self.room_id = room_id
        self.room_type = room_type
        self.capacity = capacity
        self.bathroom = bathroom
        self.balcony = balcony
        self.price = price

class Booking():
    def __init___(self, room_id, first_name, last_name, check_in, check_out):
        self.room_id = room_id
        self.first_name = first_name
        self.last_name = last_name
        self.check_in = check_in
        self.check_out = check_out
