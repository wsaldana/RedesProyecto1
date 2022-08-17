import slixmpp
from slixmpp.exceptions import IqError, IqTimeout

from myxmpp.accounts.user import User


class SendMsgBot(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        self.user = User(jid, password)
        slixmpp.ClientXMPP.__init__(
            self,
            self.user.username,
            self.user.password
        )
        self.add_event_handler("session_start", self.start)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()

        while True:

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
                '\t9) Desconectar',
                '\t10) Eliminar cuenta',
                sep='\n'
            )
            selection = input("Option: ")
            print('')

            if selection == '1':
                await self.list_contacts()
            elif selection == '2':
                username = input('Username: ')
                await self.add_contact(username)
            elif selection == '3':
                username = input('Username: ')
                await self.contact_details(username)
            elif selection == '4':
                username = input('Username: ')
                msg = input("Message: ")
                await self.send_msg(msg, username)
            elif selection == '5':
                group = input('Group name: ')
                msg = input("Message: ")
                await self.send_group_msg(msg, group)
            elif selection == '6':
                print('chat, away, dnd')
                print('Available, Unavailable, Do not Disturb')
                presence = input('Presence: ')
                status = input("Status: ")
                await self.set_presence(presence, status)
            elif selection == '7':
                pass
            elif selection == '8':
                pass
            elif selection == '9':
                break
            elif selection == '10':
                self.register_plugin('xep_0030')
                self.register_plugin('xep_0066')
                self.register_plugin('xep_0199')
                self.register_plugin('xep_0004')
                self.register_plugin('xep_0077')

                response = self.Iq()
                response['type'] = 'set'
                response['from'] = self.boundjid.user
                response['register']['remove'] = True
                response.send()

                self.disconnect()
            elif selection == '11':
                pass
            elif selection == '12':
                pass
            elif selection == '13':
                pass
            else:
                print("\nIvalid option...")

        self.disconnect()

    async def list_contacts(self):
        print('CONTACT LIST:')
        groups = self.client_roster.groups()

        for group in groups:
            for username in groups[group]:
                name = self.client_roster[username]['name']
                if username != self.jid:
                    if name:
                        print('Name: ', name)
                    print('Username: ', username)

                    connections = self.client_roster.presence(username)
                    for _, status in connections.items():
                        if status['status'] == '':
                            status = 'online'
                        else:
                            status = status['status']
                        print('Status: ', status)

    async def add_contact(self, username):
        try:
            self.send_presence_subscription(pto=username)
        except Exception as err:
            print('Something went wrong... ', str(err))

    async def contact_details(self, username):
        self.get_roster()

        contact = self.client_roster[username]
        if contact['name']:
            print('Nombre: ', contact['name'], '\n')
        print('Username: ', username, '\n')
        connections = self.client_roster.presence(username)

        if connections == {}:
            print('Status: Offline')
        else:
            for client, status in connections.items():
                if status['status'] == '':
                    status = 'online'
                else:
                    status = status['status']
                print('Status: ', status)

    async def send_msg(self, message: str, to_jid: str):
        self.send_message(mto=to_jid,
                          mbody=message,
                          mtype='chat')

    async def send_group_msg(self, message, group):
        self.send_message(
            mto=group+"@conference.alumchat.fun",
            mbody=message,
            mtype='groupchat'
        )

    async def set_presence(self, presence, status):
        try:
            self.send_presence(pshow=presence, pstatus=status)
        except IqError:
            print('Something went wrong...')
        except IqTimeout:
            print('Timeout, server must be busy...')

    async def disconnect_session(self):
        self.disconnect()
