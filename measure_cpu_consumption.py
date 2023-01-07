import os
import re
import subprocess

import database

process_manifest_path = "D:\\ProcessManifest.jar"
app_pair_path = "D:\\PyCharm 2021.2.1\\code\\lint_full_compare\\download\\download_file"


def install_apk(apk_path, app_id):
    p = subprocess.Popen("adb install \"{}\"".format(apk_path))
    p.wait()

    res = os.popen("adb shell pm list packages -3").readlines()

    if "package:" + app_id + "\n" in res:
        print("install {} success!".format(app_id))
        return True
    else:
        print("install {} failed".format(app_id))
        return False


def run_by_monkey(app_id):
    monkey_cmd = "monkey -p {} --throttle 100 9000"
    p = subprocess.Popen(monkey_cmd.format(app_id))
    p.wait()


def record_resource_consumption(app_id):
    memory_cmd = "adb shell dumpsys meminfo | grep {}"
    res = os.popen(memory_cmd.format(app_id)).read()
    reg = re.compile(r'(?P<memory>\d{1,3}(,\d{3})*K).+(?P<pid>pid \d+)')
    memory_consumption = reg.findall(res)[0][0]
    pid = reg.findall(res)[0][-1][4:]

    cpu_cmd = "ps -p {} -o TIME"
    res = ""
    for line in os.popen(cpu_cmd.format(pid)).readlines():
        res += line
    reg = re.compile(r'(?P<time>\b\d{1,2}:\d{2}:\d{2}\b)')
    cpu_consumption = reg.findall(res)[0]

    return memory_consumption, cpu_consumption


def uninstall_apk(app_id):
    p = subprocess.Popen("adb uninstall \"{}\"".format(app_id))
    p.wait()

    res = os.popen("adb shell pm list packages -3").readlines()

    if "package:" + app_id + "\n" not in res:
        print("uninstall {} success!".format(app_id))
        return True
    else:
        print("uninstall {} failed".format(app_id))
        return False


if __name__ == '__main__':
    db = database.Database()
    os.chdir("D:\\AndroidSDK\\platform-tools")

    for app_pair in db.query_no_resource_consumption_app_pairs():

        lite_app_id = app_pair[0]
        full_app_id = app_pair[1]

        lite_app_path = os.path.join(app_pair_path, lite_app_id, lite_app_id + ".apk")
        full_app_path = os.path.join(app_pair_path, lite_app_id, full_app_id + ".apk")

        print("start process {}".format(lite_app_id))

        if install_apk(lite_app_path, lite_app_id):
            run_by_monkey(lite_app_id)
            lite_memory_count, lite_cpu_count = record_resource_consumption(lite_app_id)
            uninstall_apk(lite_app_id)
            db.update_lite_memory_consumption(lite_app_id, lite_memory_count)
            db.update_lite_cpu_consumption(lite_app_id, lite_cpu_count)

        if install_apk(full_app_path, full_app_id):
            run_by_monkey(lite_app_id)
            full_memory_count, full_cpu_count = record_resource_consumption(full_app_id)
            uninstall_apk(full_app_id)
            db.update_full_memory_consumption(lite_app_id, full_memory_count)
            db.update_full_cpu_consumption(lite_app_id, full_cpu_count)

        print("finish process {}".format(lite_app_id))
        print("------------")
