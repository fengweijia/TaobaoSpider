import pymongo

MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'detail'

KEYWORD = 'ipad'
MAX_PAGE = 100

SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']


class MongDB:
    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_URL)
        self.db = self.client[MONGO_DB]

    def save_to_mongo(self,result):
        """
        保存结果至MongoDB
        :param result: 插入数据库的数据
        """
        try:
            if self.db[MONGO_COLLECTION].insert(result):
                print("存储到MongoDB成功")
        except Exception:
            print("存储到MongoDB失败")

    def get_from_mongo(self):
        my_query = {"_id": 0,"data_sid": 1}
        query_result = []
        for i in self.db[MONGO_COLLECTION].find({},my_query):
            query_result.append(i)

        return query_result
