from flask_limiter import Limiter
from flask_bcrypt import Bcrypt

limiter = Limiter(key_func=lambda: "global")
bcrypt = Bcrypt()