def send_welcome(mailer, user):
    mailer.send(user["email"], "Welcome", f"Hi {user['name']}")
