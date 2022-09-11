from database import conn, select, insert


class Data:
    def __init__(self):
        self.mydb = conn()

    def get_data(self, query, values):
        return select(query, values, self.mydb)

    def insert_data(self, query, val):
        return insert(query, val, self.mydb)
