class SourceFilter:
    def __init__(self, expected_result, name, value):
        # It tell us what we're gonna get by applying this filter
        self.expected_result = expected_result
        self.name = name
        self.value = value

    def set_name(self, name):
        self.name = name

    def set_value(self, value):
        self.value = value
