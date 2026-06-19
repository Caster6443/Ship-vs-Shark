# 飞船大战太空鲨 (Ship vs Shark) 🚀🦈

一个基于 《Python编程：从入门到实践》（*Python Crash Course*）经典项目“外星人入侵”（*Alien Invasion*）进行二次开发与魔改的 Python 射击游戏。

Spaceship vs. Space Sharks — A modified game based on the "Alien Invasion" project from *Python Crash Course*.

---

## 🛠️ 已知问题与环境配置 (Known Issues & Workaround)

**关于 Python 3.14+ 的运行报错问题：**
本项目代码完全遵循标准语法。但由于 `Pygame 2.6.1` 在 `Python 3.14` 下存在内部引用的兼容性 Bug（`font.py` 和 `sysfont.py` 会形成死锁导致启动崩溃）。如果你使用 Python 3.14 运行此游戏，可能会遇到启动失败。

### 💡 解决方案（二选一）

1. **使用兼容的 Python 版本**：建议使用 Python 3.12 或 3.13 创建虚拟环境来运行本游戏，可完美避开此 Bug。
2. **手动给 Pygame 源码打补丁**：如果你必须在 Python 3.14 环境下运行，请打开你本地虚拟环境中的 `venv/lib/python3.14/site-packages/pygame/sysfont.py`：
   * **删除**第 27 行的 `from pygame.font import Font`
   * **移至**第 378 行的 `font_constructor` 函数内部，加上 `from pygame.font import Font` 进行延迟导入，即可正常启动游戏。

---

## 🚀 如何在本地运行 (How to Run)

1. 克隆本项目到本地：

   ```bash
   git clone [https://github.com/Caster6443/Ship-vs-Shark.git](https://github.com/Caster6443/Ship-vs-Shark.git)
   cd Ship-vs-Shark
   ```

2. 创建并激活虚拟环境:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Fish shell 请使用 source venv/bin/activate.fish
   ```

3. 安装依赖并启动游戏：

   ```bash
   pip install -r requirements.txt
   python shark_invasion.py
   ```

---
