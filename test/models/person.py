class Person:
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def contact_info(self):
        return f"Email: {self.email}"
