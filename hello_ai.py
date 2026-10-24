"""
第 1 周 · Day 3 —— 跑通你的第一次 API 调用
============================================
这是阶段 0 的第一个真正能跑的脚本。
运行方式（在项目根目录、虚拟环境已激活的情况下）：
    python hello_ai.py

注意：先把你的智谱 API Key 填进同目录下的 .env 文件里。
"""

import os

from dotenv import load_dotenv
from zhipuai import ZhipuAI

# 1) 读取同目录下的 .env 文件，把里面的键值对加载进环境变量
#    .env 长这样： ZHIPU_API_KEY=你的key
load_dotenv()

# 2) 从环境变量里取 Key —— 绝对不要写死在代码里，那等于把钥匙插在门上
api_key = os.getenv("c815e03c453946399537dbd245ec47f4.40VlD4mApqAQZ7gu")

# 3) 提前检查，给出人话版报错，而不是让它跑到一半崩掉
if not api_key or api_key == "c815e03c453946399537dbd245ec47f4.40VlD4mApqAQZ7gu":
    raise SystemExit(
        "❌ 没有读到 ZHIPU_API_KEY。\n"
        "   请打开项目根目录的 .env 文件，把 ZHIPU_API_KEY= 后面换成你的真实 Key。"
    )

# 4) 创建客户端。之后所有请求都通过它发出
client = ZhipuAI(api_key=api_key)

# 用哪个模型？glm-4-flash 是智谱的免费模型，练手足够，不花钱
MODEL = "glm-4-flash"


def ask(question):
    """把一个问题发给模型，返回它的回答（字符串）。

    messages 是一个「角色列表」：
      - system    给模型设定身份和规则（可有可无）
      - user      你说的话
      - assistant 模型说过的话
    这是后面所有 Agent / 多轮对话的地基，Day 4 会重点拆它。
    """
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": question}],
        )
        return resp.choices[0].message.content
    except Exception as e:
        # 网络抖动、Key 错了、额度用完了，都会走到这里
        # 不写 try/except 的话，程序会直接崩一串红色报错，很难看懂
        return f"调用失败：{e}"


if __name__ == "__main__":
    answer = ask("用一句话解释什么是工业工程")
    print(answer)
