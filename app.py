# app.py 完整修改版
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import random
import os
import threading
import time
import json

# 创建Flask应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'campus-pulse-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campus.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 从 models.py 导入所有模型
from models import db, User, Task, MoodLog, LearningResource, ChatMessage, StudySession

# 初始化数据库
db.init_app(app)

# 初始化登录管理
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '请先登录以访问此页面。'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 导入爬虫模块
try:
    from simple_crawler import simple_crawler
    print("✅ 简单爬虫导入成功")
except ImportError as e:
    print(f"⚠️  爬虫导入警告: {e}")
    simple_crawler = None

# ========== AI集成 ==========
# 导入智谱AI客户端
try:
    from your_ai_module import your_ai_client
    
    if your_ai_client:
        print("✅ 智谱AI客户端初始化成功")
    else:
        print("⚠️  智谱AI客户端初始化失败")
        your_ai_client = None
except ImportError as e:
    print(f"⚠️  AI模块导入失败: {e}")
    your_ai_client = None
except Exception as e:
    print(f"⚠️  AI初始化失败: {e}")
    your_ai_client = None

# ========== 智能推荐函数 ==========
def recommend_learning_resources(user_id):
    """推荐学习资源"""
    try:
        user_tasks = Task.query.filter_by(user_id=user_id).all()
        
        if not user_tasks:
            # 如果没有任务，返回热门资源
            return LearningResource.query.order_by(
                LearningResource.views.desc()
            ).limit(6).all()
        
        # 提取任务关键词
        task_text = ' '.join([t.title + ' ' + (t.description or '') for t in user_tasks]).lower()
        
        # 获取所有资源
        resources = LearningResource.query.all()
        
        if not resources:
            return []
        
        # 计算匹配度
        scored_resources = []
        
        for resource in resources:
            score = 0
            
            # 1. 标题匹配
            if resource.title:
                title_lower = resource.title.lower()
                for word in title_lower.split():
                    if len(word) > 3 and word in task_text:
                        score += 2
            
            # 2. 关键词匹配
            if resource.keywords:
                keywords = [k.strip().lower() for k in resource.keywords.split(',')]
                for keyword in keywords:
                    if keyword and keyword in task_text:
                        score += 3
            
            # 3. 类型匹配
            if resource.resource_type:
                type_lower = resource.resource_type.lower()
                if type_lower in task_text:
                    score += 4
            
            if score > 0:
                scored_resources.append((score, resource))
        
        # 按匹配度排序
        scored_resources.sort(key=lambda x: x[0], reverse=True)
        
        # 获取匹配的资源
        matched_resources = [resource for _, resource in scored_resources[:6]]
        
        # 如果匹配资源不足，补充热门资源
        if len(matched_resources) < 3:
            additional = LearningResource.query.order_by(
                LearningResource.views.desc()
            ).limit(6 - len(matched_resources)).all()
            matched_resources.extend(additional)
        
        return matched_resources[:6]
        
    except Exception as e:
        print(f"资源推荐错误: {e}")
        return LearningResource.query.limit(6).all()

def recommend_health_tips(mood_score):
    """推荐健康建议"""
    tips = {
        1: ["深呼吸放松5分钟", "听一首舒缓的音乐", "与朋友聊聊天", "进行10分钟轻度运动"],
        2: ["喝一杯温水", "短暂休息5分钟", "写下你的感受", "看看窗外的风景"],
        3: ["继续保持", "规划下一步目标", "奖励自己小成就", "保持充足睡眠"],
        4: ["分享你的好心情", "帮助同学解决问题", "尝试新事物", "记录成功经验"],
        5: ["传播正能量", "设定更高目标", "庆祝你的成就", "帮助他人提升"]
    }
    
    return random.sample(tips.get(mood_score, tips[3]), 2)

def recommend_task_priority(user_id):
    """智能任务优先级建议"""
    try:
        tasks = Task.query.filter_by(user_id=user_id, status='pending').all()
        
        if not tasks:
            return []
        
        # 返回最近的任务
        return sorted(tasks, key=lambda x: x.created_at, reverse=True)[:3]
    except:
        return []

def ai_enhanced_recommendations(user_id):
    """使用智谱AI增强资源推荐"""
    if not your_ai_client:
        print("⚠️  智谱AI未启用，使用基础推荐")
        return recommend_learning_resources(user_id)
    
    try:
        # 获取用户信息
        user = User.query.get(user_id)
        user_tasks = Task.query.filter_by(user_id=user_id).all()
        recent_mood = MoodLog.query.filter_by(user_id=user_id)\
                                  .order_by(MoodLog.created_at.desc())\
                                  .first()
        
        # 准备请求数据
        ai_request_data = {
            "user_id": user_id,
            "username": user.username,
            "email": user.email,
            "user_tasks": [
                {
                    "title": task.title,
                    "description": task.description or "",
                    "priority": task.priority,
                    "status": task.status,
                    "created_at": task.created_at.isoformat() if task.created_at else None
                }
                for task in user_tasks[:10]  # 只发送最近10个任务
            ],
            "recent_mood": {
                "score": recent_mood.mood_score if recent_mood else 3,
                "note": recent_mood.note if recent_mood else "",
                "created_at": recent_mood.created_at.isoformat() if recent_mood else None
            } if recent_mood else None,
            "request_type": "learning_resource_recommendation",
            "max_recommendations": 6
        }
        
        print(f"🤖 调用智谱AI进行推荐，用户: {user.username}")
        
        # 调用智谱AI接口
        ai_response = your_ai_client.recommend_resources(ai_request_data)
        
        if ai_response and "recommendations" in ai_response:
            recommendations = ai_response["recommendations"]
            matched_resources = []
            
            for rec in recommendations[:6]:  # 限制为6个推荐
                if "title" in rec:
                    # 创建虚拟资源对象
                    matched_resources.append({
                        'id': f"ai_{len(matched_resources)}",  # 虚拟ID
                        'title': rec['title'],
                        'description': rec.get('description', '智谱AI智能推荐'),
                        'url': rec.get('url', '#'),
                        'resource_type': rec.get('type', 'AI推荐'),
                        'keywords': rec.get('keywords', 'AI,推荐,学习'),
                        'ai_recommendation': True,
                        'reason': rec.get('reason', '基于你的学习模式智能推荐'),
                        'is_virtual': True,
                        'views': 0,
                        'created_at': datetime.utcnow()
                    })
            
            # 如果AI推荐不足，补充基础推荐
            if len(matched_resources) < 3:
                print("📊 智谱AI推荐不足，补充基础推荐")
                basic_recs = recommend_learning_resources(user_id)
                matched_resources.extend(basic_recs[:6 - len(matched_resources)])
            
            print(f"✅ 智谱AI返回 {len(matched_resources)} 个推荐")
            return matched_resources[:6]
        else:
            print("⚠️  智谱AI返回格式不正确，使用基础推荐")
            return recommend_learning_resources(user_id)
            
    except Exception as e:
        print(f"❌ 智谱AI推荐错误: {e}")
        return recommend_learning_resources(user_id)

