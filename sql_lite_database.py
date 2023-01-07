import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("measure.db")

    def insert_data(self, lite_app_id, full_app_id):
        self.conn.execute("INSERT INTO lite_app (lite_app_id,full_app_id) "
                          "VALUES (?, ?)", (lite_app_id, full_app_id))
        self.conn.commit()

    def update_launch_time(self, lite_app_id, lite_launch_time, full_launch_time):
        self.conn.execute("UPDATE lite_app "
                          "SET lite_launch_time = ?, full_launch_time = ? "
                          "WHERE lite_app_id = ?", (lite_launch_time, full_launch_time, lite_app_id))
        self.conn.commit()

    def update_lite_launch_time(self, lite_app_id, lite_launch_time):
        self.conn.execute("UPDATE lite_app "
                          "SET lite_launch_time = ? "
                          "WHERE lite_app_id = ?", (lite_launch_time, lite_app_id))
        self.conn.commit()

    def update_full_launch_time(self, lite_app_id, full_launch_time):
        self.conn.execute("UPDATE lite_app "
                          "SET full_launch_time = ? "
                          "WHERE lite_app_id = ?", (full_launch_time, lite_app_id))
        self.conn.commit()

    def query_no_launch_time_app_pairs(self):
        cursor = self.conn.execute("SELECT lite_app_id, full_app_id "
                                   "FROM lite_app "
                                   "WHERE lite_launch_time is NULL "
                                   "or full_launch_time is NULL")
        return cursor


    def query_no_cpu_consumption_app_pairs(self):
        cursor = self.conn.execute("SELECT lite_app_id, full_app_id "
                                   "FROM lite_app "
                                   "WHERE lite_cpu_consumption is NULL "
                                   "or full_cpu_consumption is NULL")
        return cursor

    def query_no_memory_consumption_app_pairs(self):
        cursor = self.conn.execute("SELECT lite_app_id, full_app_id "
                                   "FROM lite_app "
                                   "WHERE lite_memory_consumption is NULL "
                                   "or full_memory_consumption is NULL")
        return cursor

    def query_no_resource_consumption_app_pairs(self):
        cursor = self.conn.execute("SELECT lite_app_id, full_app_id "
                                   "FROM lite_app "
                                   "WHERE lite_cpu_consumption is NULL "
                                   "or full_cpu_consumption is NULL "
                                   "or lite_memory_consumption is NULL "
                                   "or full_memory_consumption is NULL")
        return cursor

    def update_lite_memory_consumption(self, lite_app_id, lite_memory_consumption):
        self.conn.execute("UPDATE lite_app "
                          "SET lite_memory_consumption = ? "
                          "WHERE lite_app_id = ?", (lite_memory_consumption, lite_app_id))
        self.conn.commit()

    def update_full_memory_consumption(self, lite_app_id, full_memory_consumption):
        self.conn.execute("UPDATE lite_app "
                          "SET full_memory_consumption = ? "
                          "WHERE lite_app_id = ?", (full_memory_consumption, lite_app_id))
        self.conn.commit()

    def update_lite_cpu_consumption(self, lite_app_id, lite_cpu_consumption):
        self.conn.execute("UPDATE lite_app "
                          "SET lite_cpu_consumption = ? "
                          "WHERE lite_app_id = ?", (lite_cpu_consumption, lite_app_id))
        self.conn.commit()

    def update_full_cpu_consumption(self, lite_app_id, full_cpu_consumption):
        self.conn.execute("UPDATE lite_app "
                          "SET full_cpu_consumption = ? "
                          "WHERE lite_app_id = ?", (full_cpu_consumption, lite_app_id))
        self.conn.commit()
