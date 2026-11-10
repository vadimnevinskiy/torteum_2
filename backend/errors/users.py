class UserNotFoundError(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User {user_id} not found")


class UserAlreadyExistsError(Exception):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User with email {email} already exists")


class RequiredFiledError(Exception):
    def __init__(self, field_name: str):
        super().__init__(f"Field: {field_name} required!")
