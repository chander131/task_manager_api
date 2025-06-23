from mongoengine import Document, StringField, DateTimeField
from datetime import datetime
from enum import Enum


class Status(str, Enum):
    TODO = "T"
    IN_PROGRESS = "I"
    DONE = "D"

    @classmethod
    def choices(cls):
        return [(key.value, key.name.title().replace("_", " ")) for key in cls]


class Task(Document):
    title = StringField(required=True, max_length=200)
    description = StringField(null=True, required=False)
    status = StringField(
        choices=Status.choices(),
        default=Status.TODO.value,
    )
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "tasks"}

    def __str__(self):
        return self.title
