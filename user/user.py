from error_treatment import error

class UserClass:
    def __init__(self, first_name, last_name, user_age, user_mail):
        self.first_name = first_name
        self.last_name = last_name
        self.user_age = user_age
        self.user_mail = user_mail

    def get_user_full_name(self):
        try:
            return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"
        except Exception as e:
            error.error_log_message(e)

    def get_user_mail(self):
        try:
            return self.user_mail if self.user_mail else "Não há e-mail registado."
        except Exception as e:
            error.error_log_message(e)