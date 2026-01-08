# simple_crawler.py 
import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime

class SimpleResourceCrawler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }

    def crawl_real_resources(self):
        """爬取全方位高质量资源"""
        print("\n" + "=" * 60)
        print("🚀 开始爬取全方位高质量学习生活资源...")
        print("=" * 60)
        
        all_resources = []
        
        # 1. 技术编程类资源
        print("\n💻 加载技术编程资源...")
        tech_resources = self.get_technology_resources()
        all_resources.extend(tech_resources)
        
        # 2. 学术学习类资源
        print("\n📚 加载学术学习资源...")
        academic_resources = self.get_academic_resources()
        all_resources.extend(academic_resources)
        
        # 3. 艺术创意类资源
        print("\n🎨 加载艺术创意资源...")
        art_resources = self.get_art_creative_resources()
        all_resources.extend(art_resources)
        
        # 4. 生活技能类资源
        print("\n🏠 加载生活技能资源...")
        life_resources = self.get_life_skill_resources()
        all_resources.extend(life_resources)
        
        # 5. 健康养生类资源
        print("\n💪 加载健康养生资源...")
        health_resources = self.get_health_wellness_resources()
        all_resources.extend(health_resources)
        
        # 6. 财经投资类资源
        print("\n💰 加载财经投资资源...")
        finance_resources = self.get_finance_investment_resources()
        all_resources.extend(finance_resources)
        
        # 7. 娱乐休闲类资源
        print("\n🎮 加载娱乐休闲资源...")
        entertainment_resources = self.get_entertainment_resources()
        all_resources.extend(entertainment_resources)
        
        # 8. 语言文化类资源
        print("\n🌍 加载语言文化资源...")
        language_resources = self.get_language_culture_resources()
        all_resources.extend(language_resources)
        
        # 9. 工具效率类资源
        print("\n🔧 加载工具效率资源...")
        tool_resources = self.get_tool_productivity_resources()
        all_resources.extend(tool_resources)
        
        # 10. 其他优质资源
        print("\n✨ 加载其他优质资源...")
        other_resources = self.get_other_quality_resources()
        all_resources.extend(other_resources)
        
        # 随机打乱资源顺序
        random.shuffle(all_resources)
        
        # 显示统计
        categories = {}
        for resource in all_resources:
            cat = resource['resource_type']
            categories[cat] = categories.get(cat, 0) + 1
        
        print("\n" + "=" * 60)
        print(f"✅ 资源加载完成！共获得 {len(all_resources)} 个全方位高质量资源")
        print("\n📊 资源分类统计:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {cat}: {count} 个")
        print(f"  其他分类: {len(categories)-10} 个")
        print("=" * 60)
        
        return all_resources

    def get_technology_resources(self):
        """获取技术编程资源"""
        resources = []
        
        tech_links = [
            # 编程语言
            ("Python官方文档", "https://docs.python.org/3/", "Python编程语言官方文档", "编程开发"),
            ("Java官方教程", "https://docs.oracle.com/javase/tutorial/", "Java编程官方教程", "编程开发"),
            ("JavaScript教程", "https://javascript.info/", "现代JavaScript完整教程", "前端开发"),
            ("Go语言之旅", "https://tour.golang.org/", "Go语言交互式教程", "编程开发"),
            ("Rust编程语言", "https://doc.rust-lang.org/book/", "Rust编程语言指南", "编程开发"),
            
            # Web开发
            ("MDN Web开发文档", "https://developer.mozilla.org/zh-CN/", "Web开发权威文档", "Web开发"),
            ("React官方文档", "https://react.dev/", "React前端框架", "前端框架"),
            ("Vue.js官方文档", "https://vuejs.org/guide/", "Vue.js渐进式框架", "前端框架"),
            ("Node.js文档", "https://nodejs.org/en/docs/", "Node.js后端开发", "后端开发"),
            
            # 数据科学
            ("Kaggle学习课程", "https://www.kaggle.com/learn", "数据科学免费课程", "数据科学"),
            ("fast.ai深度学习", "https://www.fast.ai/", "实用深度学习课程", "人工智能"),
            
            # 开发工具
            ("Git官方文档", "https://git-scm.com/doc", "Git版本控制系统", "开发工具"),
            ("Docker入门指南", "https://docs.docker.com/get-started/", "Docker容器技术", "开发工具"),
            ("VS Code文档", "https://code.visualstudio.com/docs", "VS Code编辑器", "开发工具"),
        ]
        
        for title, url, desc, category in tech_links:
            resources.append({
                'title': title,
                'description': desc,
                'url': url,
                'resource_type': category,
                'keywords': f'技术,编程,{category}',
                'created_at': datetime.utcnow()
            })
        
        print(f"✅ 加载 {len(resources)} 个技术编程资源")
        return resources

    def get_academic_resources(self):
        """获取学术学习资源"""
        resources = []
        
        academic_links = [
            # 学术平台
            ("中国大学MOOC", "https://www.icourse163.org/", "国内优质大学课程", "在线教育"),
            ("Coursera平台", "https://www.coursera.org/", "国际在线教育平台", "在线教育"),
            ("edX在线课程", "https://www.edx.org/", "哈佛MIT等名校课程", "在线教育"),
            ("学堂在线", "https://www.xuetangx.com/", "清华大学在线教育", "在线教育"),
            
            # 文献资料
            ("中国知网", "https://www.cnki.net/", "中文学术文献数据库", "学术资源"),
            ("万方数据", "https://www.wanfangdata.com.cn/", "中文学术资源平台", "学术资源"),
            ("Google学术", "https://scholar.google.com/", "全球学术搜索", "学术资源"),
            ("arXiv预印本", "https://arxiv.org/", "科学论文预印本平台", "学术资源"),
            
            # 学习工具
            ("Anki记忆卡片", "https://apps.ankiweb.net/", "间隔重复记忆软件", "学习工具"),
            ("Notion笔记", "https://www.notion.so/", "一体化工作空间", "学习工具"),
            ("Zotero文献管理", "https://www.zotero.org/", "开源文献管理工具", "学术资源"),
            
            # 考试资源
            ("考研帮", "http://www.kaoyan.com/", "考研信息与资源", "考试准备"),
            ("雅思官方网站", "https://www.chinaielts.org/", "雅思考试官方", "语言考试"),
            ("托福官方指南", "https://www.ets.org/toefl", "托福考试资源", "语言考试"),
        ]
        
        for title, url, desc, category in academic_links:
            resources.append({
                'title': title,
                'description': desc,
                'url': url,
                'resource_type': category,
                'keywords': f'学习,学术,{category}',
                'created_at': datetime.utcnow()
            })
        
        print(f"✅ 加载 {len(resources)} 个学术学习资源")
        return resources

    def get_art_creative_resources(self):
        """获取艺术创意资源"""
        resources = []
        
        art_links = [
            # 绘画设计
            ("Procreate教程", "https://procreate.art/learn", "iPad绘画软件教程", "数字绘画"),
            ("Adobe创意云", "https://www.adobe.com/cn/creativecloud.html", "Adobe全套创意软件", "创意设计"),
            ("Figma设计工具", "https://www.figma.com/", "在线UI设计协作工具", "UI设计"),
            ("Canva设计平台", "https://www.canva.com/zh_cn/", "在线平面设计工具", "平面设计"),
            
            # 摄影摄像
            ("500px摄影社区", "https://500px.com.cn/", "高质量摄影作品平台", "摄影艺术"),
            ("Unsplash图库", "https://unsplash.com/", "免费高质量图片", "摄影资源"),
            ("Pexels视频素材", "https://www.pexels.com/zh-cn/videos/", "免费视频素材库", "视频制作"),
            ("V电影", "https://www.vmovier.com/", "优质短片和影视资讯", "影视艺术"),
            
            # 音乐艺术
            ("库客音乐", "https://www.kuke.com/", "古典音乐数字图书馆", "音乐艺术"),
            ("中国古筝网", "https://www.guzheng.cn/", "古筝学习与欣赏", "传统音乐"),
            ("街声StreetVoice", "https://streetvoice.cn/", "独立音乐人平台", "音乐创作"),
            
            # 手工艺
            ("手工客", "https://www.shougongke.com/", "手工艺制作教程", "手工艺"),
            ("豆瓣手工小组", "https://www.douban.com/group/handmade/", "手工爱好者社区", "手工艺"),
            ("编织人生", "https://www.bianzhirensheng.com/", "编织教程与论坛", "手工艺"),
            
            # 书法艺术
            ("书法空间", "http://www.shufakong.com/", "书法学习与欣赏", "书法艺术"),
            ("中国书法网", "http://www.shufa.com/", "书法艺术门户", "书法艺术"),
        ]
        
        for title, url, desc, category in art_links:
            resources.append({
                'title': title,
                'description': desc,
                'url': url,
                'resource_type': category,
                'keywords': f'艺术,创意,{category}',
                'created_at': datetime.utcnow()
            })
        
        print(f"✅ 加载 {len(resources)} 个艺术创意资源")
        return resources

    def get_life_skill_resources(self):
        """获取生活技能资源"""
        resources = []
        
        life_links = [
            # 烹饪美食
            ("下厨房", "https://www.xiachufang.com/", "中文食谱分享平台", "烹饪美食"),
            ("美食杰", "https://www.meishij.net/", "菜谱大全与美食社区", "烹饪美食"),
            ("日日煮", "https://www.daydaycook.com/", "美食视频教程", "烹饪美食"),
            
            # 家居生活
            ("好好住", "https://www.haohaozhu.com/", "家居装修与生活分享", "家居生活"),
            ("一兜糖家居", "https://www.yidoutang.com/", "家居装修灵感", "家居装饰"),
            ("宜家家居指南", "https://www.ikea.cn/cn/zh/", "家居布置与收纳", "家居生活"),
            
            # 园艺种植
            ("踏花行论坛", "http://www.tahua.net/", "花卉种植交流社区", "园艺种植"),
            ("中国园艺网", "http://www.zhongguoyuanyi.net/", "园艺知识与技术", "园艺种植"),
            ("多肉植物百科", "https://www.drlmeng.com/", "多肉植物养护", "植物养护"),
            
            # 手工维修
            ("B站手工区", "https://www.bilibili.com/v/diy/", "各类手工制作视频", "手工制作"),
            ("知乎维修技巧", "https://www.zhihu.com/topic/19551195", "家电维修与保养", "生活维修"),
            
            # 宠物养护
            ("宠物世界", "https://www.petworld.com.cn/", "宠物养护知识", "宠物养护"),
            ("狗民网", "https://www.goumin.com/", "狗狗养护社区", "宠物养护"),
            ("猫研所", "https://www.maoyansuo.com/", "猫咪健康与养护", "宠物养护"),
        ]
        
        for title, url, desc, category in life_links:
            resources.append({
                'title': title,
                'description': desc,
                'url': url,
                'resource_type': category,
                'keywords': f'生活,技能,{category}',
                'created_at': datetime.utcnow()
            })
        
        print(f"✅ 加载 {len(resources)} 个生活技能资源")
        return resources

    def get_health_wellness_resources(self):
        """获取健康养生资源"""
        resources = []
        
        health_links = [
            # 健身运动
            ("Keep健身", "https://www.gotokeep.com/", "健身训练与指导", "健身运动"),
            ("薄荷健康", "https://www.boohee.com/", "健康饮食与减肥", "健康管理"),
            ("每日瑜伽", "https://www.meiriyujia.com/", "瑜伽练习教程", "瑜伽健身"),
            
            # 心理健康
            ("简单心理", "https://www.jiandanxinli.com/", "心理咨询与知识", "心理健康"),
            ("壹心理", "https://www.xinli001.com/", "心理学知识普及", "心理健康"),
            ("KnowYourself", "https://www.ky.com/", "自我认知与成长", "心理成长"),
            
            # 中医养生
            ("中医世家", "http://www.zysj.com.cn/", "中医药知识库", "中医养生"),
            ("39健康养生", "https://yangsheng.39.net/", "中医养生知识", "中医养生"),
            ("中华中医网", "http://www.zhzyw.org/", "中医药综合门户", "中医养生"),
            
            # 饮食营养
            ("中国营养学会", "http://www.cnsoc.org/", "官方营养学指导", "营养健康"),
            ("食话实说", "https://food.sina.com.cn/", "食品安全与营养", "饮食健康"),
            
            # 医疗健康
            ("丁香医生", "https://dxy.com/", "医学健康科普", "医疗健康"),
            ("好大夫在线", "https://www.haodf.com/", "在线医疗咨询", "医疗咨询"),
            ("微医平台", "https://www.guahao.com/", "互联网医疗", "医疗服务"),
        ]
        
        for title, url, desc, category in health_links:
            resources.append({
                'title': title,
                'description': desc,
                'url': url,
                'resource_type': category,
                'keywords': f'健康,养生,{category}',
                'created_at': datetime.utcnow()
            })
        
        print(f"✅ 加载 {len(resources)} 个健康养生资源")
        return resources

    def get_finance_investment_resources(self):
        """获取财经投资资源"""
        resources = []
        
        finance_links = [
            # 投资理财
            ("雪球财经", "https://xueqiu.com/", "投资交流社区", "投资理财"),
            ("东方财富网", "https://www.eastmoney.com/", "财经资讯门户", "财经资讯"),
            ("同花顺", "https://www.10jqka.com.cn/", "股票投资工具", "股票投资"),
            
            # 基金理财
            ("天天基金网", "https://fund.eastmoney.com/", "基金投资平台", "基金理财"),
            ("蛋卷基金", "https://danjuanapp.com/", "智能基金投资", "基金理财"),
            
            # 经济金融
            ("中国人民银行", "http://www.pbc.gov.cn/", "央行政策信息", "金融政策"),
            ("国家统计局", "http://www.stats.gov.cn/", "官方经济数据", "经济数据"),
            ("华尔街见闻", "https://wallstreetcn.com/", "全球财经资讯", "国际财经"),
            
            # 理财教育
            ("长投学堂", "https://www.ichangtou.com/", "理财入门教育", "理财教育"),
            ("简七理财", "https://www.jane7.com/", "理财知识科普", "理财教育"),
            
            # 税务知识
            ("国家税务总局", "http://www.chinatax.gov.cn/", "税收政策法规", "税务知识"),
            ("12366纳税服务", "http://www.12366.cn/", "纳税咨询服务", "税务服务"),
        ]
        
        for title, url, desc, category in finance_links:
            resources.append({
                'title': title,
                'description': desc,
                'url': url,
                'resource_type': category,
                'keywords': f'财经,投资,{category}',
                'created_at': datetime.utcnow()
            })
        
        print(f"✅ 加载 {len(resources)} 个财经投资资源")
        return resources

    def get_entertainment_resources(self):
        """获取娱乐休闲资源"""
        resources = []
        
        entertainment_links = [
            # 影视娱乐
            ("豆瓣电影", "https://movie.douban.com/", "电影评分与影评", "影视娱乐"),
            ("哔哩哔哩", "https://www.bilibili.com/", "视频弹幕网站", "视频娱乐"),
            ("网易云音乐", "https://music.163.com/", "音乐播放与社区", "音乐娱乐"),
            
            # 游戏娱乐
            ("Steam平台", "https://store.steampowered.com/", "游戏发行平台", "游戏娱乐"),
            ("TapTap社区", "https://www.taptap.com/", "手游推荐与社区", "手机游戏"),
            ("游民星空", "https://www.gamersky.com/", "游戏资讯门户", "游戏资讯"),
            
            # 动漫二次元
            ("AcFun弹幕网", "https://www.acfun.cn/", "ACG内容社区", "动漫娱乐"),
            ("半次元", "https://bcy.net/", "二次元创作社区", "动漫创作"),
            
            # 阅读写作
            ("起点中文网", "https://www.qidian.com/", "原创文学网站", "网络文学"),
            ("晋江文学城", "https://www.jjwxc.net/", "女性向文学网站", "网络文学"),
            ("微信读书", "https://weread.qq.com/", "电子书阅读平台", "数字阅读"),
            
            # 旅游休闲
            ("马蜂窝旅游", "https://www.mafengwo.cn/", "旅游攻略社区", "旅游出行"),
            ("携程旅行", "https://www.ctrip.com/", "在线旅游服务", "旅游预订"),
            ("穷游网", "https://www.qyer.com/", "出境游攻略", "境外旅游"),
        ]
        
        for title, url, desc, category in entertainment_links:
            resources.append({
                'title': title,
                'description': desc,
                'url': url,
                'resource_type': category,
                'keywords': f'娱乐,休闲,{category}',
                'created_at': datetime.utcnow()
            })
        
        print(f"✅ 加载 {len(resources)} 个娱乐休闲资源")
        return resources

    def get_language_culture_resources(self):
        """获取语言文化资源"""
        resources = []
        
        language_links = [
            # 语言学习
            ("多邻国", "https://www.duolingo.com/", "免费语言学习App", "语言学习"),
            ("BBC英语学习", "https://www.bbc.co.uk/learningenglish", "BBC官方英语学习", "英语学习"),
            ("沪江网校", "https://class.hujiang.com/", "在线语言学习", "语言培训"),
            
            # 文化历史
            ("故宫博物院", "https://www.dpm.org.cn/", "故宫数字博物馆", "历史文化"),
            ("中国国家博物馆", "http://www.chnmuseum.cn/", "国家博物馆官网", "历史文化"),
            ("中华经典古籍库", "https://www.gujibook.cn/", "古籍数字化平台", "古籍文献"),
            
            # 传统文化
            ("中国非物质文化遗产网", "http://www.ihchina.cn/", "非遗保护与传承", "传统文化"),
            ("中华戏曲网", "http://www.xi-qu.com/", "戏曲艺术资料", "戏曲艺术"),
            ("中国民间文艺网", "http://www.cflac.org.cn/", "民间文艺资源", "民间艺术"),
            
            # 外语学习
            ("TED演讲", "https://www.ted.com/", "思想传播平台", "演讲学习"),
            ("VOA英语学习", "https://learningenglish.voanews.com/", "VOA英语教学", "英语学习"),
            ("NHK日语学习", "https://www.nhk.or.jp/lesson/", "NHK日语课程", "日语学习"),
        ]
        
        for title, url, desc, category in language_links:
            resources.append({
                'title': title,
                'description': desc,
                'url': url,
                'resource_type': category,
                'keywords': f'语言,文化,{category}',
                'created_at': datetime.utcnow()
            })
        
        print(f"✅ 加载 {len(resources)} 个语言文化资源")
        return resources

    def get_tool_productivity_resources(self):
        """获取工具效率资源"""
        resources = []
        
        tool_links = [
            # 办公工具
            ("WPS Office", "https://www.wps.cn/", "办公软件套件", "办公工具"),
            ("石墨文档", "https://shimo.im/", "在线协作文档", "办公协作"),
            ("腾讯文档", "https://docs.qq.com/", "在线文档协作", "办公协作"),
            
            # 效率工具
            ("滴答清单", "https://www.dida365.com/", "任务管理工具", "时间管理"),
            ("番茄TODO", "https://www.fqtodo.cn/", "番茄工作法工具", "时间管理"),
            ("幕布", "https://mubu.com/", "思维导图工具", "思维整理"),
            
            # 在线工具
            ("在线工具大全", "https://tool.lu/", "程序员在线工具", "在线工具"),
            ("ProcessOn", "https://www.processon.com/", "在线流程图工具", "图表工具"),
            ("Canva可画", "https://www.canva.cn/", "在线设计工具", "设计工具"),
            
            # 资源下载
            ("虫部落", "https://search.chongbuluo.com/", "搜索聚合工具", "搜索工具"),
            ("小众软件", "https://www.appinn.com/", "软件推荐网站", "软件资源"),
            ("异次元软件", "https://www.iplaysoft.com/", "软件下载推荐", "软件资源"),
        ]
        
        for title, url, desc, category in tool_links:
            resources.append({
                'title': title,
                'description': desc,
                'url': url,
                'resource_type': category,
                'keywords': f'工具,效率,{category}',
                'created_at': datetime.utcnow()
            })
        
        print(f"✅ 加载 {len(resources)} 个工具效率资源")
        return resources

    def get_other_quality_resources(self):
        """获取其他优质资源"""
        resources = []
        
        other_links = [
            # 新闻资讯
            ("澎湃新闻", "https://www.thepaper.cn/", "时政思想媒体", "新闻资讯"),
            ("虎嗅网", "https://www.huxiu.com/", "商业科技媒体", "商业资讯"),
            ("36氪", "https://36kr.com/", "创业投资媒体", "创业资讯"),
            
            # 社会公益
            ("中国志愿服务网", "https://chinavolunteer.mca.gov.cn/", "官方志愿服务", "社会公益"),
            ("腾讯公益", "https://gongyi.qq.com/", "互联网公益平台", "社会公益"),
            ("支付宝公益", "https://love.alipay.com/", "公益捐赠平台", "社会公益"),
            
            # 环保生活
            ("低碳生活网", "http://www.ditan360.com/", "环保知识分享", "环保生活"),
            ("零废弃生活", "https://www.zerowastehome.com/", "零废弃生活方式", "环保生活"),
            
            # 时尚穿搭
            ("小红书", "https://www.xiaohongshu.com/", "生活方式社区", "时尚生活"),
            ("什么值得买", "https://www.smzdm.com/", "消费决策平台", "购物指南"),
            
            # 亲子教育
            ("宝宝树", "https://www.babytree.com/", "母婴育儿社区", "亲子育儿"),
            ("小花生", "https://www.xiaohuasheng.cn/", "儿童教育分享", "家庭教育"),
        ]
        
        for title, url, desc, category in other_links:
            resources.append({
                'title': title,
                'description': desc,
                'url': url,
                'resource_type': category,
                'keywords': f'生活,资讯,{category}',
                'created_at': datetime.utcnow()
            })
        
        print(f"✅ 加载 {len(resources)} 个其他优质资源")
        return resources
simple_crawler = SimpleResourceCrawler()
