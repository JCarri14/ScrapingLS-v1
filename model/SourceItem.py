class SourceItem:
    def __init__(self, title, thumbnail, description, created_at, times_shared, comments):
        self.title = title
        self.thumbnail = thumbnail
        self.description = description
        self.created_at = created_at
        self.times_shared = times_shared
        self.comments = comments

    def set_title(self, title):
        self.title = title

    def set_thumbnail(self, thumbnail):
        self.thumbnail = thumbnail

    def set_description(self, description):
        self.description = description

    def set_created_at(self, created_at):
        self.created_at = created_at

    def set_times_shared(self, times_shared):
        self.times_shared = times_shared

    def set_comments(self, comments):
        self.comments = comments
