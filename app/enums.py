import enum


class StringValueEnum(enum.Enum):

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"'{self.value}'"


class Command(str, StringValueEnum):

    assign = '/assign'
    invalidate = '/invalidate'
    get_all_certificates = '/list'
    see_assigned_to_user = 'see-assigned'
