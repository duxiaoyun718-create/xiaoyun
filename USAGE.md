# 使用教程 / Usage Tutorial

## 📖 关于本教程 / About This Tutorial

因为每个人的房间（学习环境）不一样，本教程将帮助您根据自己的需求定制和使用小云（XiaoYun）AI学习管理平台。

Since everyone's room (learning environment) is different, this tutorial will help you customize and use the XiaoYun AI-powered learning management platform according to your needs.

---

## 🏠 什么是"房间"？/ What is a "Room"?

在小云平台中，"房间"代表您的个性化学习环境，包括：
- 课程设置和安排
- 学习风格偏好
- AI助手配置
- 学习资源组织方式

In the XiaoYun platform, a "room" represents your personalized learning environment, including:
- Course settings and schedules
- Learning style preferences
- AI assistant configuration
- Learning resource organization

---

## 🚀 快速开始 / Quick Start

### 第一步：环境准备 / Step 1: Environment Setup

1. **克隆项目 / Clone the project**
   ```bash
   git clone https://github.com/duxiaoyun718-create/xiaoyun.git
   cd xiaoyun
   ```

2. **安装依赖 / Install dependencies**
   ```bash
   # 根据您的项目技术栈选择
   # Choose based on your project stack
   npm install    # For Node.js projects
   # or
   pip install -r requirements.txt  # For Python projects
   ```

### 第二步：配置您的房间 / Step 2: Configure Your Room

创建配置文件 `config/room.json`：

Create configuration file `config/room.json`:

```json
{
  "roomId": "your-unique-room-id",
  "roomName": "我的学习空间",
  "preferences": {
    "language": "zh-CN",
    "theme": "light",
    "aiAssistant": {
      "enabled": true,
      "model": "gpt-4",
      "personality": "encouraging"
    }
  },
  "courses": []
}
```

---

## 🎨 房间类型示例 / Room Type Examples

### 类型1：个人学习房间 / Type 1: Personal Learning Room

适合个人自学的配置：

Configuration for individual self-study:

```json
{
  "roomId": "personal-001",
  "roomName": "个人学习空间",
  "type": "personal",
  "preferences": {
    "studyMode": "self-paced",
    "reminderEnabled": true,
    "focusMode": true
  }
}
```

**特点 / Features:**
- ✅ 自定义学习进度
- ✅ 个性化提醒
- ✅ 专注模式
- ✅ AI学习助手

### 类型2：小组协作房间 / Type 2: Group Collaboration Room

适合小组学习和协作：

Configuration for group study and collaboration:

```json
{
  "roomId": "group-001",
  "roomName": "团队学习空间",
  "type": "group",
  "preferences": {
    "maxMembers": 10,
    "collaborationEnabled": true,
    "sharedResources": true,
    "videoConference": true
  }
}
```

**特点 / Features:**
- ✅ 多人协作
- ✅ 共享资源
- ✅ 视频会议集成
- ✅ 小组讨论板

### 类型3：在线课堂房间 / Type 3: Online Classroom Room

适合教师进行在线教学：

Configuration for teachers conducting online classes:

```json
{
  "roomId": "classroom-001",
  "roomName": "在线课堂",
  "type": "classroom",
  "preferences": {
    "teacherMode": true,
    "liveStreamEnabled": true,
    "attendanceTracking": true,
    "assignmentManagement": true
  }
}
```

**特点 / Features:**
- ✅ 教师控制面板
- ✅ 直播教学
- ✅ 考勤管理
- ✅ 作业布置与批改

---

## ⚙️ 高级配置 / Advanced Configuration

### AI助手个性化 / AI Assistant Personalization

根据您的学习风格配置AI助手：

Configure AI assistant based on your learning style:

```json
{
  "aiAssistant": {
    "personality": "encouraging",  // 鼓励型 / encouraging | 严格型 strict | 友好型 friendly
    "responseStyle": "detailed",   // 详细 detailed | 简洁 concise
    "languageLevel": "intermediate", // 初级 beginner | 中级 intermediate | 高级 advanced
    "specialization": ["math", "programming"]  // 专长领域
  }
}
```

### 学习资源管理 / Learning Resource Management

组织您的学习材料：

Organize your learning materials:

