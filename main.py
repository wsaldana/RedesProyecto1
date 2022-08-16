from __future__ import annotations
import abc
import logging
from argparse import ArgumentParser

from myxmpp.send import SendMsgBot
from myxmpp.accounts.user import User


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
            '1) Registrar una nueva cuenta en el servidor ',
            '2) Iniciar sesión con una cuenta ',
            '3) Cerrar sesión con una cuenta ',
            '4) Eliminar la cuenta del servidor',
            '5) Salir',
            sep='\n'
        )
        selection = input()

        if selection == '1':
            return None
        elif selection == '2':
            return None
        elif selection == '3':
            return None
        elif selection == '4':
            return None
        elif selection == '5':
            return ExitMenu()
        else:
            return WrongOptionMenu()


class LogginMenu(Menu):
    def next(self) -> Menu:
        username = input("Username: ")
        password = input("Password: ")

        user = User(username, password)


class LoggedMenu(Menu):
    def next(self) -> Menu:
        print(
            '1) Mostrar todos los usuarios/contactos y su estado ',
            '2) Agregar un usuario a los contactos ',
            '3) Mostrar detalles de contacto de un usuario ',
            '4) Comunicación 1 a 1 con cualquier usuario/contacto ',
            '5) Participar en conversaciones grupales ',
            '6) Definir mensaje de presencia ',
            '7) Enviar/recibir notificaciones ',
            '8) Enviar/recibir archivos',
            '9) Regresar',
            sep='\n'
        )
        selection = input()

        if selection == '1':
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
            return ExitMenu()
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
    parser = ArgumentParser(description=SendMsgBot.__doc__)

    # Output verbosity options.
    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.INFO)
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.INFO)

    # JID and password options.
    parser.add_argument("-j", "--jid", dest="jid",
                        help="JID to use")
    parser.add_argument("-p", "--password", dest="password",
                        help="password to use")
    parser.add_argument("-t", "--to", dest="to",
                        help="JID to send the message to")
    parser.add_argument("-m", "--message", dest="message",
                        help="message to send")

    args = parser.parse_args()

    # Setup logging.
    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')

    if args.jid is None:
        args.jid = input("Username: ")
    if args.password is None:
        args.password = input("Password: ")
    if args.to is None:
        args.to = input("Send To: ")
    if args.message is None:
        args.message = input("Message: ")

    # Setup the EchoBot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    xmpp = SendMsgBot(args.jid, args.password, args.to, args.message)
    # Service Discovery
    xmpp.register_plugin('xep_0030')
    # XMPP Ping
    xmpp.register_plugin('xep_0199')

    # Connect to the XMPP server and start processing XMPP stanzas.
    xmpp.connect()
    xmpp.process(forever=False)
