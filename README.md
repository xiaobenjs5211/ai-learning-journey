# ai-learning-journey

> 徐成俊的 AI 学习记录 · 阶段 0（2026.10.15 - 2027.01.13）
> 这一栏以后要填进简历，所以从第一天就按「给别人看」的标准写。

## 这是什么

我在自学 AI 开发，这是阶段 0 的练习仓库。
阶段 0 的目标不是学多深，而是把「学过语法」变成「手里有一个能跑的 AI 应用，并且它挂在 GitHub 上」。

## 目前有什么

| 文件 | 作用 |
|---|---|
| `hello_ai.py` | 第一个能跑的脚本：向大模型发一句话并拿到回复 |
| `explore_params.py` | 参数实验：拆解 `messages` 角色结构、`temperature`、`max_tokens` |
| `.env.example` | 密钥模板（真实密钥放在 `.env`，不进版本库） |
| `requirements.txt` | 依赖清单 |

## 怎么运行

**1. 拿到一个 API Key**

去 [智谱开放平台](https://open.bigmodel.cn) 手机号注册 → 实名认证 → 控制台创建 API Key。
`glm-4-flash` 是免费模型，练手不花钱。

**2. 克隆并进入项目**

```bash
git clone https://github.com/<你的用户名>/ai-learning-journey.git
cd ai-learning-journey
```

**3. 创建虚拟环境并激活**

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# Mac / Linux
source .venv/bin/activate
```

**4. 安装依赖**

```bash
pip install -r requirements.txt
```

**5. 配置密钥**

```bash
# Windows
copy .env.example .env
# Mac / Linux
cp .env.example .env
```

然后打开 `.env`，把 `ZHIPU_API_KEY` 换成你自己的 Key。

**6. 运行**

```bash
python hello_ai.py
```

看到模型回复的那句话，就说明整个链路通了。

## 我踩过的坑

<!-- Day 7 的作业：把这周卡住你的地方记在这里，这些以后就是你技术文章的素材 -->

1. **`ModuleNotFoundError: No module named 'sniffio'`**
   `zhipuai` 2.1.5 内部 `import sniffio`，但没把它写进自己的依赖声明。
   解决办法：`pip install sniffio`（已写进 `requirements.txt`）。

2. _（待补：你自己踩的坑）_

## 下一步

第 2 周开始补 Python 工程能力（函数 / 文件读写 / 类与对象 / 异常处理），
目标是能用 `ChatSession` 类管理多轮对话历史。

---

**技术栈**：Python 3.14 · zhipuai SDK · python-dotenv · Git
