import datetime

def getPriority(importance, duration, dateAdded, currentDate):
        return (importance * (currentDate - dateAdded)) + (datetime.timedelta(hours=1)*duration)
