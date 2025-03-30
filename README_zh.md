# 显示器亮度调度器

[English](README.md) | 中文

这是一个基于Python的调度器，可以根据一天中的时间自动调整外接显示器的亮度。该工具专为通过HDMI线缆连接到M1芯片MacBook的HP M24f FHD显示器配置，使用Lunar的命令行界面。

## 系统要求

- macOS 11+（Big Sur或更新版本）
- 搭载M1芯片的MacBook
- 通过HDMI连接的HP M24f FHD显示器
- Python 3.8+
- [Lunar应用](https://lunar.fyi/)（免费版即可）

## 安装

1. 克隆此仓库：
   ```
   git clone https://github.com/tylerxiety/monitor_brightness_scheduler.git
   cd monitor_brightness_scheduler
   ```

2. 如果尚未安装Lunar应用：
   ```
   brew install --cask lunar
   ```

3. 设置Python虚拟环境：
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

4. 安装所需依赖：
   ```
   pip install -r requirements.txt
   ```

## 配置

亮度调度计划在`config/brightness_schedule.yaml`中定义，并已针对HP M24f FHD显示器预先配置了最佳设置。您可以根据需要自定义此计划：

```yaml
schedule:
  - time: "05:00"  # 24小时制时间格式（HH:MM）
    brightness: 30  # 亮度百分比（0-100）
  
  - time: "09:00" 
    brightness: 65
  
  # 更多条目...
```

## 使用方法

### 检查显示器信息

要检查您的HP M24f FHD显示器是否被正确识别：

```
chmod +x test_monitor_info.sh
./test_monitor_info.sh
```

这将显示已连接显示器的信息及其当前设置。

### 测试亮度控制

要测试是否可以控制显示器亮度：

```
python src/monitor_brightness_control.py test 50  # 测试将亮度设置为50%
```

### 手动控制

启动、停止和检查调度器状态：

```
# 启动调度器
python main.py start

# 检查状态
python main.py status

# 停止调度器
python main.py stop

# 测试将亮度设置为50%
python src/monitor_brightness_control.py test 50
```

### 自动启动

要配置调度器在登录时自动启动：

```
chmod +x install_startup.sh
./install_startup.sh
```

这将安装一个LaunchAgent，使调度器在您登录Mac时启动。

## 工作原理

1. 调度器从配置文件中读取亮度计划
2. 根据当前时间确定适当的亮度级别
3. 使用Lunar的命令行界面调整HP显示器的亮度
4. 调度器自动处理显示器的断开和重新连接
5. 仅在需要更改亮度时才进行调整，以减少不必要的更新

## 项目结构

```
monitor_brightness_scheduler/
├── config/                   # 配置文件
│   └── brightness_schedule.yaml  # 调度配置
├── src/                      # 源代码
│   ├── __init__.py           # 包初始化
│   ├── lunar_applescript.scpt # 用于Lunar集成的AppleScript
│   ├── lunar_brightness.py   # Lunar亮度控制模块
│   ├── monitor_brightness_control.py  # 控制调度器的命令行接口
│   └── monitor_brightness_scheduler.py # 主调度器实现
├── main.py                   # 入口点脚本
├── install_startup.sh        # 安装LaunchAgent的脚本
├── start_monitor_brightness.sh # 自动启动脚本
├── requirements.txt          # Python依赖
└── README.md                 # 文档
```

## 故障排除

- 如果Lunar无法识别您的HP M24f FHD显示器，请打开Lunar应用并检查它是否出现在显示器列表中
- 对于使用HDMI连接的M1 MacBook，请确保使用高质量的HDMI线缆
- 检查`scheduler.log`中的任何错误信息
- 如果调度器未启动，请验证Lunar应用是否正在运行
- 如果`test_monitor_info.sh`不存在，请在终端中运行`lunar list`以检查已连接的显示器

## 许可证

MIT 