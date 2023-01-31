from tortoise import Model, fields


class history(Model):
    id = fields.IntField(pk=True)
    uid = fields.IntField()
    cid = fields.IntField()
    update_time = fields.DatetimeField()


class tags(Model):
    id = fields.IntField(pk=True)
    uid = fields.IntField()
    tag = fields.TextField()


class comments(Model):
    id = fields.IntField(pk=True)
    uid = fields.IntField()
    aid = fields.IntField()
    comment = fields.TextField()
    comment_time = fields.DatetimeField()