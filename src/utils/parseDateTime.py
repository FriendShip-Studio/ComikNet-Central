import datetime


def parseDateTime(time: datetime.datetime) -> str:

    if datetime.datetime.now() - time < datetime.timedelta(days=1):
        if datetime.datetime.now() - time < datetime.timedelta(hours=1):
            if datetime.datetime.now() - time < datetime.timedelta(minutes=1):
                return f"{(datetime.datetime.now() - time).seconds}秒前"
            else:
                return f"{(datetime.datetime.now() - time).seconds // 60}分钟前"
        else:
            return f"{(datetime.datetime.now() - time).seconds // 3600}小时前"
    else:
        return time.strftime("%Y-%m-%d")
