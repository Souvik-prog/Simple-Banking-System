# Banking System
import random
import sqlite3
class Banking:
    def __init__(self,conn,card_number_database,card_pin_database):
        self.conn = conn
        self.cur = conn.cursor()
        self.cur.execute('drop table if exists card')
        self.conn.commit()
        self.cur.execute(create_str)
        self.conn.commit()
        self.card_number_database = card_number_database
        self.card_pin_database = card_pin_database
    def customer_request(self):
        while(True):
            x = """
                1. Create an account
                2. Log into account
                0. Exit
                """
            print(x)
            choice = int(input())
            if choice == 1:
                self.create_account(card_pin_database, card_number_database)
            elif choice == 2:
                self.log_into_account(card_number_database, card_pin_database)
            elif choice == 0:
                print("Bye!")
                exit()
    def create_account(self,card_pin_database, card_number_database):
        print("\nYour card has been created")
        bank_identification_number = str(400000)
        for _ in range(9):
            bank_identification_number += str(random.randint(0, 9))
        major_industry_identifier = bank_identification_number[0]
        # account_number = random.randint(0,1000000000)
        # checksum = random.randint(0, 9)
        print("Your card number :")
        card_number = self.Luhn_algo(bank_identification_number)
        print(card_number)
        card_pin = str(random.randint(0, 10000))
        length_pin = len(card_pin)
        while(length_pin < 4):
            card_pin = '0' + card_pin
            length_pin += 1
        print("Your card PIN :")
        print(card_pin)
        execute_str = f'{insert_str}({card_number},{card_pin});'
        self.cur.execute(execute_str)
        self.conn.commit()
        card_number_database.append(card_number)
        card_pin_database.append(card_pin)


    def log_into_account(self,card_number_database, card_pin_database):
        card_number = input("\nEnter your card number:\n")
        card_pin = input("Enter your pin:\n")
        if card_number in card_number_database and card_pin in card_pin_database:
            print("You have successfully logged in")
            while(True):
                x = """
                    1. Balance
                    2. Add income
                    3. Do transfer
                    4. Close account
                    5. Log out
                    0. Exit
                    """
                print(x)
                choice = int(input())
                if choice == 1:
                    balance_str = f'select balance from card where number = {card_number}'
                    bal = self.cur.execute(balance_str)
                    print("Balance:",bal)
                elif choice == 2:
                    self.add_income(card_number)
                elif choice == 3:
                    print("Transfer")
                    self.transfer(card_number)
                elif choice == 4:
                    self.closeAccount(card_number)
                elif choice == 5:
                    print("You have successfully logged out")
                    break
                elif choice == 0:
                    print("Bye!")
                    exit()
        else:
            print("Wrong card number or PIN")

    def Luhn_algo(self, bank_identification_number):
        card_number = ""
        sum = 0
        for i in range(len(bank_identification_number)):
            x = int(bank_identification_number[i])
            if (i+1) % 2 != 0:
                x = 2*x
                if x > 9:
                    x -= 9
            sum += x
        s = sum
        sum = int(sum / 10)
        if sum != 0:
            sum += 1
            sum *= 10
            sum = sum - s
        if sum == 10:
            sum = 0
        bank_identification_number += str(sum)
        card_number = bank_identification_number
        return card_number
    def balance(self,cardnum):
        balance_str = f'select balance from card where ' \
                      f'number = {cardnum};'
        self.cur.execute(balance_str)
        bal = self.cur.fetchall()
        return bal[0][0]
    def add_income(self,cardnum):
        income = int(input("Enter income:"))
        set_bal = f'update card ' \
                  f'set balance = balance + {income} ' \
                  f'where number = {cardnum};'
        self.cur.execute(set_bal)
        self.conn.commit()
        print("Income was added!")

    def luhnAlgorithm(self,number_str):
        number = list(map(int, number_str))
        for index in range(16):
            if index % 2 == 0:
                number[index] *= 2
                if number[index] > 9:
                    number[index] -= 9
        total_sum = sum(number)
        if total_sum % 10 == 0:
            return True
        return False
    def transfer(self,cardnum):
        sum_luhn = 0
        transfer_cardnum = input("Enter card number:\n")
        if self.luhnAlgorithm(transfer_cardnum) == 0:
            print("Probably you made a mistake in the card number. Please try again!")
            return
        else:
            pass
        if transfer_cardnum == cardnum:
            print("You can't transfer money to the same account!")
            return
        transfer_str = f'select * from card where number = {transfer_cardnum}'
        self.cur.execute(transfer_str)
        rows = self.cur.fetchall()
        for i in transfer_cardnum:
            sum_luhn += int(i)
        if len(rows) == 0:
            print("Such a card does not exist.")
            return
        if len(rows) > 0:
            transfer_amount = int(input("Enter how much money you want to transfer:\n"))
            bal = self.balance(cardnum)
            if transfer_amount > int(bal):
                print("Not enough money!")
            else:
                set_bal = f'update card ' \
                          f'set balance = balance - {transfer_amount} ' \
                          f'where number = {cardnum};'
                set_bal_receiver = f'update card ' \
                          f'set balance = balance + {transfer_amount} ' \
                          f'where number = {transfer_cardnum};'
                self.cur.execute(set_bal)
                self.conn.commit()
                self.cur.execute(set_bal_receiver)
                self.conn.commit()
                print("Success!")
        return
    def closeAccount(self,cardnum):
        delete_str = f'delete from card where number = {cardnum}'
        self.cur.execute(delete_str)
        self.conn.commit()
        print("The account has been closed!")
conn = sqlite3.connect('card.s3db')
create_str = ('''
                create table if not exists card(
                id integer,
                number text,
                pin text,
                balance integer default 0);
                ''')
insert_str = 'insert into card (number,pin) values'
card_number_database = []
card_pin_database = []
bank = Banking(conn,card_number_database,card_pin_database)
bank.customer_request()
