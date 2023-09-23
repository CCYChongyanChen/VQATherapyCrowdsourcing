import json
import json

with open('train_grouped.json') as f:
  data = json.load(f)

print(len(data))