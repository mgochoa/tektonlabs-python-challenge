class NotFoundError(Exception):
    """ Base Error for any DB resource"""
    entity_name: str

    def __init__(self, entity_name, entity_id):
        self.entity_name = entity_name
        super().__init__(f"{self.entity_name} with id id: {entity_id} not found")
