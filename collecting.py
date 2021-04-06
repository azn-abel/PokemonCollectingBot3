class Collector:
    instances = []
    instances_dict = {}

    def __init__(self, id):
        self.__class__.instances.append(self)
        self.__class__.instances_dict[id] = self
        self.id = id
        self.pokemon_list = []
        self.unique_list = []
        self.dupe_list = []
        self.poke_points = 0


class Channel:
    instances = []
    instance_dict = {}

    def __init__(self, id, name, server):
        self.__class__.instances.append(self)
        self.__class__.instance_dict[id] = self
        self.id = id
        self.name = name
        self.server = server
        self.drops_enabled = True
        self.drop_active = False
        print(self.__class__.instances)
        print(self.__class__.instance_dict)
