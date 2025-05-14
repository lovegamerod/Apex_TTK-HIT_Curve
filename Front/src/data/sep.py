import json

# 读取原始 JSON 文件
with open('json-data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 构建 id -> name 映射
id_to_name = {item['id']: item['weapon_name'] for item in data}

# 构建 id -> stats 映射
id_to_stats = {item['id']: item['stats'] for item in data}

# 将结果写入新的 JSON 文件
with open('id_name.json', 'w', encoding='utf-8') as f:
    json.dump(id_to_name, f, ensure_ascii=False, indent=2)

with open('id_stats.json', 'w', encoding='utf-8') as f:
    json.dump(id_to_stats, f, ensure_ascii=False, indent=2)

print("已生成 id_name.json 和 id_stats.json。")
