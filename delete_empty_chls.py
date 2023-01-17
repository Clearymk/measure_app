import os
import shutil

from database import DataBase

chls_path = "/Volumes/Data/charles_result/"
db = DataBase()

for i in range(4):
    for app_dir in os.listdir(os.path.join(chls_path, str(i + 1), "result")):
        if app_dir == ".DS_Store":
            continue

        for file in os.listdir(os.path.join(chls_path, str(i + 1), "result", app_dir)):
            if file.endswith(".chls"):
                if os.path.getsize(os.path.join(chls_path, str(i + 1), "result", app_dir, file)) == 205:
                    db.update_xapk(app_dir, None)
                    shutil.rmtree(os.path.join(chls_path, str(i + 1), "result", app_dir))
                    print(app_dir)
                    break
