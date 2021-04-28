from math import ceil


def mkpage(query, schema, page, page_size):
    last_page = ceil(query.count() / page_size)
    return {
        "last_page": last_page,
        "current_page": page,
        "page_size": page_size,
        "contents": schema.dump(
            query[(page - 1) * page_size : page * page_size], many=True
        ),
    }
