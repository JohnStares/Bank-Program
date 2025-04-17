# CLI BANKING APPLICATION

import json
from datetime import datetime
import asyncio
import os
from logic import validate_amount, validate_input, validate_name, generate_acct_no

class BankingProgram:
    def __init__(self):
        self.user = {}
        self.id_counter = 1
        self.id = {}

    def auto_id(self):
        user_id = f"{self.id_counter:03}"
        self.id_counter += 1
        self.id = user_id

        return user_id

    def register_customer(self, name):
        date = datetime.today().date()
        user_id = self.auto_id()

        if user_id not in self.user:
            self.user[user_id] = []
        try:
            self.user[user_id].append({
                "Name": name,
                "account no": generate_acct_no(),
                "balance": 0.00,
                "date joined": date
            })
        except Exception as e:
            print(f"Having difficulties registering user due to {e}")
        else:
            return {"Message": "User registered successful."}

    def view_users(self):
        print("==================================")
        for user_id, user in self.user.items():
            for user_details in user:
                try:
                    print(f"Id: {user_id}\nName: {user_details[f"Name"]}\nAct No: {user_details["account no"]}\nBalance: {user_details["balance"]}")
                    print("==================================")
                except Exception as e:
                    print(e)

    def depo(self, act_no, amount):
        date = datetime.today().date()
        transaction = "Transaction"

        for _, user_details in self.user.items():
            for user in user_details:
                if transaction not in user:
                    user[transaction] = []

                if act_no == user["account no"]:
                    try:
                        user[transaction].append({
                            "type": "Deposit",
                            "amount": f"${amount}",
                            "status": "Successful",
                            "date": date
                        })

                        user["balance"] += float(amount)
                    except Exception as e:
                        print(f"An error occurred during transaction due to {e}.")
                    else:
                        print(f"${amount} successfully deposited")
                else:
                    print("Account number doesn't exist.")
                    continue


    def make_withdrawal(self, act_no, amount):
        date = datetime.today().date()
        transaction = "Transaction"

        for _, user_details in self.user.items():
            for user in user_details:
                if transaction not in user:
                    user[transaction] = []

                if act_no == user["account no"]:
                    try:
                        if user["balance"] < amount:
                            print("Insufficient fund.")
                            break

                        user[transaction].append({
                            "type": "Withdrawal",
                            "amount": f"${amount}",
                            "status": "Successful",
                            "date": date
                        })

                        user["balance"] -= amount
                    except Exception as e:
                        print(f"An error occurred during transaction due to {e}.")
                    else:
                        print(f"${amount} successfully withdrawn")
                else:
                    print("Account number doesn't exist.")
                    continue

    async def make_transfer(self, act_no, other_act_no, amount ):
        date = datetime.today().date()
        senders_name = ''
        receivers_name = ''
        async def sender():
            nonlocal senders_name
            nonlocal date
            for _, user_details in self.user.items():
                for user in user_details:
                    if "Transaction" not in user:
                        user["Transaction"] = []

                    if act_no == user["account no"]:
                        try:
                            if user["balance"] < amount:
                                print("Insufficient fund.")
                                break
                            await  asyncio.sleep(0.5)
                            user["Transaction"].append({
                                "type": "Transfer",
                                "sender": True,
                                "to": receivers_name,
                                "amount": f"${amount}",
                                "status": "Successful",
                                "date": date
                            })

                            user["balance"] -= amount
                            senders_name += user["Name"]
                        except Exception as e:
                            print(f"An error occurred during transaction due to {e}.")
                        else:
                            print(f"${amount} successfully transferred to {receivers_name}")
                            print(f"${amount} has been debited from your account.")
                    else:
                        print("Account number doesn't exist.")
                        continue

        async def receiver():
            nonlocal receivers_name
            nonlocal date
            for _, user_details in self.user.items():
                for user in user_details:
                    if "Transaction" not in user:
                        user["Transaction"] = []

                    if other_act_no == user["account no"]:
                        try:
                            receivers_name += user["Name"]
                            await asyncio.sleep(1)
                            user["Transaction"].append({
                                "type": "Transfer",
                                "sender": False,
                                "from": senders_name,
                                "amount": f"${amount}",
                                "status": "Successful",
                                "date": date
                            })
                            await asyncio.sleep(0.5)
                            user["balance"] += amount
                        except Exception as e:
                            print(f"An error occurred during transaction due to {e}.")
                        else:
                            print(f"${amount} successfully credited to your account by {senders_name}")
                    else:
                        print("Account number doesn't exist.")
                        continue

        t1 = asyncio.create_task(sender())
        t2 = asyncio.create_task(receiver())

        try:
            await t1
            await t2
        except Exception as e:
            print("An error occurred due to", e)

    def view_all(self):
        for value in self.user.values():
            print(value)

    def view_deposit(self):
        for values in self.user.values():
            for trans in values[0]['Transaction']:
                if trans['type'] == "Deposit":
                    print(f"{trans}")

    def view_withdrawal(self):
        for values in self.user.values():
            for trans in values[0]['Transaction']:
                if trans['type'] == "Withdrawal":
                    print(f"{trans}")

    def view_transfer(self):
        for values in self.user.values():
            for trans in values[0]['Transaction']:
                if trans['type'] == "Transfer":
                    print(f"{trans}")

