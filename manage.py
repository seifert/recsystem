#!/usr/bin/env python3

import os

import shelter.main


def main():
    os.environ['SHELTER_SETTINGS_MODULE'] = 'recsystem.settings'
    shelter.main.main()

if __name__ == '__main__':
    main()
