class BrowserCreationError(Exception):
    pass


class BrowserAlreadyExistsForPlayer(Exception):
    pass


class BrowserNotFoundInRegistry(Exception):
    pass


class FailedParseEventData(Exception):
    pass


class EventDataTypeMismatch(Exception):
    pass


class EventDataValidationError(Exception):
    pass