class FileHandler:
    def __init__(self, filename):
        self.filename = filename

    def load_file(self):
        if not os.path.exists(self.filename):
            return {}

        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                print("File loaded successfully")
                return data
        except Exception as e:
            print(f"An error occurred while loading file due to {e}")


    def save_file(self, file):
        try:
            with open(self.filename, "w") as f:
                json.dump(file, f, indent=4, default=str)
                print("File saved successfully")
        except Exception as e:
            print(f"An error occurred while saving file due to {e}")



class BankingProgramApplication:
    def __init__(self):
        self.bank = BankingProgram()
        self.file = FileHandler("Bank Database.json")

    def load(self):
        self.bank.user = self.file.load_file()

    def save(self):
        self.file.save_file(self.bank.user)

    def commands(self):
        print("=====================")
        print("1. Register User")
        print("2. Make a Deposit")
        print("3. Make a Withdrawal")
        print("4. Make a Transfer")
        print("5. View all users")
        print("6. View all transactions")
        print("7. View all deposits")
        print("8. View all withdrawal")
        print("9: view all Transfers")
        print("Press 0 to break")
        print("=======================")


    async def execute(self):
        self.load()
        self.commands()

        while True:

            command_map = {
                "1": self.register_user,
                "2": self.deposit_amount,
                "3": self.withdraw_amount,
                "5": self.bank.view_users,
                "6": self.bank.view_all,
                "7": self.bank.view_deposit,
                "8": self.bank.view_withdrawal,
                "9": self.bank.view_transfer
            }

            command = input("Command: ")

            if command == "0":
                self.save()
                break
            elif command == "4":
                await self.make_transfer()
            elif command in command_map:
                command_map[command]()
            else:
                print("Invalid input. Try again")

    def register_user(self):
        while True:
            name = input("Enter name of customer: ")
            validated_name = validate_name(name)
            if validated_name:
                break
        self.bank.register_customer(validated_name)

    def deposit_amount(self):
        while True:
            act_no = input("Enter account number of the customer you want to deposit: ")
            amount = input("Enter amount: ")
            validated_act_no = validate_input(act_no)
            validated_amount = validate_amount(amount)
            if validated_act_no and validated_amount:
                break
        self.bank.depo(validated_act_no, amount)

    def withdraw_amount(self):
        while True:
            act_no = input("Enter account number of the customer you want to withdrawal from: ")
            amount = input("Enter amount: ")
            validated_act_no = validate_input(act_no)
            validated_amount = validate_amount(amount)
            if validated_act_no and validated_amount:
                break
        self.bank.make_withdrawal(validated_act_no, validated_amount)

    async def make_transfer(self):
        while True:
            act_no = input("Enter sender account number: ")
            other_act_no = input("Enter account number of the receiver: ")
            amount = input("Enter amount: ")
            validated_act_no = validate_input(act_no)
            validated_other_act_no = validated_act_no(other_act_no)
            validated_amount = validate_amount(amount)
            if validated_act_no and validated_other_act_no and validated_amount:
                break
        await self.bank.make_transfer(validated_act_no, validated_other_act_no, validated_amount)


async def main():
    app = BankingProgramApplication()
    await app.execute()

asyncio.run(main())


