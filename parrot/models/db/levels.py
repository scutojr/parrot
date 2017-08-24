import mongoengine as me


class Level(me.Document):
    name = me.StringField()
    ordinal = me.IntField()


class LevelSeq(me.Document):
    name = me.StringField()
    levels = me.ListField()

    def compair(self, level1, level2):
        pass

    def append(self, level):
        pass
