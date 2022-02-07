from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, DateTime


engine = create_engine("sqlite:///storage.db", echo=True)

metadata = MetaData()
client = Table('client', metadata,
               Column('login', String(50)),
               Column('information', String(100)))

client_history = Table('client_history', metadata,
                       Column('ip-address', String(20)),
                       Column('entered time', DateTime))

contact_list = Table('contact_list', metadata,
                     Column('owner-id', Integer),
                     Column('client-id', Integer))
metadata.create_all(engine)
