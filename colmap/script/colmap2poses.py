import argparse
import os
from utils import pose_utils

def main(input_colmap_dir):
    pose_utils.gen_poses(input_colmap_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='colmap2poses')
    parser.add_argument('--input_colmap_dir', type=str, default='~/Desktop/data/input_colmap')
    args = parser.parse_args()

    args.input_colmap_dir = os.path.expanduser(args.input_colmap_dir)

    main(args.input_colmap_dir)