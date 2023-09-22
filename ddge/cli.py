from datetime import datetime
from argparse import ArgumentParser

from rich.table import Table
from rich.prompt import Prompt
from rich.console import Console
from rich.traceback import install

from .api import Client
from .storage import Storage, DEFAULT_DATA, DEFAULT_CONFIG_PATH

install(show_locals=True)


class CLI:
    def __init__(self, client = None, storage = None) -> None:
        self._client = client
        self._storage = storage
        self.console = Console()

    @property
    def client(self) -> Client:
        if not self._client:
            raise ValueError("Client not set!")
        return self._client

    @client.setter
    def client(self, client: Client):
        self._client = client

    @property
    def storage(self) -> Storage:
        if not self._storage:
            raise ValueError("Storage not set!")
        return self._storage

    @storage.setter
    def storage(self, storage: Storage):
        self._storage = storage

    def aliases(self):
        table = self.alias_table(self.storage.aliases)
        self.console.print(table)

    def login(self):
        self.client.otp()
        otp = self.get_otp()
        self.client.full_login(otp)
        self.storage.save_credentials(
            self.client.token, # type: ignore
            self.client.access_token, # type: ignore
            self.client.username
        )
        self.console.print(f'[bold green]Succesfully[/bold green] logged in as [bold red]{self.client.username}@duck.com[/bold red]')
        self.console.print(f'[bold green]-> {self.client.real_email}[/bold green]')

    def generate_alias(self):
        alias = self.client.generate_alias()
        self.storage.add_alias(alias)
        self.console.print(f'[bold green]{alias}@duck.com[/bold green]')

    def remove_alias(self, key_like):
        alias = self.storage.remove_alias(key_like)
        table = self.alias_table([alias])
        table.title = "Removed alias"
        self.console.print(table)

    def logout(self):
        self.storage.data = {**DEFAULT_DATA}
        self.storage.save()

    def alias_table(self, aliases: list[dict]):
        table = Table()
        table.add_column("Index", style="bold yellow")
        table.add_column("Alias")
        table.add_column("Creation Date")
        for index, alias in enumerate(aliases):
            table.add_row(str(index), f"{alias['address']}@duck.com",
                          datetime.fromtimestamp(alias['created']).strftime('%c'))
        return table

    def get_otp(self):
        return Prompt.ask("Enter your [bold red]OTP[/bold red] code or url [italic](it may take a while for the email to arrive)[/italic]")


def main():
    cli = CLI()

    parser = ArgumentParser("ddge", description="DuckDuckGo Email CLI")
    parser.add_argument("-c", "--config", help="Custom config path.", default=DEFAULT_CONFIG_PATH)
    subparsers = parser.add_subparsers(title='actions', required=False)

    login = subparsers.add_parser("login",
                           help="Allows you to login using the OTP code and saves the credentials.")
    login.add_argument("username", help="The @duck.com username.")
    login.set_defaults(func=cli.login)

    logout = subparsers.add_parser("logout",
                           help="Deletes the locally saved credentials.")
    logout.set_defaults(func=cli.logout)

    generate = subparsers.add_parser("generate",
                           help="The default action. Generates an alias")
    generate.set_defaults(func=cli.generate_alias)

    aliases = subparsers.add_parser("aliases",
                           help="Lists the created aliases.")
    aliases.set_defaults(func=cli.aliases)

    remove = subparsers.add_parser("remove",
                           help="Delete the alias from the local storage.")
    remove.add_argument("key_like", help="index, full alias or alias username(the part before @)")
    remove.set_defaults(func=cli.remove_alias, pass_=['key_like'])

    args = parser.parse_args()

    storage = Storage(args.config)
    username = getattr(args, 'username', None)
    if username:
        username = username.split("@")[0]
    client = Client(username or storage.username, storage.token, storage.access_token)

    cli.client = client
    cli.storage = storage

    if not hasattr(args, 'func'):
        cli.generate_alias()
    else:
        args.func(**{k:v for k, v in args.__dict__.items()
                     if k in getattr(args, 'pass_', [])})
