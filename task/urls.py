from django.urls import path
from . import views

urlpatterns = [
]
import requests, base64
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from dn.models import DnListModel, DnDetailModel
from django.conf import settings
from scanner.models import ListModel as scanner

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
    for i in range(len((dn_list))):
        try:
            res = requests.get('https://api.teapplix.com/api2/Shipment?ReturnLabel=1&TxnId=' + dn_list[i].txnid,
                               headers=headers).json().get('Items', '')
            if len(res) > 0:
                dn_list[i].carrier = res[0].get('TrackingInfo', '').get('CarrierName')
                dn_list[i].trackingnumber = res[0].get('TrackingInfo', '').get('TrackingNumber')
                dn_list[i].mian_dan = res[0].get('LabelData', '').replace(" ", "")
                dn_list[i].have_mian_dan = True
                if CarrierList.objects.filter(
                        carrier=res[0].get('TrackingInfo', '').get('CarrierName')).exists() is False:
                    CarrierList.objects.create(
                        carrier=res[0].get('TrackingInfo', '').get('CarrierName')
                    )
                DnDetailModel.objects.filter(txnid=dn_list[i].txnid).update(
                    carrier=res[0].get('TrackingInfo', '').get('CarrierName'),
                    trackingnumber=res[0].get('TrackingInfo', '').get('TrackingNumber'),
                    mian_dan=res[0].get('LabelData', '').replace(" ", ""),
                    have_mian_dan=True
                )
                dn_list[i].save()
                decoded_data = base64.b64decode(res[0].get('LabelData', '').replace(" ", ""))
                path = str(settings.BASE_DIR) + '/media/miandan/' + str(dn_list[i].txnid) + '.pdf'
                with open(path, 'wb') as file:
                    file.write(decoded_data)
        except:
            pass
        finally:
            pass
    print('订单获取结束')
# per-execution monitoring, call register_events on your scheduler
register_events(scheduler)
# scheduler.start()