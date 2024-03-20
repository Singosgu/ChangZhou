from django.urls import path
from . import views

urlpatterns = [
]
import requests, base64
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from warehouse.models import ListModel
from django.conf import settings

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


# 时间间隔3秒钟打印一次当前的时间
@register_job(scheduler, "interval", seconds=10000, id='task_job', replace_existing=True)
def task_job():
    warehouse_list = [20, 25]
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'APItoken': 'e7d82-0913c-5fe10-603c2-be99e-a42e9-a837'
    }
    for k in warehouse_list:
        get_orders = requests.get('https://api.teapplix.com/api2/OrderNotification?NotShipped=1&PageSize=100&WarehouseId=' + str(k), headers=headers).json()
        for j in range(get_orders.get('Pagination', '').get('TotalPages', '')):
            get_order = requests.get(
                'https://api.teapplix.com/api2/OrderNotification?NotShipped=1&PageSize=100&PageNumber=' + str(j + 1) + '&WarehouseId=' + str(k),
                headers=headers).json().get('Orders')
            for i in get_order:
                print('仓库id：' + str(i.get('OrderDetails', '').get('WarehouseId', '')), '单号：' + i.get('TxnId', ''))
                try:
                    res = requests.get('https://api.teapplix.com/api2/Shipment?ReturnLabel=1&TxnId=' + i.get('TxnId', ''), headers=headers).json().get('Items', '')[0].get('LabelData', '').replace(" ", "")
                    decoded_data = base64.b64decode(res)
                    with open(str(settings.BASE_DIR) + '/' + str(i.get('TxnId', '')) + '.pdf', 'wb') as file:
                        file.write(decoded_data)
                except:
                    pass
                finally:
                    pass
    print('订单获取结束')
# per-execution monitoring, call register_events on your scheduler
register_events(scheduler)
# scheduler.start()