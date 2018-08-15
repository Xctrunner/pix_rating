import os

parent = '/Users/waltmart/Dropbox (Personal)/Camera Uploads/'


lst = []
for root, dirs, _ in os.walk(parent):
    for dir in dirs:
        if dir == "selected" and 'lena_pictures' not in root:
            for file in os.listdir(os.path.join(root, dir)):
                if file.lower().endswith(".jpg"):
                    lst.append(os.path.join(root, file))
with open(parent + '/selected/full_list.txt', 'w+') as f:
    f.write('\n'.join(lst))
