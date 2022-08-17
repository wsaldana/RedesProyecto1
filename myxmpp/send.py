import slixmpp

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
                '\t9) Regresar',
                sep='\n'
            )
            selection = input("Option: ")
            print('')

            if selection == '1':
                await self.list_contacts()
            elif selection == '2':
                pass
            elif selection == '3':
                pass
            elif selection == '4':
                pass
            elif selection == '5':
                pass
            elif selection == '6':
                pass
            elif selection == '7':
                pass
            elif selection == '8':
                pass
            elif selection == '9':
                break
            elif selection == '10':
                pass
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
                        print('Estado: ', status)

    async def send_msg(self, message: str, to_jid: str):
        self.send_message(mto=to_jid,
                          mbody=message,
                          mtype='chat')

    async def disconnect_session(self):
        self.disconnect()
