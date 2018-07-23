import cv2, os, math, random
from collections import deque
import argparse

TARGET_PIXEL_AREA = 220000.0


# TODO need to get new size based on bigger of the two
def combine_pics(impath1, impath2):
    img1 = cv2.imread(impath1)
    img2 = cv2.imread(impath2)
    switched = False

    if img1.shape[0] * img1.shape[1] < img2.shape[0] * img2.shape[1]:
        temp = img1
        img1 = img2
        img2 = temp
        switched = True

    ratio1 = float(img1.shape[1]) / float(img1.shape[0])
    new_h = int(math.sqrt(TARGET_PIXEL_AREA / ratio1) + 0.5)
    new_w1 = int((new_h * ratio1) + 0.5)

    ratio2 = float(img2.shape[1]) / float(img2.shape[0])
    new_w2 = int((new_h * ratio2) + 0.5)

    return switched, cv2.hconcat([cv2.resize(img1, (new_w1, new_h)), cv2.resize(img2, (new_w2, new_h))])


def is_first_better(combined, impath1, impath2, is_switched):
    winName = impath1 + "  |||  " + impath2 if not is_switched else impath2 + "  |||  " + impath1
    cv2.namedWindow(winName)
    cv2.moveWindow(winName, 0, 150)
    cv2.imshow(winName, combined)
    while True:
        key = cv2.waitKeyEx(0)
        if key in [ord('a'), ord('s'), ord('d'), ord('f')]:
            cv2.destroyAllWindows()
            return True
        elif key in [ord('j'), ord('k'), ord('l'), ord(';')]:
            cv2.destroyAllWindows()
            return False
        else:
            cv2.destroyAllWindows()
            break


def get_full_list(parent):
    lst = []
    for root, dirs, files in os.walk(parent):
        for file in files:
            if not (file == '.DS_Store' or file.startswith('Icon') or file == '.dropbox' or file.startswith('blogpic')
                    or file.endswith('.m4v') or file.endswith('.MOV') or file.endswith('mov') or file.endswith('.txt')):
                lst.append(os.path.join(root, file))
    with open('full_pic_list.txt', 'w') as f:
        f.write('\n'.join(lst))
    return lst


def get_txt_list(path):
    with open(path, 'r') as fi:
        lst = fi.readlines()
        random.shuffle(lst)
        return lst

def print_ends():
    with open('full_pic_list.txt', 'r') as f:
        lst = f.readlines()
        ends = list(map(lambda x: x[-4:], lst))
        end_set = set(ends)
        print(end_set)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('in_dir', help='within Camera Uploads')
    args = parser.parse_args()

    parent = '/Users/waltmart/Dropbox (Personal)/Camera Uploads/' + args.in_dir + '/'
    pic_list = get_full_list(parent)
    rand_pic_list = pic_list.copy()
    random.shuffle(rand_pic_list)
    q = deque(rand_pic_list)

    # for n in [2500, 2000, 1500, 1000, 500, 200, 100, 50, 20, 10]:
    # for n in [1500, 1000, 500, 200, 100, 50, 20, 10]:
    for n in [1000, 500, 200, 100, 50, 20, 10, 5]:
    # for n in [100, 50, 20, 10, 5, 2, 1]:
        while len(q) > n:
            pic1 = q.popleft()
            pic2 = q.popleft()
            switched, combined = combine_pics(pic1, pic2)
            if is_first_better(combined, pic1[len(parent):], pic2[len(parent):], switched):
                q.append(pic1) if not switched else q.append(pic2)
            else:
                q.append(pic2) if not switched else q.append(pic1)

        if not os.path.exists(parent + 'lists/'):
            os.makedirs(parent + 'lists/')

        with open(parent + 'lists/' + str(n) + '.txt', 'w+') as f:
            f.write('\n'.join(list(q)))
