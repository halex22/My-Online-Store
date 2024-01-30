import json

test_dict = { 1: {'product': 'test_product', 'price': 45, 'quantity': 2}}
test_dict.update({2: {'product': 'test_product_two', 'price': 40, 'quantity': 1}})
test_json = json.loads(json.dumps(test_dict))
print(test_json)