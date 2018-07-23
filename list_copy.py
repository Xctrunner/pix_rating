import argparse, os
from shutil import copyfile

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('in_dir', help='within Camera Uploads')
    parser.add_argument('list_size')

    args = parser.parse_args()

    dir = '/Users/waltmart/Dropbox (Personal)/Camera Uploads/' + args.in_dir + '/'
    list_dir = dir + 'lists/'
    list_file = list_dir + str(args.list_size) + '.txt'
    dest_dir = dir + 'selected/'

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(list_file, 'r') as f:
        for line in f:
            struct = line.split('/')
            copyfile(line.rstrip(), dest_dir + struct[-1].rstrip())