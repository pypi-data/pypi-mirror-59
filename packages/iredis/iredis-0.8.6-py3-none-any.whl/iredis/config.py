class Config:
    """
    Global config, set once on start, then
    become readonly, never change again.

    :param raw: weather write raw bytes to stdout without any
        decoding.
    :param decode: How to decode bytes response.(For display and
        Completers)
        default is None, means show literal bytes. But completers
        will try use utf-8 decoding.
    """

    def __init__(self):
        self.raw = False
        self.completer_max = 300
        self.transaction = False
        # for transaction render
        self.queued_commands = []
        # show command hint?
        self.newbie_mode = False
        # display zset withscores?
        self.withscores = False
        self.version = "Unknown"
        self.no_version_reason = None
        self.rainbow = False
        self.retry_times = None
        self.socket_keepalive = True
        self.decode = None
        self.no_info = False

    def __setter__(self, name, value):
        # for every time start a transaction
        # clear the queued commands first
        if name == "transaction" and value is True:
            self.queued_commands = []
        super().__setattr__(name, value)


config = Config()
