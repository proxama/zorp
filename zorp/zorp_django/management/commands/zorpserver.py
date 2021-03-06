"""
Management command to run a Zorp server
"""

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.utils import autoreload

class Command(BaseCommand):
    """
    Command to run a Zorp server.

    Optionally takes an port number or address:port pair.

    If not given, ZORP_SERVER_HOST/ZORP_SERVER_PORT will be fetched from your
    project's settings. If these aren't available, the default values will be
    used.
    """

    help = "Runs a Zorp server"
    args = "[optional port number, or address:port]"

    option_list = BaseCommand.option_list + (
        make_option("--noreload", dest="use_reloader", default=True, action="store_false",
            help="Tells Zorp to NOT use the auto-reloader."),
    )

    def handle(self, address_port="", **options):
        """
        Command entry point.
        """

        import re

        from django.conf import settings

        from zorp import Server
        from zorp.registry import registry
        from zorp.settings import DEFAULT_HOST, DEFAULT_PORT
        from zorp.zorp_django.loading import register_remote_methods_from_apps

        def run_server():
            """
            Run the server.
            """

            # Import all remote_methods.
            loaded_apps = register_remote_methods_from_apps().loaded_apps

            # Display loaded apps.
            self.stdout.write("Loaded apps:\n")
            if loaded_apps:
                for app in loaded_apps:
                    self.stdout.write(" * {}\n".format(app))
            else:
                self.stdout.write(" * (none)")
            self.stdout.write("\n")

            # Display registered methods.
            self.stdout.write("Registered methods:\n")
            if registry.methods:
                for registry_name, method in sorted(registry.methods.iteritems()):
                    self.stdout.write(" * {} => {}.{}\n".format(
                        registry_name,
                        method.__module__, method.__name__
                    ))
            else:
                self.stdout.write(" * (none)")
            self.stdout.write("\n")

            server = Server(address, port)

            self.stdout.write("Server listening on {}:{}\n".format(server.address, server.port))
            if options['use_reloader']:
                self.stdout.write("Auto-reloader: on")
            else:
                self.stdout.write("Auto-reloader: off")
            server.start()

            self.stdout.write("Server exited\n")

        def get_address_port_from_string(string, default_address, default_port):
            """
            Given a string in the format "PORT" or "IP:PORT", return the
            parsed ip/port tuple, using the default values where necessary.
            """

            if not string:
                return default_address, default_port

            address_port_re = re.compile(
                r"^"
                r"(?:(?P<address>\d+\.\d+\.\d+\.\d+):)?"
                r"(?P<port>\d+)"
            )

            match = address_port_re.search(string)
            if match:
                address, port = match.group("address"), match.group("port")

                address = address or default_address
                port = port or default_port

                try:
                    port = int(port)
                except ValueError:
                    pass
                else:
                    return address, port

            raise CommandError("{!r} is neither a valid port number, nor an IP:PORT pair".format(string))

        default_host = getattr(settings, "ZORP_SERVER_HOST", DEFAULT_HOST)
        default_port = getattr(settings, "ZORP_SERVER_PORT", DEFAULT_PORT)

        address, port = get_address_port_from_string(address_port, default_host, default_port)

        if options['use_reloader']:
            autoreload.main(run_server)
        else:
            run_server()
