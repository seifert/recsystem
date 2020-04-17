
import os.path
import tempfile

# recsystem application settings

# Name of the application, this name will be shown in the process list.
# NAME = 'recsystem'

# Function, which is called when application is initialized.
# INIT_HANDLER = 'recsystem.app.init_handler'

# Function, which is called when Tornado applications is initialized.
# APP_SETTINGS_HANDLER = 'recsystem.app.app_settings_handler'

# Function, which is called when SIGUSR1 is received. Function is called
# in the main process and in all workers and service processes.
# SIGUSR1_HANDLER = 'recsystem.app.sigusr1_handler'

# Function, which is called when SIGUSR2 is received. Function is called
# only in process which received signal.
# SIGUSR2_HANDLER = 'recsystem.app.sigusr2_handler'

# Application configuration class name.
CONFIG_CLASS = 'recsystem.config.Config'

# Application context class name.
CONTEXT_CLASS = 'recsystem.context.Context'

# Application management commands
MANAGEMENT_COMMANDS = (
    'recsystem.commands.FetchRss',
)

# Application service processes. Each item is a tuple
# ('path.to.Class', wait_unless_ready, timeout).
SERVICE_PROCESSES = (
    # ('recsystem.processes.DummyProcess', True, 5),
)

# HTTP server interfaces
INTERFACES = {
    'default': {
        # Address/hostname (optional) and port where HTTP server listen to
        # incomming requests.
        'LISTEN': ':8000',

        # Path to desired unix socket
        # 'UNIX_SOCKET': '/run/myapp.sock',

        # Number of the server processes. Positive number, 0 means number
        # of the CPU cores.
        'PROCESSES': 0,

        # URL path to HTTP handler routing.
        'URLS': 'recsystem.urls.urls_default',
    },
}

# Database, content of the dict will be passed as a **kwargs
# into database connect function.
DATABASE = {
    'database': os.path.join(tempfile.gettempdir(), 'recsystem.db'),
}

RSS_FEED = {
    'url': 'http://feeds.bbci.co.uk/news/world/rss.xml',
    'timeout': 5.0,
}
