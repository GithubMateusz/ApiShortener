import motor.motor_tornado

from config import Config


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=Singleton):
    def __init__(self, config=Config()):
        self._client = motor.motor_tornado.MotorClient(config.DB_HOST, config.DB_PORT)
        self._database = self._client[config.DB_NAME]
        self._database.list.create_index("id", )

        self._collection_link = config.DB_LINK
        self._database[self._collection_link].create_index("one_hour_time_link", expireAfterSeconds=1 * 60 * 60)
        self._database[self._collection_link].create_index("twelve_hours_time_link", expireAfterSeconds=12 * 60 * 60)
        self._database[self._collection_link].create_index("one_day_time_link", expireAfterSeconds=24 * 60 * 60)
        self._database[self._collection_link].create_index("seven_days_time_link", expireAfterSeconds=168 * 60 * 60)

    async def do_insert_one(self, collection, data):
        document = await self._database[collection].insert_one(data)
        return document.inserted_id

    async def do_replace_one(self, collection, id_object, data):
        self._database[collection].replace_one(id_object, data)

    async def do_find_one(self, collection, search_after):
        document = await self._database[collection].find_one(search_after)
        return document

    async def do_find(self, collection, search_after):
        document = self._database[collection].find(search_after)
        list_link = []
        async for one_link in document:
            if one_link["private"] == "yes":
                typ = "prywatny"
            else:
                typ = "publiczny"
            list_link.append(
                {"link": one_link["link"], "short_link": one_link["short_link"], "typ": typ}
            )
        return list_link

    async def do_delete_one(self, collection, id_object):
        self._database[collection].delete_one(id_object)
