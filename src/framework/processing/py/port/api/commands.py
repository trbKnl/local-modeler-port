from dataclasses import dataclass

class CommandUIRender:
    __slots__ = "page"

    def __init__(self, page):
        self.page = page

    def toDict(self):
        dict = {}
        dict["__type__"] = "CommandUIRender"
        dict["page"] = self.page.toDict()
        return dict


class CommandSystemDonate:
    __slots__ = "key", "json_string"

    def __init__(self, key, json_string):
        self.key = key
        self.json_string = json_string

    def toDict(self):
        dict = {}
        dict["__type__"] = "CommandSystemDonate"
        dict["key"] = self.key
        dict["json_string"] = self.json_string
        return dict


class CommandSystemExit:
    __slots__ = "code", "info"

    def __init__(self, code, info):
        self.code = code
        self.info = info

    def toDict(self):
        dict = {}
        dict["__type__"] = "CommandSystemExit"
        dict["code"] = self.code
        dict["info"] = self.info
        return dict


@dataclass
class CommandSystemGetParameters:
    """
    Ask the server for a set of parameters to c
    """

    def toDict(self):
        dict = {}
        dict["__type__"] = "CommandSystemGetParameters"
        return dict

@dataclass
class CommandSystemPostParameters:
    id: str
    model: str
    checkValue: str

    def toDict(self):
        dict = {}
        dict["__type__"] = "CommandSystemPostParameters"
        dict["id"] = self.id
        dict["model"] = self.model
        dict["checkValue"] = self.checkValue
        return dict
