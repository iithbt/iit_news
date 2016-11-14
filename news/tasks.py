# from celery.task.schedules import crontab
# from celery.decorators import periodic_task
from celery import shared_task
from celery.utils.log import get_task_logger

from .grab_feed import main

logger = get_task_logger(__name__)


# @periodic_task(
#     run_every=(crontab(minute='*/1')),
#     name="task_grab_feed",
#     ignore_result=True
# )
@shared_task
def task_grab_feed():
    main()
    logger.info("Feed grab complete!")