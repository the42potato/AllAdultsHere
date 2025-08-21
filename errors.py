from werkzeug.exceptions import HTTPException

class JokeError(HTTPException):
    code = 418
    desc = "I'm a teapot, not a coffee machine."

    def __init__(self, custom_code, description=desc):
        super().__init__(description or self.description)
        self.custom_code = custom_code

def raise_joke_http_error(custom_code, description="I'm a teapot, not a coffee machine."):
    raise JokeError(custom_code=custom_code, description=description)