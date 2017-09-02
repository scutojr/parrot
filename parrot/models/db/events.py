import mongoengine as me


class BasicEvent(me.Document):
    topic = me.StringField()
    hostname = me.StringField()
    service = me.StringField()
    status = me.StringField()
    output = me.StringField()
    time = me.DateTimeField()
    tags = me.DynamicEmbeddedDocument()

    @staticmethod
    def from_dict():
        pass

    def to_dict(self):
        pass


class Executable(me.Document):
    pass


class Schedulable(me.Document):
    pass


class Event(BasicEvent):
    executable = me.ReferenceField('Executable')
    schedulable = me.ReferenceField('Schedulable')
