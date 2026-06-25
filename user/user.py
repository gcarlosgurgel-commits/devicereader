from error_treatment import error

class USER:
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.mail = None
        
    def set_first_name(self):
        """ Set the users first name"""
        try:
            self.first_name = input("First name: ").lower()
        except Exception as e:
            error.error_log_message(e)
    def set_last_name(self):
        """ Set the users last name """
        try:
            self.last_name = input("Last name: ").lower()
        except Exception as e:
            error.error_log_message(e)
    def get_user_full_name(self):
        try:
            return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"
        except Exception as e:
            error.error_log_message(e)
    def set_user_mail(self):
        try:
            self.mail = input("Digite seu e-mail: ").lower()
        except Exception as e:
            error.error_log_message(e)
    def get_user_mail(self):
        try:
            return self.mail if self.mail else "Não há e-mail registado."
        except Exception as e:
            error.error_log_message(e)