def ai_analyze_learning(user_id):
    """使用智谱AI分析学习模式"""
    if not your_ai_client:
        return {
            "efficiency": "AI未启用",
            "characteristics": "请配置智谱AI",
            "suggestions": ["联系管理员启用AI功能"],
            "predicted_score": 0,
            "encouragement": "你可以先使用基本功能"
        }
    
    try:
        # 收集学习数据
        user_tasks = Task.query.filter_by(user_id=user_id).all()
        completed_tasks = [t for t in user_tasks if t.status == 'completed']
        completion_rate = len(completed_tasks) / len(user_tasks) if user_tasks else 0
        
        # 准备分析数据
        analysis_request = {
            "user_id": user_id,
            "total_tasks": len(user_tasks),
            "completed_tasks": len(completed_tasks),
            "completion_rate": round(completion_rate * 100, 1),
            "task_history": [
                {
                    "title": t.title,
                    "status": t.status,
                    "priority": t.priority,
                    "created_at": t.created_at.isoformat() if t.created_at else None,
                    "due_date": t.due_date.isoformat() if t.due_date else None
                }
                for t in user_tasks[-10:]  # 最近10个任务
            ],
            "request_type": "learning_analysis"
        }
        
        # 调用智谱AI
        analysis_result = your_ai_client.analyze_learning(analysis_request)
        
        # 确保返回标准格式
        if analysis_result:
            return {
                "efficiency": analysis_result.get("efficiency", "良好"),
                "characteristics": analysis_result.get("characteristics", "需要更多数据"),
                "suggestions": analysis_result.get("suggestions", ["保持学习节奏", "制定明确目标", "定期复习"]),
                "predicted_score": analysis_result.get("predicted_score", 75),
                "encouragement": analysis_result.get("encouragement", "继续加油！")
            }
        else:
            raise Exception("智谱AI分析返回空结果")
            
    except Exception as e:
        print(f"❌ 智谱AI分析错误: {e}")
        return {
            "efficiency": "分析失败",
            "characteristics": "数据不足",
            "suggestions": ["请添加更多学习任务"],
            "predicted_score": 0,
            "encouragement": "开始你的学习之旅吧！"
        }

def ai_chat_response(user_id, message):
    """使用智汇通智能体进行聊天"""
    if not your_ai_client:
        return "智汇通智能体功能未启用。"
    
    try:
        # 直接调用聊天，不需要复杂的上下文
        response = your_ai_client.simple_chat(message)
        
        if response and len(response) > 0:
            return response
        else:
            return "智汇通智能体正在思考，请稍后再试。"
            
    except Exception as e:
        print(f"❌ 智汇通聊天错误: {e}")
        return "智汇通智能体暂时无法响应，请稍后重试。"

# ========== 学习计时器相关函数 ==========
@app.route('/api/study/start', methods=['POST'])
@login_required
def start_study_session():
    """开始学习计时 - 支持自定义任务名"""
    try:
        data = request.get_json()
        task_id = data.get('task_id')
        custom_task_name = data.get('custom_task_name', '').strip()
        
        # 检查是否已有活跃会话
        active_session = StudySession.query.filter_by(
            user_id=current_user.id,
            end_time=None
        ).first()
        
        if active_session:
            return jsonify({
                'success': False,
                'message': '已有活跃的学习会话，请先结束当前会话'
            })
        
        # 如果没有选择任务但有自定义任务名，创建一个临时任务
        temp_task_id = None
        if not task_id and custom_task_name:
            # 创建一个临时任务记录
            temp_task = Task(
                title=custom_task_name,
                description='学习计时器创建的临时任务',
                priority=2,
                status='pending',
                user_id=current_user.id
            )
            db.session.add(temp_task)
            db.session.flush()  # 获取ID但不提交
            temp_task_id = temp_task.id
            task_id = temp_task_id
        
        # 创建新的学习会话
        new_session = StudySession(
            user_id=current_user.id,
            task_id=task_id if task_id else None,
            start_time=datetime.utcnow(),
            session_type='focus'
        )
        
        # 如果使用自定义任务名，保存到备注
        if custom_task_name:
            new_session.notes = custom_task_name
        
        db.session.add(new_session)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'session_id': new_session.id,
            'task_id': task_id,
            'custom_task_name': custom_task_name if custom_task_name else None,
            'start_time': new_session.start_time.isoformat(),
            'message': '学习计时开始！'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"开始学习计时错误: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/study/end', methods=['POST'])
