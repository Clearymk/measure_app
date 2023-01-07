import os
import re
import subprocess

import database

process_manifest_path = "/Users/clear/PycharmProjects/measure_app/lib/ProcessManifest.jar"
app_pair_path = "/Volumes/Data/backup/"


def install_apk(apk_path, app_id):
    p = subprocess.Popen("adb install {}".format(apk_path), shell=True)
    p.wait()

    res = os.popen("adb shell pm list packages -3").readlines()

    if "package:" + app_id + "\n" in res:
        print("install {} success!".format(app_id))
        return True
    else:
        print("install {} failed".format(app_id))
        return False


def uninstall_apk(app_id):
    p = subprocess.Popen("adb uninstall {}".format(app_id), shell=True)
    p.wait()

    res = os.popen("adb shell pm list packages -3").readlines()

    if "package:" + app_id + "\n" not in res:
        print("uninstall {} success!".format(app_id))
        return True
    else:
        print("uninstall {} failed".format(app_id))
        return False


def find_app_main_activity(app_path):
    res = os.popen("java -jar {} {}".format(process_manifest_path, app_path)).readlines()
    return res[0].strip()


def get_app_launch_time_launch_app(app_id, launch_activity):
    p = subprocess.Popen("adb shell am start -S -W {}/{} "
                         "-c android.intent.category.LAUNCHER "
                         "-a android.intent.action.MAIN".format(app_id, launch_activity),
                         stdout=subprocess.PIPE, shell=True)
    output = p.communicate()[0].decode("utf-8")
    p.wait()
    reg = re.compile(r'WaitTime: (?P<time>\d+)')
    return reg.findall(output)[0]


if __name__ == '__main__':
    db = database.DataBase()

    for app_pair in db.query_no_launch_time_app_pairs():

        lite_app_id = app_pair[0]
        full_app_id = app_pair[1]

        lite_app_path = os.path.join(app_pair_path, lite_app_id, lite_app_id + ".apk")
        full_app_path = os.path.join(app_pair_path, lite_app_id, full_app_id + ".apk")

        print("start process {}".format(lite_app_id))

        if install_apk(lite_app_path, lite_app_id):
            lite_app_launch_time = get_app_launch_time_launch_app(lite_app_id,
                                                                  find_app_main_activity(lite_app_path))
            uninstall_apk(lite_app_id)
            print("lite app {} launch time is {}".format(lite_app_id, lite_app_launch_time))
            db.update_lite_launch_time(lite_app_id, lite_app_launch_time)

        if install_apk(full_app_path, full_app_id):
            full_app_launch_time = get_app_launch_time_launch_app(full_app_id,
                                                                  find_app_main_activity(full_app_path))
            uninstall_apk(full_app_id)
            print("full app {} launch time is {}".format(full_app_id, full_app_launch_time))
            db.update_full_launch_time(lite_app_id, full_app_launch_time)
        print("finish process {}".format(lite_app_id))
        print("------------")
