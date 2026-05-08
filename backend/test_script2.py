from app.config import Settings

s = Settings(email_backend="resend", email_resend_api_key="")
print("key is:", repr(s.email_resend_api_key))
