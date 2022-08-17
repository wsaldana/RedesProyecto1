from __future__ import annotations
import abc
import logging

from myxmpp.send import SendMsgBot


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
            return None
        elif selection == '2':
            return LogginMenu()
        elif selection == '3':
            return ExitMenu()
        else:
            return WrongOptionMenu()


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


class LoggedMenu(Menu):
    def next(self) -> Menu:
        print(
            '\n==================== USER MENU ===================',
            '\t1) Mostrar todos los usuarios/contactos y su estado ',
            '\t2) Agregar un usuario a los contactos ',
            '\t3) Mostrar detalles de contacto de un usuario ',
            '\t4) Comunicación 1 a 1 con cualquier usuario/contacto ',
            '\t5) Participar en conversaciones grupales ',
            '\t6) Definir mensaje de presencia ',
            '\t7) Enviar/recibir notificaciones ',
            '\t8) Enviar/recibir archivos',
            '\t9) Regresar',
            sep='\n'
        )
        selection = input("Option: ")
        print('')

        if selection == '1':
            self.xmpp.handler()
            return None
        elif selection == '2':
            return None
        elif selection == '3':
            return None
        elif selection == '4':
            return None
        elif selection == '5':
            return None
        elif selection == '6':
            return None
        elif selection == '7':
            return None
        elif selection == '8':
            return None
        elif selection == '9':
            return MainMenu()
        else:
            return WrongOptionMenu()


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
