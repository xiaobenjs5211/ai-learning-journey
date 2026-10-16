"""
第 1 周 · Day 4 —— 拆开参数，搞懂你到底在调什么
================================================
运行：python explore_params.py

这一天不写新功能，只做实验。目的只有一个：
把 messages 这个「角色列表」刻进脑子里 —— 后面所有 Agent 都建在它上面。
"""

import os

from dotenv import load_dotenv
from zhipuai import ZhipuAI

load_dotenv()
client = ZhipuAI(api_key=os.getenv("ZHIPU_API_KEY"))
MODEL = "glm-4-flash"


def chat(messages, **kwargs):
    """统一入口：传入角色列表，返回 (回答文本, token用量)。"""
    resp = client.chat.completions.create(model=MODEL, messages=messages, **kwargs)
    text = resp.choices[0].message.content
    usage = getattr(resp, "usage", None)
    tokens = getattr(usage, "total_tokens", "未知") if usage else "未知"
    return text, tokens


def title(t):
    print("\n" + "=" * 64)
    print(t)
    print("=" * 64)


# ---------------------------------------------------------------
title("实验 1：messages 是「角色列表」，不是一段字符串")
# ---------------------------------------------------------------
# 同一个人提问，加不加 system，回答的口吻完全不同。
# system 就是给模型「立人设、定规则」的地方。
question = "解释一下什么是流水线平衡"

no_system, _ = chat([{"role": "user", "content": question}])
print("\n【只有 user】")
print(no_system)

with_system, _ = chat(
    [
        {"role": "system", "content": "你是一位工业工程专业的教授，回答专业、简洁，不超过 60 字。"},
        {"role": "user", "content": question},
    ]
)
print("\n【system + user】")
print(with_system)
print("\n→ 观察：内容受同一个知识库限制，但口吻、长度被你用 system 控制住了。")


# ---------------------------------------------------------------
title("实验 2：assistant 角色 —— 模型也可以「说过话」")
# ---------------------------------------------------------------
# 把模型之前的回复以 assistant 身份塞回列表，它就能「记住」上下文。
# 这就是多轮对话的全部秘密：历史消息不断 append 进这个列表。
history = [
    {"role": "system", "content": "你是一位简洁的助手。"},
    {"role": "user", "content": "我叫徐成俊，在南京农业大学读工业工程。"},
]
reply1, _ = chat(history)
print(f"\n第 1 轮提问：我叫徐成俊，在南京农业大学读工业工程。")
print(f"模型回复：{reply1}")

history.append({"role": "assistant", "content": reply1})       # 把模型的回答记下来
history.append({"role": "user", "content": "我叫什么？读什么专业？"})  # 再问

reply2, _ = chat(history)
print(f"\n第 2 轮提问：我叫什么？读什么专业？")
print(f"模型回复：{reply2}")
print("\n→ 把 history.append(...) 这两行删掉再跑一次，它会答不上来。")
print("  这个对比，就是「上下文」这个词的全部含义。")


# ---------------------------------------------------------------
title("实验 3：temperature —— 同一句话，每次答案都不一样")
# ---------------------------------------------------------------
# temperature 越低越确定、越保守；越高越发散、越有创意。
# 写代码、做数据处理用低值；写文案、头脑风暴用高值。
prompt = [{"role": "user", "content": "给一个工业工程相关的创业点子，一句话。"}]
for temp in (0.01, 1.5):
    print(f"\n【temperature = {temp}】")
    for i in range(2):  # 同一个参数连问两次，看稳定性
        text, _ = chat(prompt, temperature=temp)
        print(f"  第 {i + 1} 次：{text}")


# ---------------------------------------------------------------
title("实验 4：max_tokens —— 给回答长度设个上限")
# ---------------------------------------------------------------
prompt = [{"role": "user", "content": "讲讲工业工程的发展历史。"}]
for mt in (30, 500):
    text, tokens = chat(prompt, max_tokens=mt)
    print(f"\n【max_tokens = {mt}】实际用量 {tokens} tokens")
    print(text[:200] + ("..." if len(text) > 200 else ""))
print("\n→ max_tokens 是「输出上限」，卡太狠会话说一半就断掉。")


# ---------------------------------------------------------------
title("实验 5：看一眼 token 用量 —— 你花钱花在哪")
# ---------------------------------------------------------------
text, tokens = chat([{"role": "user", "content": "用一句话解释什么是工业工程"}])
print(f"\n回答：{text}")
print(f"本次总 token 用量：{tokens}")
print("\n→ 记住这个感觉：上下文越长，token 越多，越贵越慢。")
print("  第 3 周的「上下文管理」就是在解决这件事。")

print("\n✅ Day 4 结束。如果实验 2 的对比让你「哦——」了一下，今天就值了。")
