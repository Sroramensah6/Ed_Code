import datetime
import math
# regular expressions
# using re to parse data and
# fugure out what our word count is actually is
import re

from django.utils.html import strip_tags


def words_count(html_string):
    world_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+', world_string)
    count = len(matching_words)
    return count


def get_read_time(html_string):
    count = len(html_string)
    read_time_min = math.ceil(count/200.0)  # assuming 200wrpm reading
    # read_time_sec = read_time_min * 60
    # read_time = str(datetime.timedelta(seconds=read_time_sec))
    read_time = str(datetime.timedelta(minutes=read_time_min))
    return read_time
