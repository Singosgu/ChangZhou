from django.urls import path
from . import views

urlpatterns = [
]
import requests, base64
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from dn.models import DnListModel
from django.conf import settings

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


# 时间间隔3秒钟打印一次当前的时间
@register_job(scheduler, "interval", seconds=60 * 30, id='task_job', replace_existing=True)
def task_job():
    dn_list = DnListModel.objects.filter(mian_dan='')
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'APItoken': 'e7d82-0913c-5fe10-603c2-be99e-a42e9-a837'
    }
    for i in dn_list:
        try:
            res = requests.get('https://api.teapplix.com/api2/Shipment?ReturnLabel=1&TxnId=' + i.TxnId, headers=headers).json().get('Items', '')[0].get('LabelData', '').replace(" ", "")
            i.mian_dan = res
            i.save()
            decoded_data = base64.b64decode(res)
            with open(str(settings.BASE_DIR) + '/media/miandan/' + str(i.get('TxnId', '')) + '.pdf', 'wb') as file:
                file.write(decoded_data)
        except:
            pass
        finally:
            pass
    print('订单获取结束')
# per-execution monitoring, call register_events on your scheduler
register_events(scheduler)
# scheduler.start()