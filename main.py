"""
Simple CLI chat implementing XMPP protocol.

Main will use state pattern to change the state
of the program execution.
"""

from __future__ import annotations
import abc
import logging

from myxmpp.send import SendMsgBot, Register


logging.basicConfig(level='ERROR', format='%(levelname)-8s %(message)s')


class Menu(abc.ABC):
    """Menu abstract class"""

    @abc.abstractclassmethod
    def next(self) -> Menu:
        """Passes to the next program state

        Returns:
            Menu: Next menu to execute
        """
        pass


class WrongOptionMenu(Menu):
    """Menu for invalid options"""

    def next(self) -> Menu:
        print("Invalid option...")
        return MainMenu()


class ExitMenu(Menu):
    """Exit menu"""

    def next(self) -> Menu:
        print("See you later...")
        return None


class MainMenu(Menu):
    """Main menu which contains the options
    with the main functionalities
    """

    def next(self) -> Menu:
        print(
            '\n==================== MAIN MENU ===================',
            '\t1) Registrar una nueva cuenta en el servidor ',
            '\t2) Iniciar sesión con una cuenta ',
            '\t3) Salir',
            sep='\n'
        )
        selection = input("Option: ")
        print('')

        if selection == '1':
            return RegisterMenu()
        elif selection == '2':
            return LogginMenu()
        elif selection == '3':
            return ExitMenu()
        else:
            return WrongOptionMenu()


class RegisterMenu(Menu):
    """Menu for registering a new user"""

    def next(self) -> Menu:
        username = input("Username: ")
        password = input("Password: ")

        xmpp = Register(username, password)
        xmpp.register_plugin('xep_0030')
        xmpp.register_plugin('xep_0004')
        xmpp.register_plugin('xep_0066')
        xmpp.register_plugin('xep_0077')
        xmpp.register_plugin('xep_0199')
        xmpp.register_plugin('xep_0045')
        xmpp.connect()
        xmpp.process(forever=False)

        print("Done")

        return MainMenu()


class LogginMenu(Menu):
    """Menu for logging an account"""

    def next(self) -> Menu:
        username = input("Username: ")
        password = input("Password: ")

        xmpp = SendMsgBot(username, password)
        xmpp.register_plugin('xep_0030')
        xmpp.register_plugin('xep_0199')
        xmpp.register_plugin('xep_0045')
        xmpp.connect()
        print('\nLoading...')
        xmpp.process(forever=False)

        return MainMenu()


class Executer:
    """Handles the program execution state
    and executes the next state
    """

    # Set initial state
    current_menu: Menu = MainMenu()

    def execute(self):
        """Executes current state and passes to next one"""
        next_menu = self.current_menu.next()
        self.current_menu = next_menu

        return self.current_menu


def run():
    """Starts the program state"""

    entry_point = Executer()

    while True:
        next_menu = entry_point.execute()

        if not next_menu:
            break


if __name__ == '__main__':
    run()
