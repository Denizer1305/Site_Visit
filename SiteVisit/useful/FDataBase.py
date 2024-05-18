import sqlite3
from flask import json


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_profile(self, alias):
        try:
            self.__cur.execute(f"SELECT * FROM profiles WHERE user_name LIKE ? LIMIT 1", (alias,))
            res = self.__cur.fetchone()
            if res:
                return (res['user_name'], res['name'], res['surname'], res['email'], res['phone'],
                        res['profession'], res['about'], json.loads(res['social']), res['avatar'],
                        res['type_profile'])
        except sqlite3.Error as e:
            print(f"Ошибка при получении поста из БД. {e}")
        return False, False, False, False, False, False, False, False, False, False

