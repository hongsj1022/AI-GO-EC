from main_engine import MainEngine

import json
import argparse

def load_config(filename):
    cfg: dict
    with open(filename, 'r') as f:
        cfg = json.load(f)

    return cfg


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='config.json', help='config file')
    args = parser.parse_args()
    
    cfg = load_config(args.config)

    me = MainEngine(cfg)
    me.run()


