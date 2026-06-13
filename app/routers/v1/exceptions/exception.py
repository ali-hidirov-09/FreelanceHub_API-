class FreelanceHubError(Exception):
    pass

class ObjectNotFound(FreelanceHubError):
    def __init__(self, model_name: str, obj_id: int, status_code: int):
        self.model_name = model_name
        self.obj_id = obj_id
        self.status_code = status_code

