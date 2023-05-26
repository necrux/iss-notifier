#!/usr/bin/env python3
"""Configure and send email notifications."""
import smtplib
import configparser
from os import path

SUBJECT = "Look Up"
MESSAGE = "The ISS is overhead."


class Email:
    """Configure and send email notifications."""
    def __init__(self):
        self.auth_file = f'{path.expanduser("~")}/.keys'
        self.auth_file_section = 'iss'
        self.auth_email_field = 'email'
        self.auth_password_field = 'password'
        self.auth_smtp_field = 'smtp'

    def get_credentials(self) -> tuple:
        """Get the email credentials from the current user."""
        config = configparser.ConfigParser()

        try:
            config.read(self.auth_file)
            email = config[self.auth_file_section][self.auth_email_field]
            password = config[self.auth_file_section][self.auth_password_field]
            smtp = config[self.auth_file_section][self.auth_smtp_field]
        except KeyError:
            print("Must configure an email first.")
            self.configure()
        finally:
            config.read(self.auth_file)
            email = config[self.auth_file_section][self.auth_email_field]
            password = config[self.auth_file_section][self.auth_password_field]
            smtp = config[self.auth_file_section][self.auth_smtp_field]
        return email, password, smtp

    def configure(self):
        """Configure email credentials for the current user."""
        config = configparser.RawConfigParser()
        email = input("What is your email address? ")
        password = input("What is the app password? ")
        smtp = input("What is the SMTP server? ")

        if path.exists(self.auth_file):
            config.read(self.auth_file)

        if not config.has_section(self.auth_file_section):
            config.add_section(self.auth_file_section)
            config.set(self.auth_file_section, self.auth_email_field, email)
            config.set(self.auth_file_section, self.auth_password_field, password)
            config.set(self.auth_file_section, self.auth_smtp_field, smtp)

            with open(self.auth_file, 'a+', encoding='UTF-8') as file:
                config.write(file)
        else:
            overwrite = input('You already have this information configured. '
                              'Do you want to overwrite these values? y/N ')
            overwrite = overwrite.lower()

            if overwrite == 'y':
                config.set(self.auth_file_section, self.auth_email_field, email)
                config.set(self.auth_file_section, self.auth_password_field, password)
                config.set(self.auth_file_section, self.auth_smtp_field, smtp)

                with open(self.auth_file, 'w', encoding='UTF-8') as file:
                    config.write(file)

    def send_notification(self):
        """Send email notifications."""
        email, password, smtp = self.get_credentials()
        connection = smtplib.SMTP(smtp)
        connection.starttls()
        connection.login(email, password)
        connection.sendmail(from_addr=email,
                            to_addrs=email,
                            msg=f"Subject:{SUBJECT}\n\n{MESSAGE}")
