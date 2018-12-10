#-*-coding:utf-8-*-

from django.http import JsonResponse
from news.models import new,cate
from datetime import datetime

def home(request):
    # ��url�����л��cate
    _cate = request.GET.get("cateid")
    # ����������Ϊ���Ƽ������ߴ��߼�
    if _cate == "1":
        news = getRecNews(_cate)
    # �����������Ȱ�����,����ָ���߼���������
    elif _cate == "2":
        news,news_hot_value = getHotNews()
    # ������������
    else:
        news = new.objects.filter(new_cate=_cate).order_by("-new_time")[:20]
    # ƴ������
    result = dict()
    result["cate_id"] = _cate
    result["cate_name"] = str(cate.objects.get(cate_id=_cate))
    result["news"] = list()
    for one in news:
        result["news"].append({
            "new_id":one.new_id,
            "new_title":str(one.new_title),
            "new_time": one.new_time,
            "new_hot_value": news_hot_value[one.new_id] if _cate == "2" else 0 ,
            "new_content": str(one.new_content[:100])
        })
    return JsonResponse(result)


# �ȶȰ��ȡ���߼������Ȱ���ָ�������ÿ�������ȡtop2���ݣ�����������ݽ������򣬷���
#        �����߼���new_seenum * 0.3 + new_disnum * 0.5 + (new_date-base_data) * 0.2

def getHotNews():
    return_news = dict()
    base_time = datetime.now()
    # ������������ÿ�������µ�top2���� ��ÿƪ���Ŷ�Ӧ���ȶ�ֵ
    all_news_id = list()
    all_news_hot_value = dict()
    # ��ȡ���е����ID
    cate_list =[one.cate_id for one in cate.objects.filter(cate_id__in=("3","4","5","6","7","8","9"))]
    # ����ָ�����������ȡÿ�����͵�top2���ű�����all_new_id��
    for cate_one in cate_list:
        new_one_sorted_dict = dict()
        for new_one in new.objects.filter(new_cate_id=cate_one):
            diff =  base_time - datetime.strptime(str(new_one.new_time.date()), '%Y-%m-%d')
            new_one_sorted_dict[new_one.new_id] = new_one.new_seenum * 0.4 + new_one.new_disnum * 0.5 - diff.days * 0.1
        for one in sorted(new_one_sorted_dict.items(), key=lambda l:l[1], reverse=True)[:2]:
            all_news_id.append(one[0])
            all_news_hot_value[one[0]] = one[1]
    # ����all_news_id��ȡ���ŵľ�����Ϣ
    return new.objects.filter(new_id__in=all_news_id),all_news_hot_value

# Ϊ���Ƽ������� ��ȡ
def getRecNews(_cate):
    news = new.objects.all().order_by("-new_time")[:20]
    return news

