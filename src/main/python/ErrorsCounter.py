class ErrorsCounter:
    _instance = None
    _error_count = 0

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ErrorsCounter, cls).__new__(cls)
        return cls._instance

    @classmethod
    def increment(cls):
        cls._error_count += 1

    @classmethod
    def reset(cls):
        cls._error_count = 0

    @classmethod
    def get_count(cls):
        return cls._error_count
