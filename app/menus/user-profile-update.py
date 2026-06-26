from app.menus.base import BaseMenu
from app.repositories.user import User, UserRepository
from app.services.customer import Customer


class UserUdate(BaseMenu):
    def __init__(self, username: User, new_full_name, new_email):
        self.username = username
        self.new_full_name = new_full_name
        self.new_email = new_email

    def show_user(self, user: User, customer: Customer):
        print(f""" username is : {user.username} \n
               password is : {user.password} \n
               email is : {customer.email} \n
               full name is : {customer.full_name}""")

    def update_user(
        self, user1: UserRepository, username, new_full_name, new_email, new_password
    ):
        user1.update_by_username(username, new_password, new_full_name, new_email)
