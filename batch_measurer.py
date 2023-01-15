import os
import time
import queue
import threading

import database
from single_measurer import SingleMeasurer

MAX_THREAD = 4
download_queue = queue.Queue()
device_ids = ["emulator-5554", "emulator-5556", "emulator-5558", "emulator-5560", "emulator-5562"]
device_names = {"emulator-5554": "Pixel_4_API_30", "emulator-5556": "Pixel_4_API_30_2",
                "emulator-5558": "Pixel_4_API_30_3", "emulator-5560": "Pixel_4_API_30_4",
                "emulator-5562": "Pixel_4_API_30_5"}


class BatchMeasurer:
    def __init__(self):
        self.threads = []
        self.db = database.DataBase()
        self.base_app_ids = []
        self.prepare()

    def worker(self, device_id):
        global download_queue
        self.start_emulator(device_names[device_id], device_id)
        print(device_id, "started")
        while not download_queue.empty():
            app_pair = download_queue.get()
            SingleMeasurer(device_id, device_names[device_id], app_pair)
            download_queue.task_done()

        os.popen("adb -s {} emu kill".format(device_id))

    def start_emulator(self, device_name, device_id):
        os.popen("source ~/.bash_profile && emulator -avd {} -no-snapshot-load".format(device_name))

        while True:
            res = os.popen("adb -s {} shell getprop dev.bootcomplete".format(device_id)).readlines()
            if "1\n" in res:
                break
            else:
                time.sleep(5)

    def prepare(self):
        for app_pair in self.db.query_re_run():
            download_queue.put([app_pair[0], app_pair[1]])

        # set max thread and start each thread
        for i in range(MAX_THREAD):
            thread = threading.Thread(target=self.worker, args=(device_ids[i],))
            thread.start()
            self.threads.append(thread)

        for thread in self.threads:
            thread.join()


if __name__ == '__main__':
    BatchMeasurer()
