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


class Schedulable(me.Document):
    concurrency = me.IntField()


class Executable(me.Document):
    name = me.StringField()
    params = me.DynamicField()


class Event(BasicEvent):
   executable = me.ReferenceField('Executable')
   schedulable = me.ReferenceField('Schedulable')
