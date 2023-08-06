# coding: utf-8

"""
    django-reversion-compare unittests
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyleft: 2017 by the django-reversion-compare team, see AUTHORS for more details.
    :created: 2017 by Jens Diemer <github.com@jensdiemer.de>
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import re


def print_db_queries(queries):
    queries_data = {}
    for query in queries:
        sql = query["sql"]
        queries_data.setdefault(sql, 0)
        queries_data[sql] += 1
    duplicates = sum([count - 1 for count in list(queries_data.values())])
    print("-" * 79)
    print("total queries....: %i" % len(queries))
    print("unique queries...: %i" % len(queries_data))
    print(f"duplicate queries: {duplicates:d}")
    print()
    for query, count in sorted(queries_data.items()):
        query = re.sub(r'["\'`]', "", query)
        print(f"{count} x {query}")
    print("-" * 79)
