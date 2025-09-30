import requests
import json
import os
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


def format_telegram_message(data):
    """格式化为 Telegram 消息"""
    if not data:
        return "❌ 获取黄金价格失败"
    
    # 判断涨跌
    change_pct = data.get('涨跌幅(%)')
    if change_pct and change_pct > 0:
        trend = "📈"
    elif change_pct and change_pct < 0:
        trend = "📉"
    else:
        trend = "➖"
    
    message = f"{trend} 上海黄金交易所 - 黄金9999\n\n"
    
    # 关键数据
    latest_price = data.get('最新价')
    change_amount = data.get('涨跌额')
    change_pct = data.get('涨跌幅(%)')
    
    if latest_price:
        message += f"💰 最新价: {latest_price:.2f} {data.get('单位', '元/克')}\n"
    
    if change_amount is not None and change_pct is not None:
        sign = "+" if change_amount >= 0 else ""
        message += f"📊 涨跌: {sign}{change_amount:.2f} ({sign}{change_pct:.2f}%)\n"
    
    message += "\n"
    
    # 详细数据
    if data.get('开盘价'):
        message += f"开盘价: {data['开盘价']:.2f}\n"
    if data.get('最高价'):
        message += f"最高价: {data['最高价']:.2f}\n"
    if data.get('最低价'):
        message += f"最低价: {data['最低价']:.2f}\n"
    if data.get('昨收价'):
        message += f"昨收价: {data['昨收价']:.2f}\n"
    
    if data.get('更新时间'):
        message += f"\n🕒 更新时间: {data['更新时间']}"
    
    return message


def send_telegram_message(message):
    """发送消息到 Telegram"""
    bot_token = os.getenv('TG_BOT_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("错误: 缺少 TG_BOT_TOKEN 或 TG_CHAT_ID 环境变量")
        return False
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'  # 可选: 支持 HTML 格式
    }
    
    try:
        response = requests.post(url, data=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Telegram 消息发送成功")
            return True
        else:
            print(f"❌ Telegram 发送失败: {response.status_code}")
            print(f"响应: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Telegram 发送异常: {e}")
        return False


if __name__ == "__main__":
    print("正在获取黄金9999实时数据...\n")
    
    gold_data = fetch_gold_9999_data()
    
    if gold_data:
        print("\n" + "="*50)
        print("数据获取成功，准备发送到 Telegram...")
        print("="*50 + "\n")
        
        # 格式化消息
        telegram_msg = format_telegram_message(gold_data)
        
        # 发送到 Telegram
        send_telegram_message(telegram_msg)
        
    else:
        print("\n❌ 获取数据失败")
        # 发送失败通知
        send_telegram_message("❌ 黄金价格获取失败，请检查日志")