```json
{
  "resources": {
    "storage": "cloud",  // cloud | local
    "autoSync": true,
    "categories": [
      "视频课程 / Video Courses",
      "文档资料 / Documents",
      "练习题库 / Exercise Bank",
      "项目案例 / Project Cases"
    ]
  }
}
```

---

## 🔧 常见配置场景 / Common Configuration Scenarios

### 场景1：考试准备模式 / Scenario 1: Exam Preparation Mode

```json
{
  "mode": "exam-prep",
  "settings": {
    "quizFrequency": "daily",
    "progressTracking": true,
    "weaknessAnalysis": true,
    "practiceSessions": {
      "duration": 45,
      "breakTime": 15
    }
  }
}
```

### 场景2：项目学习模式 / Scenario 2: Project-Based Learning Mode

```json
{
  "mode": "project-based",
  "settings": {
    "projectTracking": true,
    "milestones": true,
    "codeReview": true,
    "mentorSupport": true
  }
}
```

### 场景3：快速复习模式 / Scenario 3: Quick Review Mode

```json
{
  "mode": "quick-review",
  "settings": {
    "flashcardsEnabled": true,
    "summaryGeneration": true,
    "timeBoxed": true,
    "duration": 30
  }
}
```

---

## 📱 多设备同步 / Multi-Device Synchronization

在不同设备间同步您的房间设置：

Sync your room settings across devices:

1. **启用云同步 / Enable Cloud Sync**
   ```bash
   xiaoyun sync --enable
   ```

2. **登录账号 / Login to Account**
   ```bash
   xiaoyun login --username your_username
   ```

3. **同步设置 / Sync Settings**
   ```bash
   xiaoyun sync --pull  # 拉取配置 / Pull configuration
   xiaoyun sync --push  # 推送配置 / Push configuration
   ```

---

## 🛠️ 故障排除 / Troubleshooting

### 问题1：房间配置未生效 / Issue 1: Room Configuration Not Applied

**解决方案 / Solution:**
1. 检查配置文件格式是否正确 / Check configuration file format
2. 重启应用 / Restart application
3. 清除缓存：`xiaoyun cache --clear`

### 问题2：AI助手无响应 / Issue 2: AI Assistant Not Responding

**解决方案 / Solution:**
1. 检查网络连接 / Check network connection
2. 验证API密钥：`xiaoyun check --api-key`
3. 查看日志：`xiaoyun logs --tail 100`

### 问题3：资源同步失败 / Issue 3: Resource Sync Failed

**解决方案 / Solution:**
1. 检查存储空间 / Check storage space
2. 验证网络连接 / Verify network connection
3. 手动重试：`xiaoyun sync --retry`

---

## 📚 更多资源 / Additional Resources

- **官方文档 / Official Documentation**: [待添加 / To be added]
- **视频教程 / Video Tutorials**: [待添加 / To be added]
- **社区论坛 / Community Forum**: [待添加 / To be added]
- **常见问题 / FAQ**: [待添加 / To be added]

---

## 💡 最佳实践 / Best Practices

1. **定期备份配置 / Regular Configuration Backup**
   ```bash
   xiaoyun backup --config
   ```

2. **使用版本控制 / Use Version Control**
   - 将配置文件加入版本控制系统
   - Keep configuration files in version control

3. **测试新配置 / Test New Configurations**
   - 在测试环境中先验证配置
   - Validate configurations in test environment first

4. **文档化定制化设置 / Document Customizations**
   - 记录您的特殊配置和原因
   - Document your special configurations and reasons

---

## 🤝 获取帮助 / Getting Help

如果您在配置房间时遇到问题，请：

If you encounter issues while configuring your room:

1. 查看本教程的相关章节 / Check relevant sections of this tutorial
2. 搜索常见问题 / Search FAQs
3. 在GitHub Issues中提问 / Ask in GitHub Issues
4. 联系技术支持 / Contact technical support

---

## 📝 贡献指南 / Contributing

欢迎改进本教程！请通过Pull Request提交您的建议。

Contributions to improve this tutorial are welcome! Please submit your suggestions via Pull Request.

---

**最后更新 / Last Updated**: 2026-01-08
**版本 / Version**: 1.0.0
