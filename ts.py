import datetime

def get_ts_next_minute():
    now = datetime.datetime.now()
    # On met secondes et microsecondes à zéro
    rounded = now.replace(second=0, microsecond=0)
    # Si l'heure courante comporte des secondes, on ajoute 1 minute
    if now.second > 0 or now.microsecond > 0:
        rounded += datetime.timedelta(minutes=1)
    return int(rounded.timestamp() * 1000)
    
def get_ts_for_specific_time(hour, minute, day=None, month=None, year=None):
    now = datetime.datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month
    if day is None:
        day = now.day
    
    specific_dt = datetime.datetime(year, month, day, hour, minute, 0, 0)
    return int(specific_dt.timestamp() * 1000)