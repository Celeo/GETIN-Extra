#!/usr/bin/env python
from app.app import db


def main():
    print('Attemping to create database ...', end='')
    db.create_all()
    print('done')


if __name__ == '__main__':
    main()
