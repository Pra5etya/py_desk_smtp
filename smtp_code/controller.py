from smtp_code.model import UserModel
from smtp_code.view import View
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string
from tkinter import messagebox

class Controller:
    def __init__(self):
        self.model = UserModel()
        self.view = View(self)
        self.view.run()

    def register(self, username, password, email):
        self.model.register_user(username, password, email)
        messagebox.showinfo("Success", "Registration successful!")

    def login(self, username, password):
        user = self.model.login_user(username, password)
        if user:
            messagebox.showinfo("Success", "Login successful!")
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def forgot_password(self, email):
        user = self.model.find_user_by_email(email)
        if user:
            verification_code = self.send_verification_email(email)
            if verification_code:
                self.view.show_verification_code_input(email, verification_code)
        else:
            messagebox.showerror("Error", "Email not found")

    def send_verification_email(self, email):
        # Generate verification code
        verification_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

        # Send email with verification code
        smtp_server = 'sandbox.smtp.mailtrap.io'
        smtp_port = 2525  # Change according to your SMTP server
        
        sender_email = '8b78a03d0e70b9'  # Change to your email
        sender_password = '51d9feccfb8f48'  # Change to your password

        private_email = 'sample@main2.com' # change to your email

        msg = MIMEMultipart()
        msg['From'] = private_email
        msg['To'] = email
        msg['Subject'] = 'Verification Code for Password Reset'

        body = f'Your verification code is: {verification_code}'
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)

            server.starttls()
            server.login(sender_email, sender_password)
            
            server.sendmail(private_email, email, msg.as_string())
            server.quit()
            
            messagebox.showinfo("Success", "Verification code sent to your email!")
            
            return verification_code
        except smtplib.SMTPException as e:
            messagebox.showerror("Error", f"Failed to send email: {str(e)}")
            return None

    def verify_code(self, email, entered_code, verification_code):
        if entered_code == verification_code:
            self.view.show_reset_password_dialog(email)
        else:
            messagebox.showerror("Error", "Invalid verification code!")

    def update_password(self, email, new_password):
        self.model.update_password(email, new_password)
        messagebox.showinfo("Success", "Password updated successfully!")
