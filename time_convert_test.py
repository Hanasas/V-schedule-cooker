from datetime import datetime, timedelta
from timezone import timezone_offsets

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

    print(f"current time: {current_time.strftime(time_format)}")
    print(f"Converted time: {target_time.strftime(time_format)}")

    return target_time.strftime(time_format) + ' ' + target_timezone_str

# 示例用法
config_path = 'config.txt'
target_timezone = read_target_timezone(config_path)
time_str = '08:00 PM PST'  # 假设时间字符串为 "08:00 PM PST"

converted_time = convert_to_target_timezone(time_str, target_timezone)
print(f"Converted time: {converted_time}")

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

test_time_conversion()