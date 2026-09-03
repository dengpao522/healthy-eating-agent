import json

d = {
    "name":"zhaojianhui",
    "age":21,
    "gender":"man"
}

j = json.dumps(d,ensure_ascii = False)
print(j)

json_str = '{"name": "zhaojianhui", "age": 21, "gender": "man"}'

res_dict = json.loads(json_str)
print(res_dict)
