import asyncio
from datetime import datetime, timedelta
from sqlalchemy import select
from models import engine, Base, Message, Assignment, StudentAssignment
from models import AsyncSessionFactory

async def create_test_messages():
    """创建一些测试消息"""
    async with AsyncSessionFactory() as session:
        # 先找一个作业
        result = await session.execute(select(Assignment).limit(1))
        assignment = result.scalar_one_or_none()
        
        if not assignment:
            print("没有找到作业，请先创建一个作业")
            return
        
        assignment_id = assignment.assignment_id
        student_ids = [1, 2, 3]  # 假设有这几个学生
        
        # 为每个学生创建一些测试消息
        now = datetime.now()
        
        # 消息1：作业截止通知（刚创建）
        for sid in student_ids:
            msg1 = Message(
                student_id=sid,
                assignment_id=assignment_id,
                content=f"作业「{assignment.assignment_title}」已截止，请查看批改结果",
                type="assignment_deadline",
                is_read=False,
                created_at=now
            )
            session.add(msg1)
        
        # 消息2：作业提醒（1小时前）
        for sid in student_ids:
            msg2 = Message(
                student_id=sid,
                assignment_id=assignment_id,
                content=f"作业「{assignment.assignment_title}」将在今天截止，请尽快完成",
                type="homework_reminder",
                is_read=False,
                created_at=now - timedelta(hours=1)
            )
            session.add(msg2)
        
        # 消息3：课程变动通知（昨天）
        for sid in student_ids:
            msg3 = Message(
                student_id=sid,
                assignment_id=assignment_id,
                content="明天的计算机网络课程改至 302 教室，请同学们带好教材准时参加",
                type="course_change",
                is_read=True,
                created_at=now - timedelta(days=1)
            )
            session.add(msg3)
        
        # 消息4：系统更新（3天前）
        for sid in student_ids:
            msg4 = Message(
                student_id=sid,
                assignment_id=assignment_id,
                content="智能课程助手 V1.2 版本已发布，修复了已知的问题",
                type="system_update",
                is_read=True,
                created_at=now - timedelta(days=3)
            )
            session.add(msg4)
        
        await session.commit()
        print(f"已为学生 {student_ids} 创建测试消息，作业ID: {assignment_id}")

if __name__ == "__main__":
    asyncio.run(create_test_messages())
