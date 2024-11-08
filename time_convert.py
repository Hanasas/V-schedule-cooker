from datetime import datetime, timedelta

timezone_offsets = {
    'UTC': 0,
    'GMT': 0,
    'BST': 1,    # British Summer Time
    'CET': 1,    # Central European Time
    'CEST': 2,   # Central European Summer Time
    'EET': 2,    # Eastern European Time
    'EEST': 3,   # Eastern European Summer Time
    'MSK': 3,    # Moscow Standard Time
    'MSD': 4,    # Moscow Daylight Time
    'AST': -4,   # Atlantic Standard Time
    'ADT': -3,   # Atlantic Daylight Time
    'EST': -5,   # Eastern Standard Time
    'EDT': -4,   # Eastern Daylight Time
    'CST': 8,    # China Standard Time
    'CDT': 8,    # China Daylight Time (not used, but included for completeness)
    'CST_NA': -6, # Central Standard Time (North America)
    'CDT_NA': -5, # Central Daylight Time (North America)
    'MST': -7,   # Mountain Standard Time
    'MDT': -6,   # Mountain Daylight Time
    'PST': -8,   # Pacific Standard Time
    'PDT': -7,   # Pacific Daylight Time
    'AKST': -9,  # Alaska Standard Time
    'AKDT': -8,  # Alaska Daylight Time
    'HST': -10,  # Hawaii Standard Time
    'HDT': -9,   # Hawaii Daylight Time (rarely used)
    'AEST': 10,  # Australian Eastern Standard Time
    'AEDT': 11,  # Australian Eastern Daylight Time
    'ACST': 9.5, # Australian Central Standard Time
    'ACDT': 10.5,# Australian Central Daylight Time
    'AWST': 8,   # Australian Western Standard Time
    'AWDT': 9,   # Australian Western Daylight Time (rarely used)
    'NZST': 12,  # New Zealand Standard Time
    'NZDT': 13,  # New Zealand Daylight Time
    'IST': 5.5,  # Indian Standard Time
    'PKT': 5,    # Pakistan Standard Time
    'WIB': 7,    # Western Indonesian Time
    'WITA': 8,   # Central Indonesian Time
    'WIT': 9,    # Eastern Indonesian Time
    'JST': 9,    # Japan Standard Time
    'KST': 9,    # Korea Standard Time
    'HKT': 8,    # Hong Kong Time
    'SGT': 8,    # Singapore Time
    'MYT': 8,    # Malaysia Time
    'PHT': 8,    # Philippine Time
    'VET': -4.5, # Venezuelan Standard Time
    'ART': -3,   # Argentina Time
    'BRT': -3,   # Brasilia Time
    'CLT': -4,   # Chile Standard Time
    'CLST': -3,  # Chile Summer Time
    'WAT': 1,    # West Africa Time
    'CAT': 2,    # Central Africa Time
    'EAT': 3,    # East Africa Time
    'SAST': 2,   # South Africa Standard Time
    # 你可以根据需要添加更多的时区偏移
}

def read_target_timezone(config_path):
    with open(config_path, 'r') as file:
        for line in file:
            if line.startswith("Timezone"):
                timezone = line.split(':')[1].strip()
                timezone = timezone.split('(')[0].strip()  # 提取时区缩写
                return timezone
    return None

def parse_time_string(time_str):
    # 解析时间字符串，提取时间和时区信息
    parts = time_str.split()
    if len(parts) == 3:
        time_part = f"{parts[0]} {parts[1]}"
        timezone_part = parts[2]
    elif len(parts) == 2:
        time_part = parts[1]
        timezone_part = parts[0]
    else:
        raise ValueError("Invalid time string format")
    
     # 确保时间字符串格式正确，将 '.' 替换为 ':'
    time_part = time_part.replace('.', ':')
    
    return time_part, timezone_part

def convert_to_target_timezone(time_str, target_timezone_str):
    global timezone_offsets
    # 解析时间字符串
    time_part, current_timezone_str = parse_time_string(time_str)
    time_format = "%I:%M %p"  # 假设时间格式为 "HH:MM AM/PM"
    current_time = datetime.strptime(time_part, time_format)

    # 获取当前时区和目标时区的偏移量
    current_offset = timezone_offsets.get(current_timezone_str, 0)
    target_offset = timezone_offsets.get(target_timezone_str, 0)

    # 计算时间差
    time_difference = target_offset - current_offset

    # 转换时间
    target_time = current_time + timedelta(hours=time_difference)

    # print(f"current time: {current_time.strftime(time_format)}")
    # print(f"Converted time: {target_time.strftime(time_format)}")

    return target_time.strftime(time_format)

# 测试用例
def test_time_conversion():
    test_cases = [
        ('08:00 PM PST', 'CST', '12:00 PM CST'),
        ('08:00 AM PST', 'CST', '12:00 AM CST'),
        ('08:00 PM EST', 'CST', '09:00 AM CST'),
        ('08:00 AM EST', 'CST', '09:00 PM CST'),
    ]

    for time_str, target_timezone, expected in test_cases:
        result = convert_to_target_timezone(time_str, target_timezone)
        assert result == expected, f"Test failed for {time_str}: expected {expected}, got {result}"


if __name__ == "__main__":
    test_time_conversion()