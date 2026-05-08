from app.config import Settings

s = Settings(_env_file=None)
print("email_backend:", s.email_backend)
