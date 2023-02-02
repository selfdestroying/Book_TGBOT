# Creating user template
user_dict_template = {'page': 1,
                      'bookmarks': set()}

# Initializing database
user_db: dict[int, dict[str, int | set]] = {}