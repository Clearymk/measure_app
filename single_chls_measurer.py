import re
import shutil
import subprocess
import time
import os
import traceback
import database


class SingleChlsMeasurer:
    def __init__(self, device_id, device_name, app_pair, count):
        self.device_id = device_id
        self.device_name = device_name
        self.app_pair = app_pair
        self.db = database.DataBase()
        self.process_manifest_path = "/Users/clear/PycharmProjects/measure_app/lib/ProcessManifest.jar"
        self.app_pair_path = "/Volumes/Data/backup/"
        self.run_time = 6000
        self.charles_path = "/Volumes/Data/charles_result/" + str(count)

        try:
            self.measurer()
        except Exception as e:
            with open("log.txt", "a+", encoding="utf8") as f:
                f.write(self.app_pair[0] + "\n")
                f.write(traceback.format_exc())
                f.write("\n---------\n")

    def install_apk(self, apk_path, app_id):
        p = subprocess.Popen("adb -s {} install {}".format(self.device_id, apk_path), shell=True)
        p.wait()

        res = os.popen("adb -s {} shell pm list packages -3".format(self.device_id)).readlines()

        if "package:" + app_id + "\n" in res:
            print("install {} success!".format(app_id))
            return True
        else:
            print("install {} failed".format(app_id))
            return False

    def run_by_monkey(self, app_id, count):
        monkey_cmd = "adb -s {} shell monkey -p {}  " \
                     "--pct-syskeys 0 --pct-anyevent 0 --pct-motion 5 " \
                     "--ignore-crashes --ignore-timeouts --throttle 100 {}"
        subprocess.call(monkey_cmd.format(self.device_id, app_id, count), shell=True)

    def record_resource_consumption(self, app_id):
        memory_cmd = "adb -s {} shell dumpsys meminfo | grep {}"
        res = os.popen(memory_cmd.format(self.device_id, app_id)).read()
        reg = re.compile(r'(?P<memory>(?<!,)\b(\d{1,3}(?:,\d{3})*)[Kk]\b(?!,)).+(?P<pid>pid \d+)')
        memory_consumption = reg.findall(res)[0][0]
        pid = reg.findall(res)[0][-1][4:]

        cpu_cmd = "adb -s {} shell ps -p {} -o TIME"
        res = ""
        for line in os.popen(cpu_cmd.format(self.device_id, pid)).readlines():
            res += line
        reg = re.compile(r'(?P<time>\b\d{1,2}:\d{2}:\d{2}\b)')
        cpu_consumption = reg.findall(res)[0]

        return memory_consumption, cpu_consumption

    def uninstall_apk(self, app_id):
        p = subprocess.Popen("adb -s {} uninstall {}".format(self.device_id, app_id), shell=True)
        p.wait()

        res = os.popen("adb -s {} shell pm list packages -3".format(self.device_id)).readlines()

        if "package:" + app_id + "\n" not in res:
            print("uninstall {} success!".format(app_id))
            return True
        else:
            print("uninstall {} failed".format(app_id))
            return False

    def measurer(self):
        self.check_emulator()
        lite_app_id = self.app_pair[0]
        full_app_id = self.app_pair[1]

        lite_app_path = os.path.join(self.app_pair_path, lite_app_id, lite_app_id + ".apk")
        full_app_path = os.path.join(self.app_pair_path, lite_app_id, full_app_id + ".apk")

        print("start process {}".format(lite_app_id))

        if self.install_apk(full_app_path, full_app_id):
            time_count = 0
            while True:
                print("time count:", time_count)
                if time_count > self.run_time / 10:
                    break

                start_time = time.time()
                self.run_by_monkey(full_app_id, self.run_time - int(round(time_count, 1) * 10))
                end_time = time.time()

                time_count += end_time - start_time
            print("spend time count", time_count)
            self.uninstall_apk(full_app_id)
        self.get_charles_result(lite_app_id, full_app_id)

        if self.install_apk(lite_app_path, lite_app_id):
            time_count = 0
            while True:
                if time_count > self.run_time / 10:
                    break

                start_time = time.time()
                self.run_by_monkey(lite_app_id, self.run_time - int(round(time_count, 1) * 10))
                end_time = time.time()

                time_count += end_time - start_time
            print("spend time count", time_count)
            self.uninstall_apk(lite_app_id)
        self.get_charles_result(lite_app_id, lite_app_id)

        self.db.update_xapk(lite_app_id, 10)

    def get_charles_result(self, lite_app_id, app_id):
        charles_file = ""
        flag = False

        while not flag:
            for file in os.listdir(self.charles_path):
                if file.endswith(".chls"):
                    charles_file = file
                    flag = True
                    break
            time.sleep(5)

        if not os.path.exists(os.path.join(self.charles_path, "result", lite_app_id)):
            os.mkdir(os.path.join(self.charles_path, "result", lite_app_id))

        shutil.move(os.path.join(self.charles_path, charles_file),
                    os.path.join(self.charles_path, "result", lite_app_id, app_id + ".chls"))

    def check_emulator(self):
        output = ""
        for line in os.popen("adb devices").readlines():
            output += line

        if self.device_id not in output:
            os.popen("source ~/.bash_profile && emulator -avd {} -no-snapshot-load".format(self.device_name))

            while True:
                res = os.popen("adb -s {} shell getprop dev.bootcomplete".format(self.device_id)).readlines()
                if "1\n" in res:
                    break
                else:
                    time.sleep(1)
