import re

# 匹配日期（日月年）
DATE_PATTERN = r'\d{1,2}/\d{1,2}/\d{4}'  # 日期格式示例：12/31/2023
# 匹配星期（全写或缩写）
WEEKDAY_PATTERN = r'Mon(\.|day)?|Tue(\.|sday)?|Wed(\.|nesday)?|Thu(\.|rsday)?|Fri(\.|day)?|Sat(\.|urday)?|Sun(\.|day)?|mon(\.|day)?|tue(\.|sday)?|wed(\.|nesday)?|thu(\.|rsday)?|fri(\.|day)?|sat(\.|urday)?|sun(\.|day)?'
# 匹配具体时间
TIME_PATTERN = r'\d{1,2}[:.]\d{2}([:.]\d{2})?\s*(AM|PM)?'  # 具体时间格式示例：08:00 AM
# 匹配时区标志
TIMEZONE_PATTERN = r'(UTC|GMT|EST|EDT|CST|CDT|PST|PDT|JST)'  # 可以添加其他时区标志

TEXT_IN = 1
DATE_IN = 2
WEEKDAY_IN = 3
TIME_IN = 4
ZONE_IN = 5

def is_time_string(input_str):
    # 判断是否匹配任何一种时间格式
    # print(input_str)
    if re.match(DATE_PATTERN, input_str):
        # print("data")
        return DATE_IN
    elif input_str.isdigit():
        # print("digit")
        return DATE_IN
    elif re.match(WEEKDAY_PATTERN,input_str):
        # print("weekday")
        return WEEKDAY_IN
    elif re.match(TIME_PATTERN,input_str):
        # print("time")
        return TIME_IN
    elif re.match(TIMEZONE_PATTERN,input_str):
        # print("zone")
        return ZONE_IN
    else:
        # print("text")
        return TEXT_IN

# 测试函数
test_strings = [
    "19",
    "12/31/2023",
    "Monday",
    "08:00 AM",
    "CST",
    "InvalidString",
]
if __name__ == '__main__':
    for string in test_strings:
        print(f"{string}: {is_time_string(string)}")
