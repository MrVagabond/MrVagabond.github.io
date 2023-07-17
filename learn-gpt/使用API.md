详情见openai官方文档

以Python为例，说明如何使用GPT的API

## 本质
调用API，其实就是发起一个网络请求

```
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "SOME THING"}],
    "temperature": 0.7
  }'
```
返回的响应类似于下面这种
```json
{
  "id":"",
  "object": "",
  "created": xxx,
  "model": "gpt-3.5-turbo-0301",
  "usage": {
    "prompt_tokens": xx,
    "completion_tokens: xx,
    "total_tokens": xx
  },
  "choices": [
    {
      "message": {
        "role": xx,
        "content": ""
      },
      "finish_reason": "stop",
      "index": 0
    }
  ]
}
```

无论是直接使用Python内置的网络工具还是使用openai的封装，都是在做这个事情

