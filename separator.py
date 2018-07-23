import os, argparse, cv2, math
from shutil import copy2

TARGET_PIXEL_AREA = 7 * (10 ** 5)

def get_full_list(parent):
    lst = []
    for root, dirs, files in os.walk(parent):
        for file in files:
            if not (file == '.DS_Store' or file.startswith('Icon') or file == '.dropbox' or file.startswith('blogpic')
                    or file.endswith('.m4v') or file.endswith('.MOV') or file.endswith('mov') or file.endswith('.txt')):
                lst.append(os.path.join(root, file))
    with open('full_pic_list.txt', 'w') as f:
        f.write('\n'.join(lst))
    lst.sort()
    return lst


def has_characteristic(img):
    cv2.namedWindow('separator')
    cv2.moveWindow('separator', 0, 150)
    cv2.imshow('separator', resized)

    while True:
        key = cv2.waitKeyEx(0)
        if key in [ord('a'), ord('s'), ord('d'), ord('f'), ord('j'), ord('k'), ord('l'), ord(';')]:
            cv2.destroyAllWindows()
            return True
        elif key in [' ']:
            cv2.destroyAllWindows()
            return False
        else:
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('in_dir', help='within Camera Uploads')
    parser.add_argument('out_dir', help='anywhere')
    args = parser.parse_args()

    par = '/Users/waltmart/Dropbox (Personal)/Camera Uploads/' + args.in_dir + '/'
    pic_list = get_full_list(par)

    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)

    for pic in pic_list:
        img = cv2.imread(pic)

        ratio1 = float(img.shape[1]) / float(img.shape[0])
        new_h = int(math.sqrt(TARGET_PIXEL_AREA / ratio1) + 0.5)
        new_w = int((new_h * ratio1) + 0.5)
        resized = cv2.resize(img, (new_w, new_h))

        if has_characteristic(resized):
            copy2(pic, args.out_dir)
