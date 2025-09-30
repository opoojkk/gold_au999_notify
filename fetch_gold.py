import requests
import json
from datetime import datetime

def fetch_gold_9999_data():
    """爬取上海黄金交易所黄金9999的实时行情数据"""
    url = "https://api.jijinhao.com/quoteCenter/realTime.htm"
    
    params = {'codes': 'JO_71'}
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://quote.cngold.org/gjs/jjs.html',
        'Accept': '*/*',
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        print(f"状态码: {response.status_code}")
        
        content = response.text.strip()
        
        # JSONP格式: var quote_json = {...};
        if 'quote_json' in content:
            # 找到 = 后面的内容
            start_idx = content.find('=') + 1
            json_str = content[start_idx:].strip()
            
            # 移除末尾的分号
            if json_str.endswith(';'):
                json_str = json_str[:-1].strip()
            
            print(f"提取JSON长度: {len(json_str)} 字符")
            
            # 解析JSON
            data = json.loads(json_str)
            print(f"JSON解析成功")
            
            if 'JO_71' in data:
                print("找到JO_71数据")
                return parse_gold_data(data['JO_71'])
            else:
                print("JO_71不在数据中")
                return None
        
        print("未能解析到数据")
        return None
            
    except Exception as e:
        print(f"请求失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def parse_gold_data(raw_data):
    """解析从API获取的黄金数据"""
    try:
        print("\n开始解析数据...")
        print(f"原始数据示例: q63={raw_data.get('q63')}, q80={raw_data.get('q80')}")
        
        def format_value(val, precision=2):
            try:
                if val is None or val == '':
                    return None
                num_val = float(val)
                return round(num_val, precision)
            except:
                return None
        
        # 时间转换
        update_time = None
        if raw_data.get('time'):
            try:
                timestamp = int(raw_data.get('time')) / 1000
                update_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            except:
                update_time = str(raw_data.get('time'))
        
        parsed_data = {
            '商品名称': raw_data.get('showName', '黄金9999'),
            '商品代码': raw_data.get('code', 'JO_71'),
            '最新价': format_value(raw_data.get('q63')),
            '买入价': format_value(raw_data.get('q5')),
            '卖出价': format_value(raw_data.get('q6')),
            '涨跌额': format_value(raw_data.get('q70')),
            '涨跌幅(%)': format_value(raw_data.get('q80'), 2),
            '开盘价': format_value(raw_data.get('q1')),
            '最高价': format_value(raw_data.get('q3')),
            '最低价': format_value(raw_data.get('q4')),
            '昨收价': format_value(raw_data.get('q2')),
            '单位': raw_data.get('unit', '元/克'),
            '更新时间': update_time
        }
        
        print(f"解析完成，最新价: {parsed_data['最新价']}")
        return parsed_data
        
    except Exception as e:
        print(f"解析失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def display_gold_data(data):
    """格式化显示数据，返回字符串格式（去掉=符号）"""
    if not data:
        return "无数据可显示"
    
    result = "上海黄金交易所 - 黄金9999 实时行情\n"
    result += "\n"
    
    for key, value in data.items():
        if value is not None:
            if isinstance(value, float):
                result += f"{key:15s}: {value:.2f}\n"
            else:
                result += f"{key:15s}: {value}\n"
        else:
            result += f"{key:15s}: ----\n"
    
    return result


if __name__ == "__main__":
    print("确保已安装依赖: pip install requests beautifulsoup4\n")
    print("正在获取黄金9999实时数据...\n")
    
    gold_data = fetch_gold_9999_data()
    
    if gold_data:
        result = display_gold_data(gold_data)
        
        # 将格式化后的结果保存到 result.txt
        output_file = 'result.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        
        print(f"数据已保存到 {output_file}")
    else:
        print("获取数据失败")
