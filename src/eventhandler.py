class EventHandler:
    """Objekt som håndterer events.
    
    Attributes:
        handlers (dict): Registrerte handler-funksjoner (verdi) med tilhørende event (key).
    
    Methods:
        register_handler(handler, *events): Registrer en ny handler
        handler_event(event): Håndter event
    """

    def __init__(self):
        self.__handlers = {}

    @property
    def handlers(self):
        return list(self.__handlers.keys())

    def register_handler(self, handler, *events):
        """Registrer en ny handler.
        
        Arguments:
            handler (function): Funksjonen som skal trigges når eventen oppstår.
            *events (str): Event-nøkkelordene som skal trigge handlern.
        """

        for event in events:
            self.__handlers[event] = handler

    def handle_event(self, event):
        """Håndter en event
        
        For en gitt event -> kjør tilhørende funksjon.

        Arguments:
            event (str): Event-nøkkelord som trigger en funksjon.
        """

        return self.__handlers[event]