def build_author_query(author):
    """Build author query string with all permutations of full names and initials."""
    name = author.split(" ")
    first, last = name[0], name[-1]
    query = f"au:{last}_{first} OR au:{last}_{first[0]}"
    if len(name) > 2:
        middle = name[1:-1]
        if len(middle) > 1:
            logging.warning(f"Multiple middle names found: {first} {middle} {last}")
        middle = middle[0]
        query += f" OR au:{last}_{first}_{middle} OR au:{last}_{first}_{middle[0]} OR au:{last}_{first[0]}_{middle[0]}"
    return query