@login_required
def end_study_session():
    """结束学习计时"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        focus_score = data.get('focus_score', 3)
        notes = data.get('notes', '')
        
        if not session_id:
            # 如果没有指定session_id，找到当前活跃的会话
            session = StudySession.query.filter_by(
                user_id=current_user.id,
                end_time=None
            ).first()
        else:
            session = StudySession.query.get(session_id)
        
        if not session:
            return jsonify({'success': False, 'message': '未找到活跃的学习会话'})
        
        if session.user_id != current_user.id:
            return jsonify({'success': False, 'message': '无权操作此会话'})
        
        # 计算学习时长
        end_time = datetime.utcnow()
        duration = int((end_time - session.start_time).total_seconds() / 60)
        
        # 更新会话信息
        session.end_time = end_time
        session.duration_minutes = duration
        session.focus_score = focus_score
        
        # 如果notes有内容，更新备注
        if notes and notes.strip():
            # 如果已经有一个自定义任务名，就添加到后面
            if session.notes:
                session.notes += f"\n备注: {notes.strip()}"
            else:
                session.notes = notes.strip()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'duration': duration,
            'end_time': end_time.isoformat(),
            'message': f'学习结束！本次学习了 {duration} 分钟'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"结束学习计时错误: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/study/active')
@login_required
def get_active_study_session():
    """获取当前活跃的学习会话"""
    try:
        session = StudySession.query.filter_by(
            user_id=current_user.id,
            end_time=None
        ).first()
        
        if session:
            duration = int((datetime.utcnow() - session.start_time).total_seconds() / 60)
            
            # 获取任务信息
            task_name = "自由学习"
            if session.task_id:
                task = Task.query.get(session.task_id)
                if task:
                    task_name = task.title
            elif session.notes:
                task_name = session.notes
            
            return jsonify({
                'success': True,
                'active': True,
                'session_id': session.id,
                'start_time': session.start_time.isoformat(),
                'duration': duration,
                'task_id': session.task_id,
                'task_name': task_name
            })
        else:
            return jsonify({
                'success': True,
                'active': False
            })
            
    except Exception as e:
        print(f"获取活跃会话错误: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/study/stats')
@login_required
def get_study_statistics():
    """获取学习统计数据和饼状图数据 - 修复版"""
    try:
        # 获取所有学习数据（不限时间）
        sessions = StudySession.query.filter(
            StudySession.user_id == current_user.id,
            StudySession.end_time.isnot(None)
        ).all()
        
        if not sessions:
            return jsonify({
                'success': True,
                'stats': {
                    'total_study': 0,
                    'week_study': 0,
                    'today_study': 0,
                    'avg_focus': 0,
                    'session_count': 0,
                    'task_count': 0
                },
                'pie_chart': {
                    'labels': ['暂无学习数据'],
                    'datasets': [{
                        'data': [100],
                        'backgroundColor': ['#e2e8f0'],
                        'borderColor': '#fff',
                        'borderWidth': 2
                    }]
                },
                'trend_data': [],
                'task_details': [],
                'message': '暂无学习数据，开始学习后这里会显示统计信息'
            })
        
        # 按任务统计时长
        task_stats = {}
        for session in sessions:
            # 获取任务名
            if session.task_id:
                task = Task.query.get(session.task_id)
                if task:
                    task_name = task.title
                else:
                    task_name = "已删除的任务"
            else:
                # 如果没有关联任务，使用备注或默认名称
                if session.notes and session.notes.strip():
                    task_name = session.notes.strip()
                    if len(task_name) > 30:
                        task_name = task_name[:27] + "..."
                else:
                    task_name = "自由学习"
            
            # 确保任务名不为空
            if not task_name or task_name.strip() == "":
                task_name = "未命名学习"
            
            # 添加时长
            duration = session.duration_minutes or 0
            if duration > 0:
                if task_name not in task_stats:
                    task_stats[task_name] = 0
                task_stats[task_name] += duration
        
        # 如果没有有效数据
        if not task_stats:
            return jsonify({
                'success': True,
                'stats': {
                    'total_study': 0,
                    'week_study': 0,
                    'today_study': 0,
                    'avg_focus': 0,
                    'session_count': len(sessions),
                    'task_count': 0
                },
                'pie_chart': {
                    'labels': ['暂无有效学习时长'],
                    'datasets': [{
                        'data': [100],
                        'backgroundColor': ['#e2e8f0'],
                        'borderColor': '#fff',
                        'borderWidth': 2
                    }]
                },
                'trend_data': [],
                'task_details': []
            })
        
        # 转换为饼状图数据
        sorted_tasks = sorted(task_stats.items(), key=lambda x: x[1], reverse=True)
        
        # 只显示前8个任务，其他的归为"其他"
        if len(sorted_tasks) > 8:
            main_tasks = sorted_tasks[:7]
            other_time = sum(time for _, time in sorted_tasks[7:])
            main_tasks.append(("其他任务", other_time))
        else:
            main_tasks = sorted_tasks
        
        # 生成饼状图数据
        colors = [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
            '#9966FF', '#FF9F40', '#C9CBCF', '#7CFC00'
        ]
        
        # 确保每个任务都有颜色
        while len(colors) < len(main_tasks):
            colors.extend(colors)  # 循环使用颜色
        
        pie_data = {
            'labels': [name for name, _ in main_tasks],
            'datasets': [{
                'data': [time for _, time in main_tasks],
                'backgroundColor': colors[:len(main_tasks)],
                'borderColor': '#fff',
                'borderWidth': 2
            }]
        }
        
        # 总统计
        total_study = sum(task_stats.values())
        
        # 本周统计
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        week_sessions = [s for s in sessions if s.start_time >= seven_days_ago]
        week_study = sum(s.duration_minutes or 0 for s in week_sessions)
        
        # 今日统计
        today = datetime.utcnow().date()
        today_sessions = [s for s in sessions if s.start_time.date() == today]
        today_study = sum(s.duration_minutes or 0 for s in today_sessions)
        
        # 平均专注度
        focus_scores = [s.focus_score for s in sessions if s.focus_score and s.focus_score > 0]
        avg_focus = round(sum(focus_scores) / len(focus_scores), 1) if focus_scores else 0
        
        # 学习趋势（最近7天每日学习时长）
        trend_data = []
        for i in range(7):
            day = datetime.utcnow().date() - timedelta(days=6-i)
            day_sessions = [s for s in sessions if s.start_time.date() == day]
            day_study = sum(s.duration_minutes or 0 for s in day_sessions)
            trend_data.append({
                'date': day.strftime('%m-%d'),
                'duration': day_study
            })
        
        return jsonify({
            'success': True,
            'stats': {
                'total_study': total_study,
                'week_study': week_study,
                'today_study': today_study,
                'avg_focus': avg_focus,
                'session_count': len(sessions),
                'task_count': len(task_stats)
            },
            'pie_chart': pie_data,
            'trend_data': trend_data,
            'task_details': [
                {
                    'task': name, 
                    'duration': time, 
                    'percentage': round(time/total_study*100, 1) if total_study > 0 else 0
                }
                for name, time in sorted_tasks[:10]
            ]
        })
        
    except Exception as e:
        print(f"❌ 获取学习统计错误: {e}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'message': str(e),
            'stats': {},
            'pie_chart': {
                'labels': ['加载失败'],
                'datasets': [{'data': [1], 'backgroundColor': ['#ef4444']}]
            },
            'trend_data': []
        })

@app.route('/api/study/sessions')
@login_required
def get_study_sessions():
    """获取学习会话历史"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        sessions = StudySession.query.filter(
            StudySession.user_id == current_user.id,
            StudySession.end_time.isnot(None)
        ).order_by(
            StudySession.start_time.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        session_list = []
        for session in sessions.items:
            # 获取任务名
            task_name = "自由学习"
            if session.task_id:
                task = Task.query.get(session.task_id)
                task_name = task.title if task else "已删除的任务"
            elif session.notes:
                task_name = session.notes
            
            # 格式化日期
            start_time = session.start_time.strftime('%Y-%m-%d %H:%M')
            end_time = session.end_time.strftime('%H:%M') if session.end_time else None
            
            session_list.append({
                'id': session.id,
                'task_name': task_name,
                'task_id': session.task_id,
                'start_time': start_time,
                'end_time': end_time,
                'duration': session.duration_minutes or 0,
                'focus_score': session.focus_score or 0,
                'notes': session.notes,
                'date': session.start_time.strftime('%Y-%m-%d')
            })
        
        return jsonify({
            'success': True,
            'sessions': session_list,
            'total': sessions.total,
            'pages': sessions.pages,
            'current_page': sessions.page
        })
        
    except Exception as e:
        print(f"获取学习会话历史错误: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/study/delete/<int:session_id>', methods=['DELETE'])
@login_required
def delete_study_session(session_id):
    """删除学习会话"""
    try:
        session = StudySession.query.get_or_404(session_id)
        
        if session.user_id != current_user.id:
            return jsonify({'success': False, 'message': '无权删除此会话'})
        
        db.session.delete(session)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '学习记录已删除'
        })
        
    except Exception as e:
        print(f"删除学习会话错误: {e}")
        return jsonify({'success': False, 'message': str(e)})

