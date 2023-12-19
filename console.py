#!/usr/bin/python3

"""
This is the entry point of the command interpreter
"""

from tasks import storage
from tasks.users import User
from tasks.tasks import Task
from datetime import datetime, timedelta
import cmd
import os


class TASKCommand(cmd.Cmd):
    prompt = "(task) "

    def preloop(self):
        """Method to execute before any command is called"""
        print("Welcome to Task Command interpreter. "
              "Type `help` to view all commands")

    def emptyline(self):
        """Do nothing upon recieving an empty line."""
        pass

    def do_clear(self, line):
        """Clears the screen"""
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """Exit the program"""
        print("")
        return True

    def do_create_user(self, arg):
        """Create a single user: Please provide your
            first name, last name and email address in that order
            usage: create_user Brian Oloo oloobrian@gmail.com
        """
        args = arg.split()
        if len(args) != 3:
            print('please provide your first, last names and email address')
            return

        first_name = args[0].strip('"')
        last_name = args[1].strip('"')
        email_address = args[2].strip('"')

        user = User(
            first_name=first_name,
            last_name=last_name,
            email_address=email_address)
        storage.new(user)
        try:
            storage.save(user)
        except Exception as e:
            print(e)
            return
        user = storage.get_user_by_email(User, email_address)
        print(f"{user.first_name} {user.last_name} has been created")

    def do_create_task(self, arg):
        """Create a single task for an existing user: Please provide
            the following details:
                User's email address
                Task title
                Task's description e.g study_my_books
                Task's priority level - high, low, medium
                Task's status - pending or done
                Task's number of days to complete or 0 for none
            Please provide them in that order given
        usage: create_task oloobrian@gmail.com Code do_some_coding high done 0
        """
        if not arg:
            print("** Provide the required parameters"
                  "use `help create_task` for more information **")
            return
        else:
            args = arg.split()
        if len(args) != 6:
            ensure = ("Provide the following details respectively \n\t"
                      "User's email address \n\t"
                      "Task title \n\t"
                      "Task's description e.g study_my_books \n\t"
                      "Task's priority level - high, low, medium \n\t"
                      "Task's status - pending or done \n\t"
                      "Task's number of days to complete or 0 for none")
            print(ensure)
            return

        email_address = args[0]
        title = args[1].strip('"').title()
        description = args[2].strip('"').replace('_', ' ')
        priority_level = args[3].strip('"')
        status = args[4].strip('"')
        number_of_days = int(args[5].strip('"'))

        try:
            task = Task(
                email_address=email_address,
                priority_level=priority_level,
                days_to_complete=number_of_days,
                completion_status=status)
            task.email_address = email_address
            task.description = description
            task.title = title
            task.days_to_complete = number_of_days
        except Exception as e:
            print(e)
            return

        try:
            storage.new(task)
            storage.save()
        except Exception as e:
            print(e)
            return

        for key, value in task.to_dict().items():
            print(f'{key} - {value}')

    def do_update_user(self, arg):
        """Update an existing user's details a user has to provide the correct
            information to be updated
            usage: update_user oloobrian@gmail.com
        """
        if not arg:
            print("** Provide email address of the user you'd "
                  "prefer to change their information")

        email_address = arg
        try:
            user = storage.get_user_by_email(User, email=email_address)
        except Exception as e:
            print(e)
            return
        if user:
            print("Old user's details are as follows: {} {} {}".format(
                user.first_name, user.last_name, user.email_address
            ))
            first_name = input("what is the new first name?: ")
            last_name = input("What is the new last name? ")
            email_address = input("What is the new email addess? ")
            user.first_name = first_name
            user.last_name = last_name
            try:
                user.save()
                user.update_email_address(email_address)
            except Exception as e:
                print(e)
                return
            user = storage.get_user_by_email(User, email=email_address)
            print("Updated user's details are as follows: {} {} {}".format(
                user.first_name, user.last_name, user.email_address
            ))
        else:
            print('** No user with such email address** ')
            return

    def do_update_task(self, arg):
        """Method to update task - provide user's email address and task title
            in that order - choose option of what to update
            usage: update_task oloobrian89@gmail.com "Check_TA"
        """
        if not arg:
            print("** Provide user's email address and task title **")
            return

        args = arg.split()
        if len(args) != 2:
            print("** Provide user's email address  and task title **")
            return

        email_address = args[0].strip('"')
        title = args[1].strip('"').replace('_', ' ')
        tasks = storage.get_task(Task, email=email_address)

        found_task = None
        for task in tasks:
            if task.title == title:
                found_task = task
                break
        if not found_task:
            print("** No such task title found **")
            return

        options = {
            1: 'title',
            2: 'description',
            3: 'priority_level',
            4: 'completion_status',
            5: 'days_to_complete'
        }

        print("Choose an option to update:")
        for key, value in options.items():
            print(f"{key}. {value.capitalize()}")

        choice = int(input("Enter your choice: "))
        if choice not in options.keys():
            print("Invalid choice")
            return

        if choice == 1:
            new_title = input('Enter the new task title: ')
            found_task.title = new_title
        elif choice == 2:
            new_description = input('Enter the new task description: ')
            found_task.description = new_description
        elif choice == 3:
            new_priority = input("Enter the new priority level "
                                 "(high, low, medium): ")
            found_task.priority_level = new_priority.lower()
        elif choice == 4:
            new_completion_status = input("Enter the completion status "
                                          "(pending, done): ")
            if new_completion_status == 'done':
                found_task.completion_status = new_completion_status.lower()
                found_task.days_to_complete = 0
                found_task.deadline = datetime.now()
            else:
                found_task.completion_status = new_completion_status.lower()
        elif choice == 5:
            new_days_to_complete = int(input("Enter the number of days"
                                             "remaining (0 for no days): "))
            if new_days_to_complete > 0:
                found_task.days_to_complete = new_days_to_complete
                found_task.deadline = datetime.now() + timedelta(
                    days=new_days_to_complete)
            else:
                found_task.days_to_complete = new_days_to_complete
                found_task.deadline = datetime.now()
        else:
            print('Input the required numbers')
            return

        found_task.save()
        print("Task updated successfully")

    def do_delete_user(self, arg):
        """Delete an existing user - Provide the email for the user
            usage: delete_user oloobrian@gmail.com
        """
        if not arg:
            print('** Provide email address for the user to delete **')
            return

        email_address = arg.lower()
        users = storage.all(User)
        count = 0
        for user in users:
            if user:
                count = count + 1
        print(f'The number of users is {count}')
        if count > 0:
            user = storage.get_user_by_email(User, email=email_address)
            storage.delete(user)

        users = storage.all(User)
        count = 0
        for user in users:
            if user:
                count = count + 1
        print(f'The remaining number of users is {count}')

    def do_delete_task(self, arg):
        """Delete a specific task created by a user
            Provide email address and task title
            usage: delete_task oloobrian@gmail.com Code
        """
        if not arg:
            print('** Provide email address and tasks title **')
            return

        args = arg.split()
        if len(args) != 2:
            print('** Provide email address and tasks title **')
            return

        email_address = args[0].lower()
        title = args[1].strip('"')
        tasks = storage.get_task(Task, email=email_address)
        count = 0
        if tasks:
            for task in tasks:
                count = count + 1
            print(f'Their are {count} task(s)')
            for task in tasks:
                if task.title == title:
                    storage.delete(task)
        else:
            print('** No task associated with such email address **')
            return

        tasks = storage.get_task(Task, email=email_address)
        count = 0
        if tasks:
            for task in tasks:
                count = count + 1
        print(f'Their are {count} task(s) remaining')

    def do_show_specific_user(self, arg):
        """Show specific user - provide user's email address
            usage: show_specific_user oloobrian@gmail.com"""
        if not arg:
            print("** Provide user's email address **")
            return

        user = storage.get_user_by_email(User, email=arg)
        if user:
            print('{}.{} {} - {}'.format(
                user.id, user.first_name, user.last_name, user.email_address
            ))
        else:
            print('** No user with such email **')

    def do_show_all_users(self, arg):
        """Show all users
            Usage: show_all_users User
        """
        if not arg:
            print('usage: show_all_users users')
            return
        users = storage.all(User)
        if users:
            for user in users:
                print('{}.{} {} - {}'.format(
                    user.id, user.first_name,
                    user.last_name, user.email_address))
        else:
            print('No users found')
            return

    def do_show_all_userspecific_tasks(self, arg):
        """Show all task for a specific user
            usage: show_all_userspecifc_tasks oloobrian@gmail.com
        """
        if not arg:
            print("** Provide user's email address **")
            return
        email_address = arg.lower()
        tasks = storage.get_task(Task, email=email_address)
        if tasks:
            for task in tasks:
                print("{}. {}; {}; status - {}; priority - {}; deadline - {}".
                      format(task.task_id, task.title,
                             task.description, task.completion_status,
                             task.priority_level, task.deadline
                             ))
        else:
            print('** Their are no task for such user **')

    def do_show_task_priority(self, arg):
        """Show task for each user based on priority level (high, low, medium)
            usage show_task_priority oloobrian@gmail.com high
        """
        if not arg:
            print('** provide user email and task priority **')
            return

        args = arg.split()
        if len(args) != 2:
            print('** provide user email and task priority **')
            return

        email_address = args[0].lower()
        priority = args[1].lower()
        tasks = storage.get_task(Task, email=email_address)
        if tasks:
            for task in tasks:
                if task.priority_level == priority:
                    print("{}. {}; {}; status-{}; priority - {}; deadline-{}".
                          format(task.task_id, task.title,
                                 task.description, task.completion_status,
                                 task.priority_level, task.deadline
                                 ))
                else:
                    pass
        else:
            print('** No task has been allocated with that user **')
            return

    def do_show_task_status(self, arg):
        """Show user specific task by completion status (pending or done)
            usage show_task_status oloobrian@gmail.com done
        """
        if not arg:
            print('** provide user email and task completion status **')
            return

        args = arg.split()
        if len(args) != 2:
            print('** provide user email and task completion status **')
            return

        email_address = args[0].lower()
        status = args[1].lower()
        tasks = storage.get_task(Task, email=email_address)
        if tasks:
            for task in tasks:
                if task.completion_status == status:
                    print("{}. {}; {}; status-{}; priority - {}; deadline-{}".
                          format(task.task_id, task.title,
                                 task.description, task.completion_status,
                                 task.priority_level, task.deadline
                                 ))
                else:
                    pass
        else:
            print('** No task has been allocated with that user **')
            return


if __name__ == '__main__':
    TASKCommand().cmdloop()
