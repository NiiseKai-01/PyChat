from textual.app import App, ComposeResult
from textual.widgets import Input, Static
from textual.containers import VerticalScroll
import socket
import threading

host = "127.0.0.1"
port = 55555

nickname = input("Enter nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


class ChatApp(App):

    CSS = """
    Screen {
        layout: vertical;
    }

    #chat {
        height: 1fr;
        border: solid green;
    }

    #input {
        dock: bottom;
        height: 3;
    }
    """

    def compose(self) -> ComposeResult:
        yield VerticalScroll(id="chat")
        yield Input(placeholder="Type message...", id="input")

    def on_mount(self):
        thread = threading.Thread(target=self.receive_messages, daemon=True)
        thread.start()

    def receive_messages(self):
        while True:
            try:
                message = client.recv(1024).decode()

                if message == "NICK":
                    client.send(nickname.encode())
                else:
                    self.call_from_thread(self.add_message, message)

            except:
                break

    def add_message(self, message):
        chat = self.query_one("#chat", VerticalScroll)
        chat.mount(Static(message))
        chat.scroll_end()

    def on_input_submitted(self, event: Input.Submitted):
        message = f"{nickname}: {event.value}"
        client.send(message.encode())
        event.input.value = ""


if __name__ == "__main__":
    ChatApp().run()