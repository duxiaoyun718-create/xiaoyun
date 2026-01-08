# your_ai_module.py
from dataset_ai import dataset_ai

class YourAIClient:
    """基于数据集的AI客户端"""
    
    def __init__(self):
        self.client = dataset_ai
        print("✅ 基于数据集的AI客户端已加载")
    
    def simple_chat(self, message):
        """简单聊天"""
        return self.client.answer(message)
    
    def chat(self, data):
        """适配原有接口"""
        message = data.get("message", "")
        return self.client.answer(message)
    
    def recommend_resources(self, user_data):
        """推荐资源"""
        return {
            "recommendations": [
                {
                    "title": "Python Crash Course",
                    "description": "No Starch Press畅销书，已售出100万+册",
                    "url": "https://ehmatthes.github.io/pcc_3e/",
                    "type": "免费电子书",
                    "reason": "适合初学者，评分4.8/5.0"
                },
                {
                    "title": "freeCodeCamp Python课程",
                    "description": "250万+学员认证，300小时系统课程",
                    "url": "https://www.freecodecamp.org/learn/scientific-computing-with-python/",
                    "type": "免费在线课程",
                    "reason": "项目驱动，提供认证"
                }
            ]
        }
    
    def analyze_learning(self, user_data):
        """学习分析"""
        completion_rate = user_data.get('completion_rate', 0)
        
        if completion_rate >= 80:
            efficiency = "优秀"
            score = 90
            suggestions = ["保持当前节奏", "挑战更高难度", "参与开源项目"]
        elif completion_rate >= 60:
            efficiency = "良好"
            score = 75
            suggestions = ["优化时间安排", "增加项目实践", "系统复习"]
        elif completion_rate >= 40:
            efficiency = "一般"
            score = 60
            suggestions = ["制定详细计划", "减少分心因素", "寻求帮助"]
        else:
            efficiency = "待提升"
            score = 45
            suggestions = ["设定小目标", "建立学习习惯", "找到学习动力"]
        
        return {
            "efficiency": efficiency,
            "characteristics": "基于数据集分析",
            "suggestions": suggestions,
            "predicted_score": score,
            "encouragement": "坚持学习，每天进步一点点！"
        }

# 创建客户端实例
your_ai_client = YourAIClient()