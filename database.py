import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.Connection('db.sqlite3', check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_lang(self, user_id):
        query = '''
                SELECT lang 
                FROM user
                WHERE user_id = '{}'
                LIMIT 1
        '''.format(user_id)
        try:
            lang = self.cursor.execute(query).fetchone()[0]
            return lang
        except TypeError:
            return 'ru'

    def check_user(self, user_id):
        query = '''
               SELECT * 
               FROM user
               WHERE user_id = '{}'
               LIMIT 1
               '''.format(user_id)
        result = self.cursor.execute(query).fetchone()
        return False if result in [None, []] else True

    def create_user(self, data: dict):
        query = '''
                INSERT INTO user (user_id, firstname, username)
                VALUES ('{}', '{}', '{}')        
                '''.format(data['user_id'], data['firstname'], data['username'])
        self.cursor.execute(query)
        self.connection.commit()

    def update_user(self, user_id, key, value):
        query = '''
        UPDATE user
        SET {} = '{}'
        WHERE user_id = '{}'
        '''.format(key, value, user_id)
        self.cursor.execute(query)
        self.connection.commit()

    def get_user(self, user_id):
        query = '''
        SELECT *
        FROM user
        WHERE user_id = '{}'
        LIMIT 1 
        '''.format(user_id)
        result = self.cursor.execute(query).fetchone()
        return result

    def create_request(self, data: dict):
        query = '''
            INSERT INTO request(potok, user_id)
            VALUES ('{}', '{}')
        '''.format(data['potok'], data['user_id'])
        self.cursor.execute(query)
        self.connection.commit()

    def check_request(self, user_id):
        query = """
            SELECT * from request
            WHERE user_id = '{}' and status = "pending"
            LIMIT 1
        """.format(user_id)
        result = self.cursor.execute(query).fetchone()
        return False if result in [None, []] else True

    def get_request(self, user_id, request_id=None):
        if request_id is None:
            query = """
                SELECT * from request
                WHERE user_id = '{}' and status = "pending"
                LIMIT 1
            """.format(user_id)
        else:
            query = """
                        SELECT * from request
                        WHERE user_id = '{}' and status = "inprogress" and id = '{}'
                        LIMIT 1
                    """.format(user_id, request_id)
        result = self.cursor.execute(query).fetchone()
        return result

    def get_request_button(self, user_id, request_id):
        query = """
                   SELECT * from request
                   WHERE user_id = '{}' and id = '{}'
                   LIMIT 1
               """.format(user_id, request_id)
        result = self.cursor.execute(query).fetchone()
        return result

    def update_request(self, user_id, key, value, status: str = "pending", request_id: str = None):
        if request_id is None:
            query = '''
                UPDATE request
                SET {} = '{}'
                WHERE user_id = '{}' and status = '{}'
            '''.format(key, value, user_id, status)
        else:
            query = '''
                        UPDATE request
                        SET {} = '{}'
                        WHERE user_id = '{}' and status = '{}' and id = '{}'
                        '''.format(key, value, user_id, status, request_id)
        self.cursor.execute(query)
        self.connection.commit()

    def get_all_requests(self, user_id):
        query = """
            SELECT * FROM request
            WHERE user_id = '{}'
            ORDER BY id DESC 
            LIMIT 20
        """.format(user_id)
        result = self.cursor.execute(query).fetchall()
        return result

    def is_user_have_contact(self, user_id):
        query = """
            SELECT phone 
            FROM user
            WHERE user_id = '{}'
            LIMIT 1
        """.format(user_id)
        result = self.cursor.execute(query).fetchone()
        return False if result in [None, []] else True
