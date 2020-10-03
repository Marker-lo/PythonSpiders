#!/usr/bin/python
# -*- coding: utf-8 -*-

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class SQLAlchemyDatabase:
    def __init__(self, req_data):
        self.m_host = req_data.get('host')
        self.m_port = req_data.get('port')
        self.m_user = req_data.get('user')
        self.m_pwd = req_data.get('pwd')
        self.m_schema = req_data.get('schema')
        self.m_charset = req_data.get('charset', 'utf8')
        self.m_encoding = req_data.get('encoding', 'utf-8')
        self.m_pool_size = req_data.get('pool_size', 30)
        self.m_pool_recycle = req_data.get('pool_recycle', 10)
        self.m_pool_timeout = req_data.get('pool_timeout', 60 * 60 * 3)
        self.m_echo = req_data.get('echo', False)
        self.m_engine = None
        self.m_conn = None
        self.m_session_maker = None

    def __str__(self):
        return '{user}:{password}@{host}:{port}/{schema}?charset={charset}'.format(
            user=self.m_user, password=self.m_pwd, host=self.m_host, port=self.m_port,
            schema=self.m_schema, charset=self.m_charset
        )

    def __del__(self):
        if self.m_conn is not None:
            self.m_conn.close()
            self.m_conn = None

        # if self.m_engine is not None:
        #     self.m_engine.close()
        #     self.m_engine = None

    def __create_engine(self):

        db_url = 'mysql+pymysql://%s:%s@%s:%d/%s?charset=%s' % (self.m_user, self.m_pwd,
                                                                self.m_host, self.m_port,
                                                                self.m_schema,
                                                                self.m_charset)
        print('db_info:utils.sqlalchemy: %s' % db_url)
        engine = create_engine(db_url,
                               encoding=self.m_encoding,
                               pool_size=self.m_pool_size,
                               pool_recycle=self.m_pool_recycle,
                               pool_timeout=self.m_pool_timeout,
                               echo=self.m_echo)

        return engine

    def get_engine(self):
        if self.m_engine is None:
            self.m_engine = self.__create_engine()

        return self.m_engine

    def __create_conn(self):
        if self.m_engine is None:
            self.m_engine = self.__create_engine()

        conn = self.m_engine.connect()

        return conn

    def get_conn(self):
        if self.m_conn is None:
            self.m_conn = self.__create_conn()

        return self.m_conn

    def __create_session_maker(self):
        if self.m_engine is None:
            self.m_engine = self.__create_engine()

        session_maker = sessionmaker(bind=self.m_engine)

        return session_maker

    def get_session_maker(self):
        if self.m_session_maker is None:
            self.m_session_maker = self.__create_session_maker()

        return self.m_session_maker


def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@Singleton
class Sqlalchemydb:
    def __init__(self, req_data):
        self.m_host = req_data.get('host')
        self.m_port = req_data.get('port')
        self.m_user = req_data.get('user')
        self.m_pwd = req_data.get('pwd')
        self.m_schema = req_data.get('schema')
        self.m_charset = req_data.get('charset', 'utf8')
        self.m_encoding = req_data.get('encoding', 'utf-8')
        self.m_pool_size = req_data.get('pool_size', 30)
        self.m_pool_recycle = req_data.get('pool_recycle', 10)
        self.m_pool_timeout = req_data.get('pool_timeout', 60 * 60 * 3)
        self.m_echo = req_data.get('echo', False)
        self.m_engine = None
        self.m_conn = None
        self.m_session_maker = None

    def __del__(self):
        if self.m_conn is not None:
            self.m_conn.close()
            self.m_conn = None

        # if self.m_engine is not None:
        #     self.m_engine.close()
        #     self.m_engine = None

    def __create_engine(self):

        db_url = 'mysql+pymysql://%s:%s@%s:%d/%s?charset=%s' % (self.m_user, self.m_pwd,
                                                                self.m_host, self.m_port,
                                                                self.m_schema,
                                                                self.m_charset)
        print('db_info:utils.sqlalchemy: %s' % db_url)
        engine = create_engine(db_url,
                               encoding=self.m_encoding,
                               pool_size=self.m_pool_size,
                               pool_recycle=self.m_pool_recycle,
                               pool_timeout=self.m_pool_timeout,
                               echo=self.m_echo)

        return engine

    def get_engine(self):
        if self.m_engine is None:
            self.m_engine = self.__create_engine()

        return self.m_engine

    def __create_conn(self):
        if self.m_engine is None:
            self.m_engine = self.__create_engine()

        conn = self.m_engine.connect()

        return conn

    def get_conn(self):
        if self.m_conn is None:
            self.m_conn = self.__create_conn()

        return self.m_conn

    def __create_session_maker(self):
        if self.m_engine is None:
            self.m_engine = self.__create_engine()

        session_maker = sessionmaker(bind=self.m_engine)

        return session_maker

    def get_session_maker(self):
        if self.m_session_maker is None:
            self.m_session_maker = self.__create_session_maker()

        return self.m_session_maker


class Session:
    def __init__(self, session_maker):
        self.m_session = session_maker()

    def __del__(self):
        if self.m_session is not None:
            self.m_session.close()
            self.m_session = None

    def get_session(self):
        return self.m_session


class SessionMixin(object):
    """
    session mixin
    """
    factory = None

    @contextmanager
    def make_session(self):
        session = None

        if not self.factory:
            return None

        try:
            session = self.factory.make_session()
            yield session
        except Exception:
            if session:
                session.rollback()
            raise
        else:
            session.commit()

        finally:
            if session:
                session.close()


def get_db_session(db_factory):
    db_session = SessionMixin()
    db_session.factory = db_factory
    return db_session
