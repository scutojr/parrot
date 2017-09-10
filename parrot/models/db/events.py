import mongoengine as me


class BasicEvent(me.Document):
    topic = me.StringField()
    hostname = me.StringField()
    service = me.StringField()
    status = me.StringField()
    output = me.StringField()
    timestampt = me.LongField()
    tags = me.DynamicField()

    meta = {'allow_inheritance': True}

    @staticmethod
    def from_dict(data: dict):
        return BasicEvent(**data)

    def to_dict(self) -> dict:
        pass


class Executable(me.Document):
    concurrency = me.IntField()


class Schedulable(me.Document):
    engine = me.StringField()
    params = me.ListField()


class Event(BasicEvent):
   executable = me.ReferenceField('Executable')
   schedulable = me.ReferenceField('Schedulable')
