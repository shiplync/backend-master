from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    # Executes every hour between 8AM and 5PM
    'send-retention-notifications': {
        'task': 'impaqd_server.apps.notifications.tasks.task_send_retention_notifications',
        'schedule': crontab(minute=0, hour='8-17'),
    },
}