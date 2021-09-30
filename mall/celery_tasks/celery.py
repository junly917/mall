import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proj.settings")

# 定义celery app名称
app = Celery("mall")

# 指定celery任务的配置
app.config_from_object("celery_tasks.config", namespace="CELERY")

# 自动发现celery任务
app.autodiscover_tasks(
    ["celery_tasks.test"]
)


# 手动指定任务
@app.task(bind=True)
def debug_task(self):
    print("debug celery task.")

# 启动任务的方法:
# celery -A celery_tasks.celery worker -l info

# 发送任务
# from celery_tasks.test.tasks import sum
# result = sum.delay(参数1, 参数2)
# result.get()  # 获取任务执行的结果
#
