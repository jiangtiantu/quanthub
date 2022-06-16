import yagmail


class Email:
    def __init__(self, email_user, email_pass, email_host, email_port):
        """
        init email
        :param email_user: email user
        :param email_pass: email password
        :param email_host: email host
        :param email_port: email port
        """
        self.email_user = email_user
        self.email_pass = email_pass
        self.email_host = email_host
        self.email_port = email_port
        self.yag = yagmail.SMTP(
            self.email_user, self.email_pass, self.email_host, self.email_port
        )

    def send_email(self, to: list, subject: str, contents: list):
        """
        send email to the specified address
        :param to: to email address
        :param subject: subject of email
        :param contents: contents of email
        :return:
        """
        self.yag.send(to, subject, contents)
