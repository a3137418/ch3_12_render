from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import *
from django.forms.models import model_to_dict
from django.utils import timezone
from django.db.models import Sum

def test(request):
    return HttpResponse("Hello world!")
def search_list(request):
    if 'cName' in request.GET:
        cName = request.GET['cName']
        # print(cName)
        # resultObject = students.objects.filter(cName=cName)
        resultObject = students.objects.filter(cName__contains=cName)
    else:
        resultObject = students.objects.all().order_by('-cID')
    # for d in resultObject:
    #     print(model_to_dict(d))
    # return HttpResponse("Hello world!")
    erroermessage=""
    if not resultObject:
        erroermessage = "無此資料"
    return render(request, 'search_list.html',locals())


def search_name(request):
    # return HttpResponse("Hello world!")
    return render(request, 'search_name.html',locals())



from django.db.models import Q
from django.core.paginator import Paginator
def index(request):
    if 'site_search' in request.GET:
        site_search = request.GET['site_search']
        site_search = site_search.strip() #去前後空白
    #     print(site_search)
        #多個關鍵字
        keyworks = site_search.split()#切割字元
        print(keyworks)
        # resultList=[]
        q_objects = Q()
        for keywork in keyworks:
            q_objects.add(Q(cName__contains = keywork),Q.OR)
            q_objects.add(Q(cBirthday__contains = keywork),Q.OR)
            q_objects.add(Q(cEmail__contains = keywork),Q.OR)
            q_objects.add(Q(cPhone__contains = keywork),Q.OR)
            q_objects.add(Q(cAddr__contains = keywork),Q.OR)
        resultList = students.objects.filter(q_objects)



        #一個關鍵字
    #     resultList = students.objects.filter(
    #         Q(cName__contains = site_search)|
    #         Q(cBirthday__contains = site_search)|
    #         Q(cEmail__contains = site_search)|
    #         Q(cPhone__contains = site_search)|
    #         Q(cAddr__contains = site_search)
    #     )
    else:
        resultList  =students.objects.all().order_by("cID")
    # return HttpResponse("Hello world!")
    status = True
    if not resultList:
        errormessage = "無此資料"
        status = False

    data_count = len(resultList )
    # print(data_count)
    # for d in resultList :
    #     print(model_to_dict(d))
    # page_obj 是一個包含該頁資料的物件
    # page_obj.object_list：該頁的資料
    # page_obj.has_next、page_obj.has_previous：是否有下一頁或上一頁
    # page_obj.next_page_number、page_obj.previous_page_number：下一頁或上一頁的頁碼
    # page_obj.number：目前頁碼
    # page_obj.paginator.num_pages：總頁數
    # page_obj.paginator.page_range：表示所有可用的頁碼（從 1 開始）
    #分頁設定，每頁顯示3筆
    paginator = Paginator(resultList,3)
    # ?page=1
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # print(dir(page_obj))

    return render(request,"index.html",locals())


########################新增##############################
from django.shortcuts import redirect
def post(request):
    if request.method == "POST":
        cName = request.POST["cName"]
        cSex = request.POST["cSex"]
        cBirthday = request.POST["cBirthday"]
        cEmail = request.POST["cEmail"]
        cPhone = request.POST["cPhone"]
        cAddr = request.POST["cAddr"]
        print(f"cName={cName},cSex={cSex},cBirthday={cBirthday},cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
        # return HttpResponse("資料已新增")
        add = students(cName =cName,cSex=cSex,cBirthday=cBirthday,cEmail=cEmail,cPhone=cPhone,cAddr=cAddr)
        add.save()
        return redirect("/index/")
    else:
        return render(request,"post.html",locals())
    
########################修改##############################

def edit(request,id):
    if request.method == "POST":
        print(id)
        cName = request.POST["cName"]
        cSex = request.POST["cSex"]
        cBirthday = request.POST["cBirthday"]
        cEmail = request.POST["cEmail"]
        cPhone = request.POST["cPhone"]
        cAddr = request.POST["cAddr"]
        print(f"cName={cName},cSex={cSex},cBirthday={cBirthday},cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
        # return HttpResponse("資料已修改")
        updata = students.objects.get(cID=id)
        updata.cName = cName
        updata.cSex = cSex
        updata.cBirthday = cBirthday
        updata.cEmail = cEmail
        updata.cPhone = cPhone
        updata.cAddr = cAddr
        updata.save()
        return redirect("/index/")
    
    
    # print(id)
    obj_data = students.objects.get(cID=id)
    print(model_to_dict(obj_data))

    # return HttpResponse("hello")
    return render(request,"edit.html",locals())
########################刪除##############################
def delete(request,id):
    print(id)
    obj_data = students.objects.get(cID=id)
    print(model_to_dict)

    if request.method == "POST":
        obj_data.delete()
        return redirect('/index/')

    return render(request,"delete.html",locals())