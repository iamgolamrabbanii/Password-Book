import json, os
from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self):
        if not os.path.exists('password_book.txt'):
            open('password_book.txt', 'w', encoding = 'utf-8').close()
        self.encry_decry = Encryption_Decryption()

    def run(self):
        user_input = self.Choices()

        # chosing the work 
        if user_input == 1:
            AddNewPassword().run(self.encry_decry)
            print('*' * 50)
        elif user_input == 2:
            self.veiw_all_password()
            print('*' * 50)
        elif user_input == 3:
            self.search_by_website()
            print('*' * 50)
        else :
            return

    def Choices(self):
        print("\nWelcome to Your Password Manager\n"
            "1. Add New Password\n" 
            "2. View All Passwords\n" 
            "3. Search by Website\n" 
            "4. Exit\n\n"

            "Enter Your Choice: ", end = "")
        # taking choice and check validity
        try:
            user_input = int(input())
            if user_input < 1 or user_input > 4 :
                raise ValueError # through to except loop
            
            return user_input
        except:
            print("Enter a Valid Number")
            return self.Choices() # created a loop until get valid input
    
    def veiw_all_password(self):
        print('*' * 50)
        print("View all passowrd Page\n")
        cnt = 1
        with open('password_book.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()

            for line in lines:
                line_content = json.loads(line)
                
                user_name = self.encry_decry.decryption(line_content['username'])
                password = self.encry_decry.decryption(line_content['password'])
                
                print(str(cnt) + "." + line_content['website'])
                print(" Username :", user_name)
                print(" Password :", password)
                cnt += 1

            if len(lines) == 0:
                print("No password saved yet")
    
    def search_by_website(self):
        cnt = 1
        print('*' * 50)
        print("Search by Website Page\n")
        user_search = input("Search Your Website : ")

        with open('password_book.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()

            for line in lines:
                line_content = json.loads(line)
                if line_content['website'] == user_search.upper():
                    user_name = self.encry_decry.decryption(line_content['username'])
                    password = self.encry_decry.decryption(line_content['password'])
                    
                    print(str(cnt) + "." + line_content['website'])
                    print(" Username :", user_name)
                    print(" Password :", password)
                    cnt += 1

        if cnt == 1:
            print( f"\n{user_search} is not found\n")


class AddNewPassword:
    def __init__(self):
        print('*' * 50)
        print("Add New Password Page")
        self.website = input("Enter Website Name : ").upper()
        self.user_name = input("Enter Username : ")
        self.password = input("Enter Passowd : ")

    def run(self, encry_decry):

        self.create_new_password(encry_decry)
    def create_new_password(self, encry_decry):
  
        data = {
            'website': self.website,
            'username': encry_decry.encryption(self.user_name).decode(),
            'password': encry_decry.encryption(self.password).decode(),
        }
        with open('password_book.txt', 'a', encoding='utf-8') as file:
            json.dump(data, file)
            file.write('\n')
        print("New password Added")


class Encryption_Decryption:
    def __init__(self):
        if not os.path.exists('key.key'):
            key = Fernet.generate_key()
            with open("key.key", "wb") as f:
                f.write(key)
            self.generator = Fernet(key)

        else :
            with open("key.key", "rb") as f:
                key = f.read()
                self.generator = Fernet(key)
            
    def encryption(self, value):
        return self.generator.encrypt(value.encode())
    def decryption(self, value):
        return self.generator.decrypt(value).decode()


if __name__ == "__main__":
    pm = PasswordManager()
    while True:
        pm.run()