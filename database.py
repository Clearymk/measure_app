import time
import pymysql


class DataBase(object):
    def __init__(self, database="lite_app") -> None:
        try:
            self.mysql = pymysql.connect(host='10.19.124.172',
                                         port=10255,
                                         user='root',
                                         password='catlab1a509',
                                         database=database)
        except Exception:
            time.sleep(2)
            self.__init__()

    def insert_data(self, lite_app_id, full_app_id):
        insert_sql = "INSERT INTO lite_app.app_measure (lite_app_id,full_app_id) VALUES (%s, %s)"
        cursor = self.mysql.cursor()
        cursor.execute(insert_sql, (lite_app_id, full_app_id))
        self.mysql.commit()

    def update_lite_launch_time(self, lite_app_id, lite_launch_time):
        insert_sql = "update lite_app.app_measure set lite_launch_time = %s where lite_app_id = %s"
        cursor = self.mysql.cursor()
        cursor.execute(insert_sql, (lite_launch_time, lite_app_id))
        self.mysql.commit()

    def update_full_launch_time(self, lite_app_id, full_launch_time):
        insert_sql = "update lite_app.app_measure set full_launch_time = %s where lite_app_id = %s"
        cursor = self.mysql.cursor()
        cursor.execute(insert_sql, (full_launch_time, lite_app_id))
        self.mysql.commit()

    def query_no_launch_time_app_pairs(self):
        cursor = self.mysql.cursor()
        cursor.execute("select lite_app_id, full_app_id "
                       "from lite_app.app_measure  "
                       "where lite_launch_time is null "
                       "or full_launch_time is null ")

        return cursor.fetchall()

    def query_all_pairs(self):
        cursor = self.mysql.cursor()
        cursor.execute("select lite_app_id, full_app_id "
                       "from lite_app.app_measure ")

        return cursor.fetchall()

    def query_no_resource_consumption_app_pairs(self):
        cursor = self.mysql.cursor()
        cursor.execute("select lite_app_id, full_app_id "
                       "from lite_app.app_measure  "
                       "where (lite_cpu_time is null "
                       "or full_cpu_time is null "
                       "or lite_memory_usage is null "
                       "or full_memory_usage is null)")

        return cursor.fetchall()

    def query_re_run(self):
        cursor = self.mysql.cursor()
        cursor.execute("select lite_app_id, full_app_id "
                       "from lite_app.app_measure "
                       "where id >= 131 and id <= 260 and (xapk != 10 or xapk is null)")
        return cursor.fetchall()

    def launch_time_task(self):
        cursor = self.mysql.cursor()
        cursor.execute("select lite_app_id, full_app_id "
                       "from lite_app.app_measure "
                       "where (xapk != 3 and xapk != 5) or xapk is null;")
        return cursor.fetchall()

    def query_memory_bug(self):
        cursor = self.mysql.cursor()
        cursor.execute("select lite_app_id, full_app_id "
                       "from lite_app.app_measure "
                       "where xapk = 5")
        return cursor.fetchall()

    def update_lite_memory_usage(self, lite_app_id, lite_memory_usage):
        cursor = self.mysql.cursor()
        cursor.execute("UPDATE lite_app.app_measure "
                       "SET lite_memory_usage = %s "
                       "WHERE lite_app_id = %s", (lite_memory_usage, lite_app_id))
        self.mysql.commit()

    def update_full_memory_usage(self, lite_app_id, full_memory_usage):
        cursor = self.mysql.cursor()
        cursor.execute("UPDATE lite_app.app_measure "
                       "SET full_memory_usage = %s "
                       "WHERE lite_app_id = %s", (full_memory_usage, lite_app_id))
        self.mysql.commit()

    def update_lite_cpu_time(self, lite_app_id, lite_cpu_time):
        cursor = self.mysql.cursor()
        cursor.execute("UPDATE lite_app.app_measure "
                       "SET lite_cpu_time = %s "
                       "WHERE lite_app_id = %s", (lite_cpu_time, lite_app_id))
        self.mysql.commit()

    def update_full_cpu_consumption(self, lite_app_id, full_cpu_time):
        cursor = self.mysql.cursor()
        cursor.execute("UPDATE lite_app.app_measure "
                       "SET full_cpu_time = %s "
                       "WHERE lite_app_id = %s", (full_cpu_time, lite_app_id))
        self.mysql.commit()

    def update_xapk(self, lite_app_id, app_type):
        cursor = self.mysql.cursor()
        cursor.execute("UPDATE lite_app.app_measure "
                       "SET xapk = %s "
                       "WHERE lite_app_id = %s", (app_type, lite_app_id))
        self.mysql.commit()