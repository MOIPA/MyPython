from aip import AipNlp
import json

APP_ID = '16685157'

API_KEY = '0PQt2RjUAtNYZr8KA7cIWKue'
SECRET_KEY = 'RnKHaVAM0gkV6kk6G12nPhTe2ny8QQah'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

text = "今天天气很好，但是我的心情很差"

out = client.sentimentClassify(text)
out = out.get('items')[0]

positive_posibility = out.get('positive_prob')
confidence  = out.get('confidence')
negative_posibility = out.get('negative_prob')
sentimentValue = out.get('sentiment')

print((positive_posibility,confidence))