# ========== 启动时自动加载资源 ==========
def init_database():
    """初始化数据库和资源"""
    with app.app_context():
        # 创建所有表
        db.create_all()
        print("✅ 数据库表已创建")
        
        # 检查是否有资源
        resource_count = LearningResource.query.count()
        print(f"📊 当前有 {resource_count} 个学习资源")
        
        # 如果资源太少，自动加载
        if resource_count < 50:  # 降低阈值，更容易触发加载
            print("🔄 资源不足，正在自动加载学习资源...")
            start_auto_load_resources()
        else:
            print("✅ 资源充足，跳过自动加载")
        
        # 创建测试用户
        if User.query.filter_by(username='admin').first() is None:
            admin_user = User(
                username='admin',
                email='admin@campus.com',
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(admin_user)
            db.session.commit()
            print("✅ 测试用户已创建: admin / admin123")

def force_load_resources():
    """强制加载新资源（用于开发测试）"""
    with app.app_context():
        print("🔄 强制加载新资源...")
        
        try:
            if simple_crawler:
                # 获取新资源
                resources = simple_crawler.crawl_real_resources()
                
                if resources and len(resources) > 0:
                    # 保存到数据库
                    existing_urls = set([r.url for r in LearningResource.query.all()])
                    added_count = 0
                    updated_count = 0
                    
                    for resource_data in resources:
                        # 检查是否已存在
                        existing = LearningResource.query.filter_by(url=resource_data['url']).first()
                        
                        if existing:
                            # 更新现有资源
                            existing.title = resource_data['title'][:200]
                            existing.description = resource_data['description'][:500]
                            existing.resource_type = resource_data.get('resource_type', '其他')
                            existing.keywords = resource_data.get('keywords', '')
                            updated_count += 1
                        else:
                            # 添加新资源
                            new_resource = LearningResource(
                                title=resource_data['title'][:200],
                                description=resource_data['description'][:500],
                                url=resource_data['url'][:500],
                                resource_type=resource_data.get('resource_type', '其他'),
                                keywords=resource_data.get('keywords', ''),
                                created_at=resource_data.get('created_at', datetime.utcnow())
                            )
                            db.session.add(new_resource)
                            added_count += 1
                    
                    db.session.commit()
                    
                    print(f"✅ 资源加载完成：新增 {added_count} 个，更新 {updated_count} 个")
                    
                    # 显示最终统计
                    total_count = LearningResource.query.count()
                    print(f"📊 数据库现有 {total_count} 个学习资源")
                    
                    # 显示分类统计
                    from collections import Counter
                    categories = Counter([r.resource_type for r in LearningResource.query.all()])
                    print("📊 资源分类统计:")
                    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                        print(f"  {cat}: {count} 个")
                    
                else:
                    print("❌ 资源加载失败，返回空列表")
                    
            else:
                print("⚠️  爬虫模块不可用，跳过资源加载")
                
        except Exception as e:
            print(f"❌ 资源加载失败: {e}")
            import traceback
            traceback.print_exc()

def start_auto_load_resources():
    """启动时自动加载资源"""
    def background_load():
        time.sleep(2)  # 等待应用完全启动
        
        with app.app_context():
            try:
                if simple_crawler:
                    print("\n" + "=" * 60)
                    print("🤖 正在后台加载学习资源...")
                    print("=" * 60)
                    
                    # 获取资源
                    resources = simple_crawler.crawl_real_resources()
                    
                    if resources and len(resources) > 0:
                        # 保存到数据库
                        existing_urls = set([r.url for r in LearningResource.query.all()])
                        added_count = 0
                        
                        for resource_data in resources:
                            if resource_data['url'] not in existing_urls:
                                new_resource = LearningResource(
                                    title=resource_data['title'][:200],
                                    description=resource_data['description'][:500],
                                    url=resource_data['url'][:500],
                                    resource_type=resource_data.get('resource_type', '其他'),
                                    keywords=resource_data.get('keywords', ''),
                                    created_at=datetime.utcnow()
                                )
                                db.session.add(new_resource)
                                existing_urls.add(resource_data['url'])
                                added_count += 1
                        
                        db.session.commit()
                        
                        if added_count > 0:
                            print(f"✅ 资源加载完成，新增 {added_count} 个资源")
                        else:
                            print("⚠️  没有新增资源（可能已存在）")
                            
                        # 显示最终统计
                        total_count = LearningResource.query.count()
                        print(f"📊 数据库现有 {total_count} 个学习资源")
                    else:
                        print("❌ 资源加载失败")
                        
                else:
                    print("⚠️  爬虫模块不可用，跳过资源加载")
                    
            except Exception as e:
                print(f"❌ 资源加载失败: {e}")
    
    # 在后台线程中运行
    thread = threading.Thread(target=background_load, daemon=True)
    thread.start()

# ========== 基础路由 ==========
@app.route('/')
def index():
    """首页"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """登录页面"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            flash('登录成功！', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('用户名或密码错误！', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """注册页面"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # 验证输入
        if not username or not email or not password:
            flash('请填写所有必填字段！', 'danger')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('两次输入的密码不一致！', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(username=username).first():
            flash('用户名已存在！', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('邮箱已被注册！', 'danger')
            return redirect(url_for('register'))
        
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        
        db.session.add(new_user)
        db.session.commit()
        flash('注册成功！请登录。', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """仪表盘"""
    try:
        # 统计数据
        total_tasks = Task.query.filter_by(user_id=current_user.id).count()
        completed_tasks = Task.query.filter_by(user_id=current_user.id, status='completed').count()
        pending_tasks = total_tasks - completed_tasks
        
        # 计算完成率
        completion_rate = round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1)
        
        # 获取推荐
        learning_resources = ai_enhanced_recommendations(current_user.id)
        urgent_tasks = recommend_task_priority(current_user.id)
        
        # 最近心情
        recent_mood = MoodLog.query.filter_by(user_id=current_user.id)\
                                   .order_by(MoodLog.created_at.desc())\
                                   .first()
        
        health_tips = recommend_health_tips(recent_mood.mood_score if recent_mood else 3)
        
        return render_template('dashboard.html',
                             total_tasks=total_tasks,
                             completed_tasks=completed_tasks,
                             pending_tasks=pending_tasks,
                             completion_rate=completion_rate,
                             learning_resources=learning_resources,
                             urgent_tasks=urgent_tasks,
                             recent_mood=recent_mood,
                             health_tips=health_tips,
                             username=current_user.username,
                             now=datetime.utcnow(),
                             ai_enabled=your_ai_client is not None)
    except Exception as e:
        print(f"仪表盘错误: {e}")
        flash('加载仪表盘时出现错误，请刷新重试。', 'warning')
        return render_template('dashboard.html',
                             total_tasks=0,
                             completed_tasks=0,
                             pending_tasks=0,
                             completion_rate=0,
                             learning_resources=[],
                             urgent_tasks=[],
                             recent_mood=None,
                             health_tips=[],
                             username=current_user.username,
                             now=datetime.utcnow(),
                             ai_enabled=your_ai_client is not None)

@app.route('/tasks')
@login_required
def tasks():
    """任务管理页面"""
    try:
        tasks_list = Task.query.filter_by(user_id=current_user.id)\
                               .order_by(Task.created_at.desc())\
                               .all()
    except Exception as e:
        print(f"任务页面错误: {e}")
        tasks_list = []
        flash('加载任务列表时出现错误。', 'warning')
    
    return render_template('tasks.html', tasks=tasks_list, now=datetime.utcnow())

@app.route('/add_task', methods=['POST'])
@login_required
def add_task():
    """添加任务"""
    try:
        title = request.form.get('title', '').strip()
        if not title:
            flash('任务标题不能为空！', 'danger')
            return redirect(url_for('tasks'))
        
        description = request.form.get('description', '').strip()
        priority = request.form.get('priority', '2')
        
        # 处理截止日期
        due_date_str = request.form.get('due_date', '')
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except:
                pass
        
        new_task = Task(
            title=title,
            description=description,
            priority=int(priority),
            due_date=due_date,
            user_id=current_user.id
        )
        
        db.session.add(new_task)
        db.session.commit()
        flash('任务添加成功！', 'success')
        
    except Exception as e:
        db.session.rollback()
        print(f"添加任务错误: {e}")
        flash('添加任务失败，请重试。', 'danger')
    
    return redirect(url_for('tasks'))

@app.route('/update_task/<int:task_id>', methods=['POST'])
@login_required
def update_task(task_id):
    """更新任务"""
    try:
        task = Task.query.get_or_404(task_id)
        
        # 检查权限
        if task.user_id != current_user.id:
            flash('无权操作此任务！', 'danger')
            return redirect(url_for('tasks'))
        
        title = request.form.get('title', '').strip()
        if not title:
            flash('任务标题不能为空！', 'danger')
            return redirect(url_for('tasks'))
        
        task.title = title
        task.description = request.form.get('description', '').strip()
        task.priority = int(request.form.get('priority', '2'))
        
        # 处理截止日期
        due_date_str = request.form.get('due_date', '')
        task.due_date = None
        if due_date_str:
            try:
                task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except:
                pass
        
        db.session.commit()
        flash('任务更新成功！', 'success')
        
    except Exception as e:
        db.session.rollback()
        print(f"更新任务错误: {e}")
        flash('更新任务失败，请重试。', 'danger')
    
    return redirect(url_for('tasks'))

@app.route('/batch_complete', methods=['POST'])
@login_required
def batch_complete_api():
    """批量完成任务"""
    try:
        data = request.get_json()
        task_ids = data.get('task_ids', [])
        
        if not task_ids:
            return jsonify({'success': False, 'message': '未选择任务'})
        
        tasks = Task.query.filter(
            Task.id.in_(task_ids),
            Task.user_id == current_user.id,
            Task.status != 'completed'
        ).all()
        
        completed_count = 0
        for task in tasks:
            task.status = 'completed'
            task.completed_at = datetime.utcnow()
            completed_count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'已批量完成 {completed_count} 个任务',
            'completed_count': completed_count
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"批量完成任务错误: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/batch_delete', methods=['POST'])
@login_required
def batch_delete_api():
    """批量删除任务"""
    try:
        data = request.get_json()
        task_ids = data.get('task_ids', [])
        
        if not task_ids:
            return jsonify({'success': False, 'message': '未选择任务'})
        
        tasks = Task.query.filter(
            Task.id.in_(task_ids),
            Task.user_id == current_user.id
        ).all()
        
        deleted_count = 0
        for task in tasks:
            db.session.delete(task)
            deleted_count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'已批量删除 {deleted_count} 个任务',
            'deleted_count': deleted_count
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"批量删除任务错误: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/mood')
@login_required
def mood():
    """心情记录页面"""
    try:
        # 获取所有心情记录
        moods = MoodLog.query.filter_by(user_id=current_user.id)\
                             .order_by(MoodLog.created_at.desc())\
                             .all()
        
        # 获取今日心情
        today = datetime.utcnow().date()
        today_mood = MoodLog.query.filter(
            MoodLog.user_id == current_user.id,
            db.func.date(MoodLog.created_at) == today
        ).first()
        
        return render_template('mood.html', moods=moods, today_mood=today_mood)
    except Exception as e:
        print(f"心情页面错误: {e}")
        flash('加载心情记录时出现错误。', 'warning')
        return render_template('mood.html', moods=[], today_mood=None)

@app.route('/log_mood', methods=['POST'])
@login_required
def log_mood():
    """记录心情"""
    try:
        mood_score = request.form.get('mood_score', '').strip()
        note = request.form.get('note', '').strip()
        
        if not mood_score:
            flash('请选择心情评分！', 'danger')
            return redirect(url_for('mood'))
        
        # 检查今日是否已记录
        today = datetime.utcnow().date()
        existing_mood = MoodLog.query.filter(
            MoodLog.user_id == current_user.id,
            db.func.date(MoodLog.created_at) == today
        ).first()
        
        if existing_mood:
            existing_mood.mood_score = int(mood_score)
            existing_mood.note = note
            flash('心情记录已更新！', 'success')
        else:
            mood_log = MoodLog(
                mood_score=int(mood_score),
                note=note,
                user_id=current_user.id
            )
            db.session.add(mood_log)
            flash('心情记录成功！', 'success')
        
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        print(f"记录心情错误: {e}")
        flash('记录心情失败，请重试。', 'danger')
    
    return redirect(url_for('mood'))

@app.route('/resources')
@login_required
def resources():
    """学习资源页面 - 修复版"""
    try:
        # 获取所有资源（确保有数据）
        all_resources = LearningResource.query.order_by(
            LearningResource.created_at.desc()
        ).limit(100).all()  # 限制数量，避免数据太多
        
        # 智能推荐 - 简化版，确保能工作
        try:
            if your_ai_client:
                recommended = ai_enhanced_recommendations(current_user.id)
            else:
                recommended = recommend_learning_resources(current_user.id)
        except Exception as ai_error:
            print(f"⚠️  AI推荐失败: {ai_error}")
            # 使用简单的推荐
            recommended = LearningResource.query.order_by(
                LearningResource.views.desc()
            ).limit(6).all()
        
        # 获取分类统计 - 简化版
        categories = []
        if all_resources:
            from collections import Counter
            category_counter = Counter()
            for resource in all_resources:
                cat = resource.resource_type or '未分类'
                category_counter[cat] += 1
            
            # 转换为列表并排序
            categories = sorted(category_counter.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return render_template('resources.html', 
                             resources=all_resources, 
                             recommended=recommended,
                             categories=categories,
                             ai_enabled=your_ai_client is not None,
                             now=datetime.utcnow())
        
    except Exception as e:
        print(f"❌ 资源页面错误: {e}")
        import traceback
        traceback.print_exc()
        
        # 返回一个简单的错误页面，至少让页面能打开
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>资源页面错误 - CampusPulse</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 40px; }
                .error-box { 
                    background: #f8f9fa; 
                    border: 1px solid #dee2e6; 
                    border-radius: 10px; 
                    padding: 30px;
                    max-width: 800px;
                    margin: 0 auto;
                }
                .error-icon { 
                    font-size: 48px; 
                    color: #dc3545; 
                    text-align: center;
                    margin-bottom: 20px;
                }
            </style>
        </head>
        <body>
            <div class="error-box">
                <div class="error-icon">⚠️</div>
                <h2>资源页面加载失败</h2>
                <p>系统遇到了一些问题，正在修复中...</p>
                <p><strong>错误信息：</strong> {}</p>
                <div style="margin-top: 30px;">
                    <a href="/dashboard" style="background: #007bff; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none;">返回仪表盘</a>
                    <button onclick="location.reload()" style="background: #6c757d; color: white; padding: 10px 20px; border: none; border-radius: 5px; margin-left: 10px;">刷新页面</button>
                </div>
            </div>
        </body>
        </html>
        """.format(str(e))

# ========== AI聊天页面 ==========
@app.route('/chat')
@login_required
def chat():
    """AI聊天页面"""
    # 获取聊天历史
    chat_history = ChatMessage.query.filter_by(user_id=current_user.id)\
                                   .order_by(ChatMessage.created_at.asc())\
                                   .limit(50)\
                                   .all()
    
    return render_template('chat.html', 
                          chat_history=chat_history,
                          ai_enabled=your_ai_client is not None)

@app.route('/api/chat/send', methods=['POST'])
@login_required
def send_chat_message():
    """发送聊天消息"""
    if not your_ai_client:
        return jsonify({
            'success': False,
            'message': '智谱AI功能未启用'
        })
    
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'success': False, 'message': '消息不能为空'})
        
        # 保存用户消息
        user_msg = ChatMessage(
            user_id=current_user.id,
            message=message,
            is_ai=False
        )
        db.session.add(user_msg)
        db.session.commit()
        
        # 调用智谱AI
        ai_response = your_ai_client.simple_chat(message)
        
        # 保存AI回复
        ai_msg = ChatMessage(
            user_id=current_user.id,
            message=message,  # 原消息
            response=ai_response,
            is_ai=True
        )
        db.session.add(ai_msg)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'response': ai_response,
            'message_id': ai_msg.id,
            'timestamp': datetime.now().strftime('%H:%M'),
            'ai_model': '智谱GLM-4'
        })
        
    except Exception as e:
        print(f"❌ 聊天消息发送错误: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/logout')
@login_required
def logout():
    """登出"""
    logout_user()
    flash('您已成功登出。', 'success')
    return redirect(url_for('login'))

@app.route('/api/resources/suggest', methods=['POST'])
@login_required
def suggest_resource():
    """用户推荐学习资源"""
    try:
        data = request.get_json()
        
        # 验证数据
        if not data.get('title') or not data.get('url'):
            return jsonify({
                'success': False,
                'message': '标题和链接不能为空'
            })
        
        # 检查是否已存在
        existing = LearningResource.query.filter_by(url=data['url']).first()
        if existing:
            return jsonify({
                'success': False,
                'message': '该链接已存在'
            })
        
        # 创建资源（标记为待审核）
        new_resource = LearningResource(
            title=data['title'][:200],
            description=data.get('description', '')[:500],
            url=data['url'][:500],
            resource_type=data.get('resource_type'),
            keywords=data.get('keywords', ''),
            status='pending',  # 待审核状态
            suggested_by=current_user.id,
            created_at=datetime.utcnow()
        )
        
        db.session.add(new_resource)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '资源推荐成功，等待审核',
            'resource_id': new_resource.id
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"推荐资源错误: {e}")
        return jsonify({
            'success': False,
            'message': '推荐失败，请稍后重试'
        })

@app.route('/api/resources/stats')
@login_required
def get_resource_stats():
    """获取资源统计信息"""
    try:
        total = LearningResource.query.count()
        
        # 今日新增
        today = datetime.utcnow().date()
        today_count = LearningResource.query.filter(
            db.func.date(LearningResource.created_at) == today
        ).count()
        
        # 总访问量
        total_views = db.session.query(
            db.func.sum(LearningResource.views)
        ).scalar() or 0
        
        # 分类统计
        from collections import Counter
        resources = LearningResource.query.all()
        categories = Counter([r.resource_type or '未分类' for r in resources])
        
        return jsonify({
            'success': True,
            'stats': {
                'total': total,
                'today': today_count,
                'total_views': total_views,
                'categories': len(categories)
            }
        })
        
    except Exception as e:
        print(f"获取资源统计错误: {e}")
        return jsonify({'success': False})
# ========== AI助手路由 ==========
@app.route('/ai_assistant')
@login_required
def ai_assistant():
    """智谱GLM-4 AI助手页面"""
    print(f"🎯 访问AI助手，用户: {current_user.username}")
    
    try:
        # 检查模板是否存在
        import os
        template_path = os.path.join('templates', 'ai_assistant.html')
        
        if not os.path.exists(template_path):
            print(f"❌ 模板文件不存在: {template_path}")
            return """
            <h1>模板文件缺失</h1>
            <p>ai_assistant.html 不存在于 templates 文件夹中。</p>
            <p>请确保文件位置正确。</p>
            """
        
        # 渲染模板
        print(f"✅ 模板存在，准备渲染: {template_path}")
        return render_template('ai_assistant.html')
        
    except Exception as e:
        import traceback
        error_msg = f"渲染AI助手时出错: {str(e)}"
        print(f"❌ {error_msg}")
        traceback.print_exc()
        
        # 返回错误信息（开发阶段）
        return f"""
        <html>
        <head><title>AI助手错误</title></head>
        <body style="font-family: Arial; padding: 20px;">
            <h1 style="color: #ef4444;">AI助手加载失败</h1>
            <h3>错误信息:</h3>
            <pre style="background: #f3f4f6; padding: 15px; border-radius: 5px;">
{str(e)}
            </pre>
            <h3>解决方案:</h3>
            <ol>
                <li>检查 templates 文件夹中是否有 ai_assistant.html</li>
                <li>检查文件编码是否为 UTF-8</li>
                <li>尝试访问 <a href="/dashboard">仪表盘</a> 确认其他页面正常</li>
            </ol>
        </body>
        </html>
        """

# ========== API 路由 ==========
@app.route('/api/resource/view/<int:resource_id>', methods=['POST'])
@login_required
def increment_resource_view(resource_id):
    """增加资源查看次数"""
    try:
        resource = LearningResource.query.get_or_404(resource_id)
        resource.views = (resource.views or 0) + 1
        db.session.commit()
        return jsonify({'success': True, 'views': resource.views})
    except:
        return jsonify({'success': False})

# ========== AI API 路由 ==========
@app.route('/api/ai/analyze')
@login_required
def ai_analyze():
    """AI学习分析"""
    if not your_ai_client:
        return jsonify({
            'success': False,
            'message': '智谱AI功能未启用',
            'analysis': {
                'efficiency': 'AI未启用',
                'characteristics': '请配置智谱AI接口',
                'suggestions': ['联系管理员启用AI功能'],
                'predicted_score': 0,
                'encouragement': '你可以先使用基本功能'
            }
        })
    
    try:
        # 调用智谱AI分析
        analysis = ai_analyze_learning(current_user.id)
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'stats': {
                'total_tasks': Task.query.filter_by(user_id=current_user.id).count(),
                'completed': Task.query.filter_by(user_id=current_user.id, status='completed').count(),
                'completion_rate': round((Task.query.filter_by(user_id=current_user.id, status='completed').count() / 
                                        max(Task.query.filter_by(user_id=current_user.id).count(), 1) * 100), 1)
            }
        })
        
    except Exception as e:
        print(f"❌ AI分析错误: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/ai/chat', methods=['POST'])
@login_required
def ai_chat_api():
    """AI聊天API"""
    if not your_ai_client:
        return jsonify({
            'success': False,
            'response': '智谱AI功能未启用，请先配置AI接口。'
        })
    
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'success': False, 'response': '请输入消息'})
        
        # 调用智谱AI
        response = ai_chat_response(current_user.id, message)
        
        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.now().strftime('%H:%M'),
            'ai_type': '智谱GLM-4'
        })
        
    except Exception as e:
        print(f"❌ AI聊天错误: {e}")
        return jsonify({'success': False, 'response': '系统繁忙，请稍后重试。'})

@app.route('/api/ai/recommend', methods=['GET'])
@login_required
def ai_recommend():
    """AI资源推荐（独立API）"""
    try:
        if your_ai_client:
            recommendations = ai_enhanced_recommendations(current_user.id)
            
            # 格式化响应
            formatted_recs = []
            for rec in recommendations:
                if isinstance(rec, dict) and rec.get('is_virtual'):
                    formatted_recs.append({
                        'title': rec['title'],
                        'description': rec['description'],
                        'url': rec['url'],
                        'type': rec['resource_type'],
                        'ai_recommended': True,
                        'reason': rec.get('reason', '智谱AI智能推荐')
                    })
                else:
                    formatted_recs.append({
                        'title': rec.title,
                        'description': rec.description,
                        'url': rec.url,
                        'type': rec.resource_type,
                        'ai_recommended': False,
                        'views': rec.views or 0
                    })
            
            return jsonify({
                'success': True,
                'recommendations': formatted_recs,
                'ai_enabled': True
            })
        else:
            return jsonify({
                'success': False,
                'message': '智谱AI未启用',
                'ai_enabled': False
            })
            
    except Exception as e:
        print(f"❌ AI推荐API错误: {e}")
        return jsonify({'success': False, 'message': str(e)})

# ========== 错误处理 ==========
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# ========== 启动应用 ==========
if __name__ == '__main__':
    print("=" * 50)
    print("🚀 正在启动 CampusPulse 智能学习平台...")
    
    # 初始化数据库
    with app.app_context():
        init_database()
    
    print("🌐 访问地址: http://127.0.0.1:5000")
    print("📱 可在同一WiFi下的手机访问本机IP地址")
    app.run(debug=True, port=5000, host='0.0.0.0')