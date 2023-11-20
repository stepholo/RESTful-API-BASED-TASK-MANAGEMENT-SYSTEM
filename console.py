#!/usr/bin/python3

"""
This is the entry point of the command interpreter
"""

import cmd
import os
from tasks.base_task import TaskManager


class TASKCommand(cmd.Cmd):
    prompt = "(task) "

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

    def do_create(self, arg):
        """
            Creates a new instance of BaseModel, and prints the id
        """
        # new_instance = TaskManager()
        if not arg:
            print('** class name missing **')
            return

        class_name = arg.strip()
        if class_name != 'TaskManager':
            print('** class does not exist **')
            return

        user_name = input('Enter user name: ')
        user_email = input('Enter user email: ')

        try:
            new_instance = TaskManager(
                user_name=user_name, user_email=user_email)
            print(new_instance.id)
        except Exception as e:
            print(f'Error creating instance: {str(e)}')


if __name__ == '__main__':
    TASKCommand().cmdloop()
