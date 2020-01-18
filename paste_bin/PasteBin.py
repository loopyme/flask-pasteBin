import time


class Record:
    def __init__(self, record_title, record_type, record_expire, record_content):
        """

        :param record_title: title of record
        :param record_type: "url" or "text"
        :param record_expire: see self.expire
        :param record_content:
        """
        self.title = record_title
        self.type = record_type
        self.expire = record_expire
        self.content = (
            (
                record_content
                if "://" in record_content or record_type != "url"
                else "http://" + record_content
            )
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br/>")
        )

    @property
    def expire(self):
        if self._expire is None:  # permanent
            return self._expire, 0
        elif isinstance(self._expire, float):  # expire by time
            return self._expire, 1
        elif isinstance(self._expire, int):  # expire by visit
            return -self._expire, 2

    @expire.setter
    def expire(self, record_expire):
        if record_expire == "None":  # permanent
            self._expire = None
        elif int(record_expire) >= 3600:  # expire by time
            self._expire = time.time() + float(record_expire)
        elif int(record_expire) < 3600:  # expire by visit
            self._expire = int(record_expire)
        else:  # set expire
            self._expire = record_expire

    @property
    def valid(self):
        expire, expire_type = self.expire
        return (
            expire_type == 0
            or (expire_type == 1 and expire >= time.time())
            or (expire_type == 2 and expire > -1)
        )

    @property
    def expire_info(self):
        expire, expire_type = self.expire
        if expire_type == 0:
            return "it will hold permanently"
        elif expire_type == 1:
            return "it will expired at {}".format(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(expire))
            )
        elif expire_type == 2:
            if expire == 0:
                return "it has expired"
            else:
                return "it will expired after {} visits".format(expire)

    def visit(self):
        _, expire_type = self.expire
        if expire_type == 2:
            self._expire = self._expire + 1


class PasteBin:
    contents = {}

    def __init__(self):
        raise AttributeError("Class PasteBin can not be instance")

    @classmethod
    def check_title(cls, title=None):
        """check if title is valid"""
        for k in cls.contents.keys():
            if not cls.contents[k].valid:
                del cls.contents[k]

        if title is not None and title in cls.contents.keys():
            return False
        return True

    @classmethod
    def set_record(
        cls, record_title, record_type, record_expire, record_content, **arg
    ):
        if not cls.check_title(record_title):
            return False
        else:
            cls.contents[record_title] = Record(
                record_title, record_type, record_expire, record_content
            )
            return True

    @classmethod
    def get_record(cls, record_title):
        if record_title in cls.contents.keys():
            record = cls.contents[record_title]
            record.visit()
            if record.valid:
                return record
            else:
                del cls.contents[record_title]
        return None

    @classmethod
    def clear(cls):
        cls.contents = {}
