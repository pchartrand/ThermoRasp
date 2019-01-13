from scheduling.timeutils import time_to_minutes


def series_to_json(series):
    as_json = []
    for n, serie in enumerate(series):
        serie_as_json = []
        for point in serie:
            date_value = time_to_minutes(point[0])
            value = round(point[1], 1)
            serie_as_json.append(
                dict(
                    date=date_value,
                    value=value
                )
            )
        as_json.append(serie_as_json)
    return as_json