<div align="center">

# 🧠 ChatKG - Knowledge Graph-based LLM Dialog System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-1.11+-ee4c2c.svg?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![PaddlePaddle](https://img.shields.io/badge/PaddlePaddle-2.4+-2b6cb0.svg)](https://www.paddlepaddle.org.cn/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D.svg?logo=vue.js&logoColor=white)](https://vuejs.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**基于知识图谱和知识库的大模型对话系统**

*Combining Knowledge Graph Construction, Graph Completion, and ChatGLM for Intelligent Q&A*

[功能特点](#-功能特点) • [快速开始](#-快速开始) • [系统架构](#-系统架构) • [使用指南](#-使用指南) • [配置说明](#-配置说明)

</div>

---

## 📺 Demo 展示

<div align="center">

https://github.com/littlewwwhite/KnowledgeGraph-based-on-Raw-text-A27/assets/34784086/aa089b51-0b88-4d2b-b7fe-d892c503e55c

</div>

<table>
<tr>
<td width="50%">

### 💬 智能对话界面
![对话演示](demo/demo-chat.png)

</td>
<td width="50%">

### 🔗 知识图谱可视化
![图谱演示](demo/demo-kg.png)

</td>
</tr>
</table>

---

## ✨ 功能特点

<table>
<tr>
<td>

### 🎯 核心功能

- **智能问答** - 基于 ChatGLM-6B 的多轮对话
- **知识检索** - 结合知识图谱的精准信息检索
- **图谱可视化** - 交互式知识图谱展示
- **实体关联** - 自动展示相关实体和上下文

</td>
<td>

### 🛠️ 技术特性

- **UIE 抽取** - PaddleNLP 通用信息抽取
- **SPN4RE** - 关系三元组联合抽取模型
- **图谱补全** - 迭代式知识图谱扩展
- **流式输出** - 实时响应的对话体验

</td>
</tr>
</table>

---

## 🏗️ 系统架构

### 整体流程

项目包含 **5 个核心模块**：数据预处理 → 图谱构建 → 图谱补全 → 对话模型 → 网页呈现

![整体流程](demo/all.png)

<details>
<summary><b>📊 点击展开各模块详细说明</b></summary>

### 1️⃣ 数据预处理

将原始文本数据进行清洗、分句、标准化处理，为后续的信息抽取做准备。

![数据预处理环节](demo/data_process.png)

### 2️⃣ 种子图谱构建

利用 PaddleNLP UIE 模型和 ChatGPT 定义的关系 Schema 构建初始知识图谱。

![图谱构建](demo/build_kg.png)

### 3️⃣ 图谱补全迭代

通过 SPN4RE 模型对种子图谱进行迭代补全，逐步扩展知识覆盖范围。

![图谱补全](demo/kg.png)

### 4️⃣ 对话服务

基于 ChatGLM-6B 构建问答服务，结合知识图谱实现精准检索与智能回答。

![对话模型](demo/chat.png)

### 5️⃣ 前端界面

使用 Vue 3 + ECharts 构建现代化的交互界面，支持对话与图谱可视化。

![前端](demo/web.png)

</details>

---

## 🚀 快速开始

### 环境要求

| 组件 | 版本要求 | 说明 |
|------|---------|------|
| Python | 3.8+ | 推荐 3.8.16 |
| PyTorch | 1.10+ | 需支持 CUDA |
| PaddlePaddle | 2.4+ | GPU 版本 |
| Node.js | 16+ | 前端构建 |
| GPU | NVIDIA 3090 | 推荐双卡 |

### 1. 克隆项目

```bash
git clone https://github.com/littlewwwhite/KnowledgeGraph-based-on-Raw-text-A27.git
cd KnowledgeGraph-based-on-Raw-text-A27
```

### 2. 安装后端依赖

```bash
# 创建虚拟环境 (推荐使用 uv)
uv venv --python 3.8
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 安装 GPU 版本 PyTorch (根据 CUDA 版本选择)
pip install torch==1.11.0+cu113 -f https://download.pytorch.org/whl/torch_stable.html

# 安装 GPU 版本 PaddlePaddle
pip install paddlepaddle-gpu==2.4.2.post112 -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html
```

### 3. 配置环境变量

```bash
# 复制配置模板
cp .env.example .env

# 编辑配置 (至少设置以下项)
vim .env
```

关键配置项：

```bash
# 模型路径 (本地路径或 HuggingFace 模型名)
CHATGLM_MODEL_PATH=THUDM/chatglm-6b

# GPU 配置
CUDA_VISIBLE_DEVICES=0,1

# 服务端口
SERVER_PORT=8000
```

### 4. 构建知识图谱

```bash
# 运行知识图谱构建流程
python main.py --project my_project --gpu 0

# 从检查点恢复
python main.py --project my_project --resume checkpoint_v3 --gpu 0
```

### 5. 启动后端服务

```bash
cd server
python main.py
# 服务将启动在 http://localhost:8000
```

### 6. 启动前端界面

```bash
cd chat-kg

# 安装依赖
npm install

# 开发模式
npm run dev
# 访问 http://localhost:5173

# 生产构建
npm run build
```

---

## 📖 使用指南

### 知识图谱构建流程

```mermaid
graph LR
    A[原始文本] --> B[数据预处理]
    B --> C[UIE 信息抽取]
    C --> D[种子图谱]
    D --> E[SPN4RE 训练]
    E --> F[图谱补全]
    F --> G{扩展率检查}
    G -->|> 阈值| E
    G -->|< 阈值| H[最终图谱]
```

### 命令行参数

```bash
python main.py [OPTIONS]

Options:
  --project TEXT    项目名称，用于数据隔离 (default: project_v1)
  --resume TEXT     从指定检查点恢复训练
  --gpu TEXT        使用的 GPU ID (default: 0)
```

### API 接口

| 端点 | 方法 | 描述 |
|------|------|------|
| `/chat` | POST | 发送对话请求 |
| `/graph` | GET | 获取知识图谱数据 |
| `/entity/<name>` | GET | 查询实体信息 |

**对话请求示例：**

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "什么是损管技术?", "history": []}'
```

---

## ⚙️ 配置说明

### 环境变量完整列表

<details>
<summary><b>📋 点击展开完整配置项</b></summary>

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| **路径配置** | | |
| `DATA_DIR` | `./data` | 数据目录 |
| `RAW_DATA_PATH` | `./data/raw_data/raw_data.txt` | 原始数据文件 |
| **模型配置** | | |
| `CHATGLM_MODEL_PATH` | `THUDM/chatglm-6b` | ChatGLM 模型路径 |
| `BERT_MODEL_NAME` | `bert-base-chinese` | BERT 模型名称 |
| `UIE_MODEL_NAME` | `uie-base` | UIE 模型名称 |
| **训练配置** | | |
| `TRAIN_RATIO` | `0.5` | 训练集比例 |
| `VALID_RATIO` | `0.2` | 验证集比例 |
| `MAX_EPOCH` | `10` | 最大训练轮数 |
| `BATCH_SIZE` | `8` | 批次大小 |
| `MAX_ITERATION` | `10` | 图谱扩展最大迭代次数 |
| `EXTEND_RATIO_THRESHOLD` | `0.01` | 扩展率阈值 |
| **GPU 配置** | | |
| `CUDA_VISIBLE_DEVICES` | `0` | 可见 GPU 设备 |
| `DEFAULT_GPU` | `0` | 默认 GPU |
| **服务配置** | | |
| `SERVER_HOST` | `0.0.0.0` | 服务监听地址 |
| `SERVER_PORT` | `8000` | 服务端口 |
| `SECRET_KEY` | 随机生成 | Flask 密钥 (生产环境必须设置) |
| `DEBUG` | `false` | 调试模式 |

</details>

### Schema 配置

系统支持多版本关系 Schema，在 `data/schema/` 目录下定义：

```python
# data/schema/schema_v4.py
schema = {
    "实体类型": ["设备", "人员", "技术", "方法", "材料"],
    "关系类型": {
        "设备": ["组成部分", "功能", "位置"],
        "技术": ["应用于", "依赖", "包含"],
        # ...
    }
}
```

---

## 📁 项目结构

```
KnowledgeGraph-based-on-Raw-text-A27/
├── 📂 chat-kg/               # Vue 3 前端项目
│   ├── src/
│   │   ├── components/       # 组件 (MessageList, InfoPanel, etc.)
│   │   ├── views/            # 页面视图
│   │   └── assets/           # 样式和资源
│   └── package.json
├── 📂 config/                # 配置管理
│   └── settings.py           # 集中式配置
├── 📂 data/                  # 数据目录
│   ├── raw_data/             # 原始文本数据
│   ├── schema/               # 关系 Schema 定义
│   └── project_*/            # 项目数据 (自动生成)
├── 📂 modules/               # 核心模块
│   ├── knowledge_graph_builder.py  # 图谱构建器
│   ├── model_trainer.py      # SPN4RE 训练器
│   ├── prepare/              # 数据预处理
│   └── utils/                # 工具函数
├── 📂 server/                # Flask 后端
│   ├── main.py               # 服务入口
│   └── chat_glm.py           # ChatGLM 封装
├── 📂 tests/                 # 测试用例
├── 📜 main.py                # 主入口
├── 📜 requirements.txt       # Python 依赖
└── 📜 .env.example           # 环境变量模板
```

---

## 🔧 技术栈

<table>
<tr>
<th>后端</th>
<th>前端</th>
<th>AI/ML</th>
</tr>
<tr>
<td>

- Python 3.8+
- Flask
- Flask-CORS

</td>
<td>

- Vue 3 (Composition API)
- Vite
- ECharts
- Ant Design Vue

</td>
<td>

- PyTorch
- PaddleNLP (UIE)
- Transformers
- ChatGLM-6B
- SPN4RE

</td>
</tr>
</table>

---

## 📊 数据来源与标注

### 数据来源

| 数据集 | 描述 |
|--------|------|
| 《舰艇损管和潜水技术》 | 初始核心数据 |
| 《舰船损管技术》 | 扩充数据集 |

### 数据标注流程

1. **初始标注** - 使用 [Doccano](https://github.com/doccano/doccano) 标注约 100 条样本
2. **UIE 抽取** - 利用标注数据微调 UIE 模型进行初次抽取
3. **二次标注** - 针对抽取效果较差的部分进行修正和补充标注
4. **迭代优化** - 重复上述流程直至抽取质量满足要求

---

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行特定模块测试
pytest tests/test_config.py -v

# 查看测试覆盖率
pytest --cov=modules tests/
```

---

## 📝 开发指南

### 添加新的关系 Schema

1. 在 `data/schema/` 创建新的 schema 文件 (如 `schema_v5.py`)
2. 定义实体类型和关系类型
3. 在 `.env` 中设置 `SCHEMA_VERSION=v5`

### 前端开发

```bash
cd chat-kg
npm run dev       # 开发服务器
npm run build     # 生产构建
npm run lint      # 代码检查
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 License

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个 Star！**

Made with ❤️ by [littlewwwhite](https://github.com/littlewwwhite)

</div>
