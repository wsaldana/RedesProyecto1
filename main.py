from __future__ import annotations
import abc
import logging

from myxmpp.send import SendMsgBot, Register


logging.basicConfig(level='ERROR', format='%(levelname)-8s %(message)s')


class Menu(abc.ABC):
    @abc.abstractclassmethod
    def next(self) -> Menu:
        pass


class WrongOptionMenu(Menu):
    def next(self) -> Menu:
        print("Invalid option...")
        return MainMenu()


class ExitMenu(Menu):
    def next(self) -> Menu:
        print("See you later...")
        return None


class MainMenu(Menu):
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
    current_menu: Menu = MainMenu()

    def execute(self):
        next_menu = self.current_menu.next()
        self.current_menu = next_menu

        return self.current_menu


def run():
    entry_point = Executer()

    while True:
        next_menu = entry_point.execute()

        if not next_menu:
            break


if __name__ == '__main__':
    run()
