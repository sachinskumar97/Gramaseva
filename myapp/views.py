from django.shortcuts import render
import sys



# Create your views here.


from django.http import HttpResponse
from django.db.models import Max
from .models import user_login

from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
import razorpay

#from django.db.models import Sum

def index(request):
    return render(request, './myapp/index.html')


def about(request):
    return render(request, './myapp/about.html')


def contact(request):
    return render(request, './myapp/contact.html')


##########Ajax Pages##############
from .models import district_settings
def district_list_view(request):
    state_id = int(request.GET.get('state_id'))
    print('state_id',state_id)
    d_l = district_settings.objects.filter(state_id=state_id)
    context = {'state_id':state_id,'district_list':d_l}
    return render(request, './myapp/district_list_view.html',context)

from .models import block_settings
def block_list_view(request):
    district_id = int(request.GET.get('district_id'))
    print('district_id',district_id)
    b_l = block_settings.objects.filter(district_id=district_id)
    context = {'district_id':district_id,'block_list':b_l}
    return render(request, './myapp/block_list_view.html',context)

from .models import panchayat_settings
def panchayat_list_view(request):
    block_id = int(request.GET.get('block_id'))
    print('block_id',block_id)
    p_l = panchayat_settings.objects.filter(block_id=block_id)
    context = {'block_id':block_id,'panchayat_list':p_l}
    return render(request, './myapp/panchayat_list_view.html',context)

############# ADMIN #######################
def admin_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pwd = request.POST.get('pwd')
        #print(un,pwd)
        #query to select a record based on a condition
        ul = user_login.objects.filter(uname=un, passwd=pwd, u_type='admin')

        if len(ul) == 1:
            request.session['user_name'] = ul[0].uname
            request.session['user_id'] = ul[0].id
            return render(request,'./myapp/admin_home.html')
        else:
            msg = '<h1> Invalid Uname or Password !!!</h1>'
            context ={ 'msg1':msg }
            return render(request, './myapp/admin_login.html',context)
    else:
        msg = ''
        context ={ 'msg1':msg }
        return render(request, './myapp/admin_login.html',context)


def admin_home(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)
    else:
        return render(request,'./myapp/admin_home.html')


def admin_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return admin_login(request)
    else:
        return admin_login(request)

def admin_changepassword(request):
    if request.method == 'POST':
        opasswd = request.POST.get('opasswd')
        npasswd = request.POST.get('npasswd')
        cpasswd = request.POST.get('cpasswd')
        uname = request.session['user_name']
        try:
            ul = user_login.objects.get(uname=uname,passwd=opasswd,u_type='admin')
            if ul is not None:
                ul.passwd=npasswd
                ul.save()
                context = {'msg': 'Password Changed'}
                return render(request, './myapp/admin_changepassword.html', context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/admin_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Err Not Changed'}
            return render(request, './myapp/admin_changepassword.html', context)
    else:
        context = {'msg': ''}
        return render(request, './myapp/admin_changepassword.html', context)

from .models import state_settings
def admin_state_settings_add(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    if request.method == 'POST':

        state_name = request.POST.get('state_name')
        state_code = request.POST.get('state_code')
        try:
            sd = state_settings(state_name=state_name, state_code=state_code)
            sd.save()
            context = {'msg': 'Record Added'}
            return render(request, './myapp/admin_state_settings_add.html', context)
        except:
            context = {'msg': 'Record Adding Failed'}
            return render(request, './myapp/admin_state_settings_add.html', context)
    else:
        return render(request, './myapp/admin_state_settings_add.html')

def admin_state_settings_edit(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    if request.method == 'POST':
        s_id = request.POST.get('s_id')
        state_name = request.POST.get('state_name')
        state_code = request.POST.get('state_code')

        sd = state_settings.objects.get(id=int(s_id))

        sd.state_name = state_name
        sd.state_code = state_code
        sd.save()
        msg = 'Record Updated'
        sd_l = state_settings.objects.all()
        context = {'state_list': sd_l, 'msg': msg}
        return render(request, './myapp/admin_state_settings_view.html', context)
    else:
        id = request.GET.get('id')
        sd = state_settings.objects.get(id=int(id))
        context = {'state_name':sd.state_name,'state_code':sd.state_code,'s_id':sd.id}
        return render(request, './myapp/admin_state_settings_edit.html',context)

def admin_state_settings_delete(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    id = request.GET.get('id')
    print('id = '+id)
    sd = state_settings.objects.get(id=int(id))
    sd.delete()
    msg = 'Record Deleted'
    sd_l = state_settings.objects.all()
    context = {'state_list': sd_l,'msg':msg}
    return render(request, './myapp/admin_state_settings_view.html',context)

def admin_state_settings_view(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    sd_l = state_settings.objects.all()
    context = {'state_list':sd_l}
    return render(request, './myapp/admin_state_settings_view.html',context)

from .models import district_settings
def admin_district_settings_add(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    if request.method == 'POST':
        state_id = int(request.POST.get('state_id'))
        district_name = request.POST.get('district_name')
        district_code = request.POST.get('district_code')

        dd = district_settings(state_id=state_id, district_name=district_name, district_code=district_code)
        dd.save()
        context = {'state_id':state_id,'msg': 'Record Added'}
        return render(request, './myapp/admin_district_settings_add.html', context)
    else:
        state_id = int(request.GET.get('state_id'))
        context = {'state_id': state_id, 'msg': ''}
        return render(request, './myapp/admin_district_settings_add.html', context)

def admin_district_settings_edit(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    if request.method == 'POST':
        s_id = request.POST.get('s_id')
        state_id = int(request.POST.get('state_id'))
        district_name = request.POST.get('district_name')
        district_code = request.POST.get('district_code')

        dd = district_settings.objects.get(id=int(s_id))

        dd.district_name = district_name
        dd.district_code = district_code
        dd.save()
        msg = 'Record Updated'
        dd_l = district_settings.objects.all()
        context = {'district_list': dd_l, 'msg': msg,'state_id': state_id}
        return render(request, './myapp/admin_district_settings_view.html', context)
    else:
        id = request.GET.get('id')
        state_id = int(request.GET.get('state_id'))
        dd = district_settings.objects.get(id=int(id))
        context = {'district_name':dd.district_name,'district_code':dd.district_code,
                   's_id':dd.id,'state_id': state_id}
        return render(request, './myapp/admin_district_settings_edit.html',context)

def admin_district_settings_delete(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    id = request.GET.get('id')
    print('id = '+id)
    state_id = int(request.GET.get('state_id'))
    dd = district_settings.objects.get(id=int(id))
    dd.delete()
    msg = 'Record Deleted'
    dd_l = district_settings.objects.filter(state_id=state_id)
    context = {'district_list': dd_l,'msg':msg,'state_id': state_id}
    return render(request, './myapp/admin_district_settings_view.html',context)

def admin_district_settings_view(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)
    state_id = int(request.GET.get('state_id'))
    dd_l = district_settings.objects.filter(state_id=state_id)
    context = {'district_list':dd_l,'state_id': state_id}
    return render(request, './myapp/admin_district_settings_view.html',context)

from .models import block_settings
def admin_block_settings_add(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    if request.method == 'POST':
        district_id = int(request.POST.get('district_id'))
        block_name = request.POST.get('block_name')
        block_code = request.POST.get('block_code')

        bd = block_settings(district_id=district_id, block_name=block_name, block_code=block_code)
        bd.save()
        context = {'district_id':district_id,'msg': 'Record Added'}
        return render(request, './myapp/admin_block_settings_add.html', context)
    else:
        district_id = int(request.GET.get('district_id'))
        context = {'district_id': district_id, 'msg': ''}
        return render(request, './myapp/admin_block_settings_add.html', context)

def admin_block_settings_edit(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    if request.method == 'POST':
        s_id = request.POST.get('s_id')
        district_id = int(request.POST.get('district_id'))
        block_name = request.POST.get('block_name')
        block_code = request.POST.get('block_code')

        bd = block_settings.objects.get(id=int(s_id))

        bd.block_name = block_name
        bd.block_code = block_code
        bd.save()
        msg = 'Record Updated'
        bd_l = block_settings.objects.filter(district_id=district_id)
        context = {'block_list': bd_l, 'msg': msg,'district_id': district_id}
        return render(request, './myapp/admin_block_settings_view.html', context)
    else:
        id = request.GET.get('id')
        district_id = int(request.GET.get('district_id'))
        bd = block_settings.objects.get(id=int(id))
        context = {'block_name':bd.block_name,'block_code':bd.block_code,
                   's_id':bd.id,'district_id': district_id}
        return render(request, './myapp/admin_block_settings_edit.html',context)

def admin_block_settings_delete(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    id = request.GET.get('id')
    print('id = '+id)
    district_id = int(request.GET.get('district_id'))
    bd = block_settings.objects.get(id=int(id))
    bd.delete()
    msg = 'Record Deleted'
    bd_l = block_settings.objects.filter(district_id=district_id)
    context = {'block_list': bd_l,'msg':msg,'district_id': district_id}
    return render(request, './myapp/admin_block_settings_view.html',context)

def admin_block_settings_view(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)
    district_id = int(request.GET.get('district_id'))
    bd_l = block_settings.objects.filter(district_id=district_id)
    context = {'block_list':bd_l,'district_id': district_id}
    return render(request, './myapp/admin_block_settings_view.html',context)

from .models import panchayat_settings
def admin_panchayat_settings_add(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    if request.method == 'POST':

        block_id = int(request.POST.get('block_id'))
        panchayat_name = request.POST.get('panchayat_name')
        panchayat_code = request.POST.get('panchayat_code')
        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        pre_name = request.POST.get('pre_name')
        pre_contact = request.POST.get('pre_contact')
        pre_email = request.POST.get('pre_email')
        sec_name = request.POST.get('sec_name')
        sec_contact = request.POST.get('sec_contact')
        sec_email = request.POST.get('sec_email')
        ward_count = request.POST.get('ward_count')
        status = 'ok'
        uname = panchayat_code
        password ='1234'
        ul = user_login(uname=uname, passwd=password, u_type='panchayat')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        pd = panchayat_settings(block_id=block_id,user_id=user_id,panchayat_name=panchayat_name,
                                panchayat_code=panchayat_code,addr=addr,pin=pin,pre_name=pre_name,
                                pre_contact=pre_contact,pre_email=pre_email,sec_name=sec_name,
                                sec_contact=sec_contact,sec_email=sec_email,ward_count=ward_count,
                                status=status)
        pd.save()
        context = {'block_id':block_id,'msg': 'Record Added'}
        return render(request, './myapp/admin_panchayat_settings_add.html', context)
    else:
        block_id = int(request.GET.get('block_id'))
        context = {'block_id': block_id, 'msg': ''}
        return render(request, './myapp/admin_panchayat_settings_add.html', context)


def admin_panchayat_settings_add2(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    if request.method == 'POST':

        state_id = int(request.POST.get('state_id'))
        district_id = int(request.POST.get('district_id'))
        block_id = int(request.POST.get('block_id'))
        panchayat_name = request.POST.get('panchayat_name')
        panchayat_code = request.POST.get('panchayat_code')
        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        pre_name = request.POST.get('pre_name')
        pre_contact = request.POST.get('pre_contact')
        pre_email = request.POST.get('pre_email')
        sec_name = request.POST.get('sec_name')
        sec_contact = request.POST.get('sec_contact')
        sec_email = request.POST.get('sec_email')
        ward_count = request.POST.get('ward_count')
        status = 'ok'
        uname = panchayat_code
        password ='1234'
        ul = user_login(uname=uname, passwd=password, u_type='panchayat')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        pd = panchayat_settings(block_id=block_id,user_id=user_id,panchayat_name=panchayat_name,
                                panchayat_code=panchayat_code,addr=addr,pin=pin,pre_name=pre_name,
                                pre_contact=pre_contact,pre_email=pre_email,sec_name=sec_name,
                                sec_contact=sec_contact,sec_email=sec_email,ward_count=ward_count,
                                status=status)
        pd.save()
        sd = state_settings.objects.all()
        context = {'state_list':sd,'msg': 'Record Added'}
        return render(request, './myapp/admin_panchayat_settings_add2.html', context)
    else:
        sd = state_settings.objects.all()
        context = {'state_list': sd, 'msg': ''}
        return render(request, './myapp/admin_panchayat_settings_add2.html', context)

def admin_panchayat_settings_edit(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    if request.method == 'POST':
        s_id = request.POST.get('s_id')
        block_id = int(request.POST.get('block_id'))
        panchayat_name = request.POST.get('panchayat_name')
        panchayat_code = request.POST.get('panchayat_code')
        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        pre_name = request.POST.get('pre_name')
        pre_contact = request.POST.get('pre_contact')
        pre_email = request.POST.get('pre_email')
        sec_name = request.POST.get('sec_name')
        sec_contact = request.POST.get('sec_contact')
        sec_email = request.POST.get('sec_email')
        ward_count = request.POST.get('ward_count')

        pd = panchayat_settings.objects.get(id=int(s_id))

        pd.panchayat_name = panchayat_name
        pd.panchayat_code = panchayat_code
        pd.addr = addr
        pd.pin = pin
        pd.pre_name = pre_name
        pd.pre_contact = pre_contact
        pd.pre_email = pre_email
        pd.sec_name = sec_name
        pd.sec_contact = sec_contact
        pd.sec_email = sec_email
        pd.ward_count = ward_count

        pd.save()
        msg = 'Record Updated'
        pd_l = panchayat_settings.objects.filter(block_id=block_id)
        context = {'panchayat_list': pd_l, 'msg': msg,'block_id': block_id}
        return render(request, './myapp/admin_panchayat_settings_view.html', context)
    else:
        id = request.GET.get('id')
        block_id = int(request.GET.get('block_id'))
        pd = panchayat_settings.objects.get(id=int(id))
        context = {'pd':pd,'s_id':pd.id,'block_id': block_id}
        return render(request, './myapp/admin_panchayat_settings_edit.html',context)

def admin_panchayat_settings_delete(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    id = request.GET.get('id')
    print('id = '+id)
    block_id = int(request.GET.get('block_id'))

    pd = panchayat_settings.objects.get(id=int(id))
    ul = user_login.objects.get(user_id = pd.user_id)
    ul.delete()
    pd.delete()
    msg = 'Record Deleted'
    pd_l = panchayat_settings.objects.filter(block_id=block_id)
    context = {'panchayat_list': pd_l,'msg':msg,'block_id': block_id}
    return render(request, './myapp/admin_panchayat_settings_view.html',context)

def admin_panchayat_settings_view(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)
    block_id = int(request.GET.get('block_id'))
    pd_l = panchayat_settings.objects.filter(block_id=block_id)
    context = {'panchayat_list':pd_l,'block_id': block_id}
    return render(request, './myapp/admin_panchayat_settings_view.html',context)



############## Public User ####################
from .models import user_details

def user_login_check(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        passwd = request.POST.get('passwd')

        ul = user_login.objects.filter(uname=uname, passwd=passwd, u_type='user')
        print(len(ul))
        if len(ul) == 1:
            request.session['user_id'] = ul[0].id
            request.session['user_name'] = ul[0].uname
            context = {'uname': request.session['user_name']}
            #send_mail('Login','welcome'+uname,uname)
            return render(request, 'myapp/user_home.html',context)
        else:
            context = {'msg': 'Invalid Credentials'}
            return render(request, 'myapp/user_login.html',context)
    else:
        return render(request, 'myapp/user_login.html')

def user_home(request):

    context = {'uname':request.session['user_name']}
    return render(request,'./myapp/user_home.html',context)
    #send_mail("heoo", "hai", 'snehadavisk@gmail.com')

def user_details_add(request):
    if request.method == 'POST':

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        email = request.POST.get('email')
        contact = request.POST.get('contact')

        panchayat_id = int(request.POST.get('panchayat_id'))
        house_no = request.POST.get('house_no')
        ward_no = request.POST.get('ward_no')
        district_id = int(request.POST.get('district_id'))
        state_id = int(request.POST.get('state_id'))
        aadhaar_no = request.POST.get('aadhaar_no')


        password = request.POST.get('pwd')
        uname=email
        #status = "new"

        ul = user_login(uname=uname, passwd=password, u_type='user')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        ud = user_details(user_id=user_id,fname=fname, lname=lname, gender=gender, dob=dob,addr=addr, pin=pin,
                          panchayat_id=panchayat_id,house_no=house_no,ward_no=ward_no,district_id=district_id,
                          state_id=state_id,aadhaar_no=aadhaar_no,
                          contact=contact, email=email,status='new' )
        ud.save()

        print(user_id)
        context = {'msg': 'User Registered'}
        return render(request, 'myapp/user_login.html',context)

    else:
        sd = state_settings.objects.all()
        context = {'state_list': sd, 'msg': ''}
        return render(request, 'myapp/user_details_add.html',context)

def user_details_edit(request):
    if request.method == 'POST':

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        email = request.POST.get('email')
        contact = request.POST.get('contact')



        user_id = int(request.session['user_id'])

        ud = user_details.objects.get(user_id=user_id)
        ud.fname = fname
        ud.lname = lname
        ud.gender = gender
        ud.dob = dob
        ud.addr = addr
        ud.pin = pin
        ud.contact = contact
        ud.email = email
        ud.save()

        print(user_id)
        context = {'msg': 'User Details Updated','ud':ud}
        return render(request, 'myapp/user_details_edit.html',context)

    else:
        user_id = int(request.session['user_id'])

        ud = user_details.objects.get(user_id=user_id)

        context = {'ud': ud, 'msg': ''}
        return render(request, 'myapp/user_details_edit.html',context)


def user_changepassword(request):
    if request.method == 'POST':
        uname = request.session['user_name']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print("username:::" + uname)
        print("current_password" + str(current_password))

        try:

            ul = user_login.objects.get(uname=uname, passwd=current_password)

            if ul is not None:
                ul.passwd = new_password  # change field
                ul.save()
                context = {'msg':'Password Changed Successfully'}
                return render(request, './myapp/user_changepassword.html',context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/user_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Not Changed'}
            return render(request, './myapp/user_changepassword.html', context)
    else:
        return render(request, './myapp/user_changepassword.html')



def user_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return user_login_check(request)
    else:
        return user_login_check(request)


def user_ward_news_view(request):
    user_id = request.session['user_id']
    ud = user_details.objects.get(user_id=int(user_id))
    ward_no = ud.ward_no
    dt = datetime.today().strftime('%Y-%m-%d')
    wn_l = ward_news.objects.filter(ward_no=ward_no,dt=dt)
    msg =''
    if len(wn_l) == 0:
        msg = 'no news'
    context = {'news_list': wn_l, 'msg': msg}
    return render(request, 'myapp/user_ward_news_view.html', context)

def user_ward_covid_view(request):
    user_id = request.session['user_id']
    ud = user_details.objects.get(user_id=int(user_id))
    ward_no = ud.ward_no
    wn_l = ward_covid.objects.filter(ward_no=ward_no)
    msg =''
    if len(wn_l) == 0:
        msg = 'no data'
    context = {'covid_list': wn_l, 'msg': msg}
    return render(request, 'myapp/user_ward_covid_view.html', context)

def user_panchayat_news_view(request):
    user_id = request.session['user_id']
    ud = user_details.objects.get(user_id=int(user_id))
    dt = datetime.today().strftime('%Y-%m-%d')
    pm_l = panchayat_news.objects.filter(panchayat_id=ud.panchayat_id,dt=dt)
    msg =''
    if len(pm_l) == 0:
        msg = 'no news'
    context = {'news_list': pm_l, 'msg': msg}
    return render(request, 'myapp/user_panchayat_news_view.html', context)

def user_ward_member_search(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return user_login_check(request)

    if request.method == 'POST':
        ward_no = request.POST.get('query')
        user_id = request.session['user_id']
        ud = user_details.objects.get(user_id=int(user_id))
        panchayat_id = ud.panchayat_id

        msg = ''
        md_l = ward_member_details.objects.filter(panchayat_id=panchayat_id,ward_no__contains=ward_no)
        context = {'member_list': md_l, 'msg': msg}
        return render(request, './myapp/user_ward_member_result.html', context)
    else:
        return render(request, './myapp/user_ward_member_search.html')

from .models import panchayat_user_messages
def user_panchayat_messages_add(request):
    if request.method == 'POST':

        user_id = request.session['user_id']
        title = request.POST.get('title')
        message = request.POST.get('message')
        remarks = 'no remarks'
        rdt = ''
        rtm = ''
        status = ''

        ud = user_details.objects.get(user_id=int(request.session['user_id']))
        panchayat_id = ud.panchayat_id

        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')


        pm = panchayat_user_messages(panchayat_id=panchayat_id,user_id=user_id,title=title,
                                     message=message,remarks=remarks,dt=dt,tm=tm,rdt=rdt,
                                     rtm=rtm,status=status)
        pm.save()

        context = {'msg':'Record added'}
        return render(request, 'myapp/user_panchayat_messages_add.html',context)

    else:
        context = {'msg':''}
        return render(request, 'myapp/user_panchayat_messages_add.html',context)

def user_panchayat_messages_delete(request):
    id = request.GET.get('id')
    print("id="+id)

    pm = panchayat_user_messages.objects.get(id=int(id))
    pm.delete()

    user_id = request.session['user_id']

    pm_l = panchayat_user_messages.objects.filter(user_id=int(user_id))


    context ={'message_list': pm_l,'msg':'Record deleted'}
    return render(request,'myapp/user_panchayat_messages_view.html',context)

def user_panchayat_messages_view(request):
    user_id = request.session['user_id']
    ud = user_details.objects.get(user_id=int(user_id))
    pm_l = panchayat_user_messages.objects.filter(user_id=int(user_id),panchayat_id=ud.panchayat_id)
    msg =''
    if len(pm_l) ==0:
        msg = 'No Messages'
    context = {'message_list': pm_l, 'msg': msg}
    return render(request, 'myapp/user_panchayat_messages_view.html', context)

from .models import licence_request
def user_licence_request_add(request):
    if request.method == 'POST':

        user_id = request.session['user_id']
        title = request.POST.get('title')
        descp = request.POST.get('descp')

        status = 'Pending'

        ud = user_details.objects.get(user_id=int(request.session['user_id']))
        panchayat_id = ud.panchayat_id

        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        u_file = request.FILES['document']
        fs = FileSystemStorage()
        image = fs.save(u_file.name, u_file)


        pm = licence_request(panchayat_id=panchayat_id,user_id=user_id,title=title,image=image,
                                     descp=descp,dt=dt,tm=tm,
                                     status=status)
        pm.save()

        context = {'msg':'Record added'}
        return render(request, 'myapp/user_licence_request_add.html',context)

    else:
        context = {'msg':''}
        return render(request, 'myapp/user_licence_request_add.html',context)

def user_licence_request_delete(request):
    id = request.GET.get('id')
    print("id="+id)

    pm = licence_request.objects.get(id=int(id))
    pm.delete()

    user_id = request.session['user_id']

    pm_l = licence_request.objects.filter(user_id=int(user_id))


    context ={'licence_list': pm_l,'msg':'Record deleted'}
    return render(request,'myapp/user_licence_request_view.html',context)

def user_licence_request_view(request):
    user_id = request.session['user_id']
    ud = user_details.objects.get(user_id=int(user_id))
    pm_l = licence_request.objects.filter(user_id=int(user_id),panchayat_id=ud.panchayat_id)
    msg =''
    if len(pm_l) ==0:
        msg = 'No Request'
    context = {'licence_list': pm_l, 'msg': msg}
    return render(request, 'myapp/user_licence_request_view.html', context)

from .models import taxcollection
def user_tax_add(request):


    if request.method == 'POST':

        user_id = request.session['user_id']
        houseno = request.POST.get('houseno')
        amount = 0
        # cardno = request.POST.get('cardno')
        # cvv = request.POST.get('cvv')




        ud = user_details.objects.get(user_id=int(request.session['user_id']))
        panchayat_id = ud.panchayat_id

        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        status = 'Verifying'



        pm = taxcollection(panchayat_id=panchayat_id,user_id=user_id,houseno=houseno,amount=amount
                                    ,dt=dt,tm=tm,status=status)

        pm.save()

        context = {'msg':'Record added'}
        return render(request, 'myapp/user_tax_add.html',context)

    else:
        context = {'msg':''}
        return render(request, 'myapp/user_tax_add.html',context)



def admin_tax_verify(request):
    if request.method == 'POST':
        req_id = request.POST.get('id')
        req_status = request.POST.get('status')
        amount = request.POST.get('amount')
        user_id = request.session['user_id']

        try:
            ul = taxcollection.objects.get(id=int(req_id))
            if ul is not None:
                ul.amount = amount
                ul.status = req_status
                ul.dt = datetime.today().strftime('%Y-%m-%d')
                ul.tm = datetime.today().strftime('%H:%M:%S')
                ul.save()
                pd = panchayat_settings.objects.get(user_id=int(user_id))
                ud_l = user_details.objects.all()
                pm_l = taxcollection.objects.filter(panchayat_id=pd.id)
                msg = 'Status and Amount Changed'
                if len(pm_l) == 0:
                    msg = 'No data'
                context = {'tax_list': pm_l, 'user_list': ud_l, 'msg': msg}
                return render(request, './myapp/panchayat_user_tax_view.html', context)
            else:
                context = {'msg': 'Status,Amount Not Changed'}
                return render(request, './myapp/panchayat_user_tax_view.html', context)
        except taxcollection.DoesNotExist:
            context = {'msg': 'Status,Amount err Not Changed'}
            return render(request, './myapp/panchayat_user_tax_view.html', context)
    else:
        context = {'msg': ''}
        return render(request, './myapp/panchayat_user_tax_view.html', context)


def user_tax_view(request):
    user_id = request.session['user_id']
    ud = user_details.objects.get(user_id=int(user_id))
    pm_l = taxcollection.objects.filter(user_id=int(user_id),panchayat_id=ud.panchayat_id)
    msg =''

    if len(pm_l) ==0:
        msg = 'No Data'
    context = {'tax_list': pm_l, 'msg': msg}
    return render(request, 'myapp/user_tax_view.html', context)

def user_tax_pay(request):
    if request.method == "POST":
        try:
            req_id = request.POST.get('tax_id')
            ul = taxcollection.objects.get(id=int(req_id))
            if ul is not None:
                client = razorpay.Client(auth=('rzp_test_Orw0H2W0Ob0xnO', 'OsiVPH2GZRsBc4yKgqJMBhLm'))
                order_amount = int(ul.amount)*100
                order_currency = 'INR'
                payment_order = client.order.create(dict(amount=order_amount, currency=order_currency, payment_capture=1))

                payment_order_id = payment_order['id']
                context = {
                    'amt': order_amount, 'api_key': 'rzp_test_Orw0H2W0Ob0xnO', 'order_id': payment_order_id, 'product': ul
                }
                return render(request, './myapp/user_tax_pay.html', context)
            else:
                context = {'msg': 'Status,Amount Not Changed'}
                return render(request, 'myapp/base.html', {'msg': 'No Data'})
        except taxcollection.DoesNotExist:
            return render(request, 'myapp/base.html', {'msg': 'No Data'})
    else:

        return render(request, 'myapp/base.html', {'msg': 'No Data'})

def user_tax_payment(request):
    if request.method == 'POST':
        req_id = request.POST.get('tax_id')
        req_status = request.POST.get('status')
        user_id = request.session['user_id']

        try:

            ul = taxcollection.objects.get(id=int(req_id))
            ul.status = req_status
            ul.dt = datetime.today().strftime('%Y-%m-%d')
            ul.tm = datetime.today().strftime('%H:%M:%S')
            ul.save()
            ud = user_details.objects.get(user_id=int(user_id))
            pm_l = taxcollection.objects.filter(user_id=int(user_id), panchayat_id=ud.panchayat_id)
            context = {'tax_list': pm_l,  'msg': ""}
            return render(request, './myapp/user_tax_view.html', context)
        except taxcollection.DoesNotExist:
            context = {'msg': 'Status,Amount err Not Changed'}
            return render(request, './myapp/base.html', context)
    else:
        context = {'msg': ''}
        return render(request, './myapp/base.html', context)

from .models import ward_user_messages
def user_ward_messages_add(request):
    if request.method == 'POST':

        user_id = request.session['user_id']
        title = request.POST.get('title')
        message = request.POST.get('message')
        remarks = 'no remarks'
        rdt = ''
        rtm = ''
        status = ''

        ud = user_details.objects.get(user_id=int(request.session['user_id']))
        panchayat_id = ud.panchayat_id
        ward_no = ud.ward_no
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')


        wm = ward_user_messages(panchayat_id=panchayat_id,user_id=user_id,title=title,
                                     message=message,remarks=remarks,dt=dt,tm=tm,rdt=rdt,
                                     rtm=rtm,ward_no=ward_no,status=status)
        wm.save()

        context = {'msg':'Record added'}
        return render(request, 'myapp/user_ward_messages_add.html',context)

    else:
        context = {'msg':''}
        return render(request, 'myapp/user_ward_messages_add.html',context)

def user_ward_messages_delete(request):
    id = request.GET.get('id')
    print("id="+id)

    pm = ward_user_messages.objects.get(id=int(id))
    pm.delete()

    user_id = request.session['user_id']

    pm_l = ward_user_messages.objects.filter(user_id=int(user_id))


    context ={'message_list': pm_l,'msg':'Record deleted'}
    return render(request,'myapp/user_ward_messages_view.html',context)

def user_ward_messages_view(request):
    user_id = request.session['user_id']
    ud = user_details.objects.get(user_id=int(user_id))
    pm_l = ward_user_messages.objects.filter(user_id=int(user_id),panchayat_id=ud.panchayat_id)
    msg =''
    if len(pm_l) ==0:
        msg = 'No Messages'
    context = {'message_list': pm_l, 'msg': msg}
    return render(request, 'myapp/user_ward_messages_view.html', context)


def user_panchayat_settings_view(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)
    user_id = request.session['user_id']
    ud = user_details.objects.get(user_id=int(user_id))
    pd_l = panchayat_settings.objects.filter(id=ud.panchayat_id)
    context = {'panchayat_list':pd_l,'block_id': user_id}
    return render(request, './myapp/user_panchayat_settings_view.html',context)

##########Panchayat#############
def panchayat_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pwd = request.POST.get('pwd')
        #print(un,pwd)
        #query to select a record based on a condition
        ul = user_login.objects.filter(uname=un, passwd=pwd, u_type='panchayat')

        if len(ul) == 1:
            request.session['user_name'] = ul[0].uname
            request.session['user_id'] = ul[0].id
            return render(request,'./myapp/panchayat_home.html')
        else:
            msg = '<h1> Invalid Uname or Password !!!</h1>'
            context ={ 'msg1':msg }
            return render(request, './myapp/panchayat_login.html',context)
    else:
        msg = ''
        context ={ 'msg1':msg }
        return render(request, './myapp/panchayat_login.html',context)


def panchayat_home(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return panchayat_login(request)
    else:
        return render(request,'./myapp/panchayat_home.html')


def panchayat_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return panchayat_login(request)
    else:
        return panchayat_login(request)

def panchayat_changepassword(request):
    if request.method == 'POST':
        opasswd = request.POST.get('opasswd')
        npasswd = request.POST.get('npasswd')
        cpasswd = request.POST.get('cpasswd')
        uname = request.session['user_name']
        try:
            ul = user_login.objects.get(uname=uname,passwd=opasswd,u_type='panchayat')
            if ul is not None:
                ul.passwd=npasswd
                ul.save()
                context = {'msg': 'Password Changed'}
                return render(request, './myapp/panchayat_changepassword.html', context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/panchayat_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Err Not Changed'}
            return render(request, './myapp/panchayat_changepassword.html', context)
    else:
        context = {'msg': ''}
        return render(request, './myapp/panchayat_changepassword.html', context)

def panchayat_panchayat_settings_edit(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    if request.method == 'POST':
        user_id = int(request.session['user_id'])
        s_id = request.POST.get('s_id')
        block_id = int(request.POST.get('block_id'))
        panchayat_name = request.POST.get('panchayat_name')
        panchayat_code = request.POST.get('panchayat_code')
        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        pre_name = request.POST.get('pre_name')
        pre_contact = request.POST.get('pre_contact')
        pre_email = request.POST.get('pre_email')
        sec_name = request.POST.get('sec_name')
        sec_contact = request.POST.get('sec_contact')
        sec_email = request.POST.get('sec_email')
        ward_count = request.POST.get('ward_count')

        pd = panchayat_settings.objects.get(id=int(s_id))

        pd.panchayat_name = panchayat_name
        pd.panchayat_code = panchayat_code
        pd.addr = addr
        pd.pin = pin
        pd.pre_name = pre_name
        pd.pre_contact = pre_contact
        pd.pre_email = pre_email
        pd.sec_name = sec_name
        pd.sec_contact = sec_contact
        pd.sec_email = sec_email
        pd.ward_count = ward_count

        pd.save()
        msg = 'Record Updated'
        context = {'pd':pd,'s_id':pd.id,'block_id': block_id,'msg':msg}
        return render(request, './myapp/panchayat_panchayat_settings_edit.html', context)
    else:
        user_id = int(request.session['user_id'])
        pd = panchayat_settings.objects.get(user_id=int(user_id))
        block_id = pd.block_id
        context = {'pd':pd,'s_id':pd.id,'block_id': block_id}
        return render(request, './myapp/panchayat_panchayat_settings_edit.html',context)

from .models import ward_member_details

def panchayat_ward_member_add(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    if request.method == 'POST':
        pd = panchayat_settings.objects.get(user_id = int(request.session['user_id']))
        panchayat_id = pd.id
        member_name = request.POST.get('member_name')
        ward_no = request.POST.get('ward_no')
        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        uname = email
        password ='1234'
        ul = user_login(uname=uname, passwd=password, u_type='member')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        wd = ward_member_details(user_id=user_id,panchayat_id=panchayat_id,ward_no=ward_no,member_name=member_name,addr=addr,
                                 pin=pin,contact=contact,email=email,status='ok')
        wd.save()
        #pd = panchayat_settings.objects.get(user_id=panchayat_id)
        ward_count = pd.ward_count
        ward_list = []
        for i in range(int(ward_count)):
            ward_list.append(str(i+1))
        context = {'ward_list':ward_list,'msg': 'Record Added'}
        return render(request, './myapp/panchayat_ward_member_add.html', context)
    else:
        pd = panchayat_settings.objects.get(user_id=int(request.session['user_id']))
        panchayat_id = pd.id
        ward_count = pd.ward_count
        ward_list = []
        for i in range(int(ward_count)):
            ward_list.append(str(i+1))
        context = {'ward_list': ward_list, 'msg': ''}
        return render(request, './myapp/panchayat_ward_member_add.html', context)



def panchayat_ward_member_edit(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    if request.method == 'POST':
        s_id = request.POST.get('s_id')
        pd = panchayat_settings.objects.get(user_id=int(request.session['user_id']))
        panchayat_id = pd.id
        member_name = request.POST.get('member_name')
        ward_no = request.POST.get('ward_no')
        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        contact = request.POST.get('contact')
        email = request.POST.get('email')

        md = ward_member_details.objects.get(id=int(s_id))

        md.panchayat_id = panchayat_id
        md.member_name = member_name
        md.ward_no = ward_no
        md.addr = addr
        md.pin = pin
        md.contact = contact
        md.email = email

        md.save()
        msg = 'Record Updated'
        md_l = ward_member_details.objects.filter(panchayat_id=panchayat_id)
        context = {'member_list': md_l, 'msg': msg}
        return render(request, './myapp/admin_ward_member_view.html', context)
    else:
        id = request.GET.get('id')
        pd = panchayat_settings.objects.get(user_id=int(request.session['user_id']))
        panchayat_id = pd.id
        md = ward_member_details.objects.get(id=int(id))
        pd = panchayat_settings.objects.get(user_id=panchayat_id)
        ward_count = pd.ward_count
        ward_list = []
        for i in range(int(ward_count)):
            ward_list.append(str(i + 1))

        context = {'md':md,'s_id':md.id,'panchayat_id': panchayat_id,'ward_list':ward_list}
        return render(request, './myapp/panchayat_ward_member_edit.html',context)

def panchayat_ward_member_delete(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    id = request.GET.get('id')
    print('id = '+id)


    md = ward_member_details.objects.get(id=int(id))
    ul = user_login.objects.get(user_id = md.user_id)
    ul.delete()
    md.delete()
    pd = panchayat_settings.objects.get(user_id=int(request.session['user_id']))
    panchayat_id = pd.id
    msg = 'Record Deleted'
    md_l = ward_member_details.objects.filter(panchayat_id=panchayat_id)
    context = {'member_list': md_l,'msg':msg}
    return render(request, './myapp/panchayat_ward_member_view.html',context)

def panchayat_ward_member_view(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)
    pd = panchayat_settings.objects.get(user_id=int(request.session['user_id']))
    panchayat_id = pd.id
    msg = ''
    md_l = ward_member_details.objects.filter(panchayat_id=panchayat_id)
    context = {'member_list': md_l, 'msg': msg}
    return render(request, './myapp/panchayat_ward_member_view.html', context)

def panchayat_ward_member_search(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    if request.method == 'POST':
        query = request.POST.get('query')
        pd = panchayat_settings.objects.get(user_id=int(request.session['user_id']))
        panchayat_id = pd.id
        msg = ''
        md_l = ward_member_details.objects.filter(panchayat_id=panchayat_id,member_name__contains=query)
        context = {'member_list': md_l, 'msg': msg}
        return render(request, './myapp/panchayat_ward_member_result.html', context)
    else:
        return render(request, './myapp/panchayat_ward_member_search.html')

from .models import panchayat_news
from datetime import datetime
from django.core.files.storage import FileSystemStorage

def panchayat_news_add(request):
    if request.method == 'POST':
        u_file = request.FILES['document']
        fs = FileSystemStorage()
        file_name = fs.save(u_file.name, u_file)

        descrp = request.POST.get('descrp')
        title = request.POST.get('title')
        user_id = request.session['user_id']
        pd = panchayat_settings.objects.get(user_id=int(request.session['user_id']))
        panchayat_id = pd.id

        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')


        pm = panchayat_news(panchayat_id=panchayat_id,user_id=user_id,title=title,file_name=file_name,
                            descrp=descrp,dt=dt,tm=tm,status='new')
        pm.save()

        context = {'msg':'Record added'}
        return render(request, 'myapp/panchayat_news_add.html',context)

    else:
        context = {'msg':''}
        return render(request, 'myapp/panchayat_news_add.html',context)

def panchayat_news_delete(request):
    id = request.GET.get('id')
    print("id="+id)

    pm = panchayat_news.objects.get(id=int(id))
    pm.delete()

    user_id = request.session['user_id']

    pm_l = panchayat_news.objects.filter(user_id=int(user_id))


    context ={'news_list': pm_l,'msg':'Record deleted'}
    return render(request,'myapp/panchayat_news_view.html',context)

def panchayat_news_view(request):
    user_id = request.session['user_id']

    pm_l = panchayat_news.objects.filter(user_id=int(user_id))
    msg =''
    if len(pm_l) == 0:
        msg = 'no news'
    context = {'news_list': pm_l, 'msg': msg}
    return render(request, 'myapp/panchayat_news_view.html', context)

def panchayat_user_tax_view(request):
    user_id = request.session['user_id']
    pd = panchayat_settings.objects.get(user_id = int(user_id))
    ud_l = user_details.objects.all()
    pm_l = taxcollection.objects.filter(panchayat_id=pd.id)
    msg =''
    if len(pm_l) ==0:
        msg = 'No data'
    context = {'tax_list': pm_l,'user_list':ud_l, 'msg': msg}
    return render(request, 'myapp/panchayat_user_tax_view.html', context)

def panchayat_user_licence_request_view(request):
    user_id = request.session['user_id']
    pd = panchayat_settings.objects.get(user_id = int(user_id))
    ud_l = user_details.objects.all()
    pm_l = licence_request.objects.filter(panchayat_id=pd.id)
    msg =''
    if len(pm_l) ==0:
        msg = 'No Messages'
    context = {'licence_list': pm_l,'user_list':ud_l, 'msg': msg}
    return render(request, 'myapp/panchayat_user_licence_request_view.html', context)

def panchayat_request_edit(request):
    id = request.GET.get('id')

    status = request.GET.get('status')


    hur = licence_request.objects.get(id=int(id))
    hur.status = status


    hur.save()
    user_id = request.session['user_id']
    sd_l = licence_request.objects.all()

    context = {'licence_list': sd_l, 'msg': 'User Time Status Updated'}
    return render(request, './myapp/panchayat_home.html', context)


def panchayat_user_messages_view(request):
    user_id = request.session['user_id']
    pd = panchayat_settings.objects.get(user_id = int(user_id))
    ud_l = user_details.objects.all()
    pm_l = panchayat_user_messages.objects.filter(panchayat_id=pd.id)
    msg =''
    if len(pm_l) ==0:
        msg = 'No Messages'
    context = {'message_list': pm_l,'user_list':ud_l, 'msg': msg}
    return render(request, 'myapp/panchayat_user_messages_view.html', context)

def panchayat_user_messages_reply(request):
    if request.method == 'POST':

        user_id = request.session['user_id']
        message_id = int(request.POST.get('message_id'))
        msg = request.POST.get('answer')

        um = panchayat_user_messages.objects.get(id=int(message_id))
        um.remarks = msg
        um.rdt = datetime.today().strftime('%Y-%m-%d')
        um.rtm = datetime.today().strftime('%H:%M:%S')
        um.save()

        pd = panchayat_settings.objects.get(user_id=int(user_id))
        ud_l = user_details.objects.all()
        pm_l = panchayat_user_messages.objects.filter(panchayat_id=pd.id)
        msg = ''
        if len(pm_l) == 0:
            msg = 'No Messages'
        context = {'message_list': pm_l, 'user_list': ud_l, 'msg': msg}
        return render(request, 'myapp/panchayat_user_messages_view.html', context)

    else:
        user_id = request.session['user_id']
        message_id = int(request.GET.get('id'))

        context = { 'message_id': message_id}
        return render(request, './myapp/panchayat_user_messages_reply.html', context)


############## WARD MEMBER ###############
def ward_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pwd = request.POST.get('pwd')
        #print(un,pwd)
        #query to select a record based on a condition
        ul = user_login.objects.filter(uname=un, passwd=pwd, u_type='member')

        if len(ul) == 1:
            request.session['user_name'] = ul[0].uname
            request.session['user_id'] = ul[0].id
            return render(request,'./myapp/ward_home.html')
        else:
            msg = '<h1> Invalid Uname or Password !!!</h1>'
            context ={ 'msg1':msg }
            return render(request, './myapp/ward_login.html',context)
    else:
        msg = ''
        context ={ 'msg1':msg }
        return render(request, './myapp/ward_login.html',context)


def ward_home(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return ward_login(request)
    else:
        return render(request,'./myapp/ward_home.html')


def ward_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return ward_login(request)
    else:
        return ward_login(request)

def ward_changepassword(request):
    if request.method == 'POST':
        opasswd = request.POST.get('opasswd')
        npasswd = request.POST.get('npasswd')
        cpasswd = request.POST.get('cpasswd')
        uname = request.session['user_name']
        try:
            ul = user_login.objects.get(uname=uname,passwd=opasswd,u_type='member')
            if ul is not None:
                ul.passwd=npasswd
                ul.save()
                context = {'msg': 'Password Changed'}
                return render(request, './myapp/ward_changepassword.html', context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/ward_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Err Not Changed'}
            return render(request, './myapp/ward_changepassword.html', context)
    else:
        context = {'msg': ''}
        return render(request, './myapp/ward_changepassword.html', context)

def ward_member_details_edit(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return ward_login(request)

    if request.method == 'POST':
        user_id = int(request.session['user_id'])
        s_id = request.POST.get('s_id')
        member_name = request.POST.get('member_name')
        ward_no = request.POST.get('ward_no')
        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        contact = request.POST.get('contact')
        email = request.POST.get('email')

        md = ward_member_details.objects.get(id=int(s_id))

        md.member_name = member_name
        md.ward_no = ward_no
        md.addr = addr
        md.pin = pin
        md.contact = contact
        md.email = email

        md.save()
        msg = 'Record Updated'
        context = {'md':md,'s_id':md.id,'panchayat_id': md.panchayat_id,'msg':msg}
        return render(request, './myapp/ward_member_details_edit.html', context)
    else:
        user_id = int(request.session['user_id'])
        md = ward_member_details.objects.get(user_id=int(user_id))
        panchayat_id = md.panchayat_id
        context = {'md':md,'s_id':md.id,'panchayat_id': panchayat_id}
        return render(request, './myapp/ward_member_details_edit.html',context)

def ward_panchayat_news_view(request):
    user_id = request.session['user_id']
    wd = ward_member_details.objects.get(user_id=user_id)
    pm_l = panchayat_news.objects.filter(panchayat_id=wd.panchayat_id)
    msg =''
    if len(pm_l) == 0:
        msg = 'no news'
    context = {'news_list': pm_l, 'msg': msg}
    return render(request, 'myapp/ward_panchayat_news_view.html', context)


from .models import ward_news
def ward_news_add(request):
    if request.method == 'POST':
        u_file = request.FILES['document']
        fs = FileSystemStorage()
        file_name = fs.save(u_file.name, u_file)

        descrp = request.POST.get('descrp')
        title = request.POST.get('title')
        user_id = request.session['user_id']
        md = ward_member_details.objects.get(user_id=int(request.session['user_id']))
        panchayat_id = md.panchayat_id
        ward_no =md.ward_no

        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')


        pm = ward_news(panchayat_id=panchayat_id,user_id=user_id,title=title,file_name=file_name,
                            descrp=descrp,dt=dt,tm=tm,status='new',ward_no=ward_no)
        pm.save()

        context = {'msg':'Record added'}
        return render(request, 'myapp/ward_news_add.html',context)

    else:
        context = {'msg':''}
        return render(request, 'myapp/ward_news_add.html',context)

def ward_news_delete(request):
    id = request.GET.get('id')
    print("id="+id)

    wn = ward_news.objects.get(id=int(id))
    wn.delete()

    user_id = request.session['user_id']

    wn_l = ward_news.objects.filter(user_id=int(user_id))


    context ={'news_list': wn_l,'msg':'Record deleted'}
    return render(request,'myapp/ward_news_view.html',context)

def ward_news_view(request):
    user_id = request.session['user_id']

    wn_l = ward_news.objects.filter(user_id=int(user_id))
    msg =''
    if len(wn_l) == 0:
        msg = 'no news'
    context = {'news_list': wn_l, 'msg': msg}
    return render(request, 'myapp/ward_news_view.html', context)


from .models import ward_covid
def ward_covid_add(request):
    if request.method == 'POST':

        poscase = request.POST.get('poscase')
        negcase = request.POST.get('negcase')
        user_id = request.session['user_id']
        md = ward_member_details.objects.get(user_id=int(request.session['user_id']))
        panchayat_id = md.panchayat_id
        ward_no =md.ward_no

        dt = datetime.today().strftime('%Y-%m-%d')
        status='new'


        pm = ward_covid(panchayat_id=panchayat_id,user_id=int(user_id),ward_no=ward_no,poscase=poscase,
                        negcase=negcase,dt=dt,status=status)
        pm.save()

        context = {'msg':'Record added'}
        return render(request, 'myapp/ward_covid_add.html',context)

    else:
        context = {'msg':''}
        return render(request, 'myapp/ward_covid_add.html',context)

def ward_covid_delete(request):
    id = request.GET.get('id')
    print("id="+id)

    wn = ward_news.objects.get(id=int(id))
    wn.delete()

    user_id = request.session['user_id']

    wn_l = ward_covid.objects.filter(user_id=int(user_id))


    context ={'covid_list': wn_l,'msg':'Record deleted'}
    return render(request,'myapp/ward_covid_view.html',context)

def ward_covid_edit(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return ward_login(request)

    if request.method == 'POST':
        user_id = int(request.session['user_id'])
        s_id = request.POST.get('s_id')
        poscase = request.POST.get('poscase')
        negcase = request.POST.get('negcase')

        md = ward_covid.objects.get(id=int(s_id))

        md.poscase = poscase
        md.negcase = negcase

        md.save()
        msg = 'Record Updated'
        context = {'md':md,'s_id':md.id,'panchayat_id': md.panchayat_id,'msg':msg}
        return render(request, './myapp/ward_covid_edit.html', context)
    else:
        user_id = int(request.session['user_id'])
        md = ward_covid.objects.get(user_id=int(user_id))
        panchayat_id = md.panchayat_id
        context = {'md':md,'s_id':md.id,'panchayat_id': panchayat_id}
        return render(request, './myapp/ward_covid_edit.html',context)


def ward_covid_view(request):
    user_id = request.session['user_id']

    wn_l = ward_covid.objects.filter(user_id=int(user_id))
    msg =''
    if len(wn_l) == 0:
        msg = 'no data'
    context = {'covid_list': wn_l, 'msg': msg}
    return render(request, 'myapp/ward_covid_view.html', context)



def ward_member_search(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    if request.method == 'POST':
        query = request.POST.get('query')
        md = ward_member_details.objects.get(user_id=int(request.session['user_id']))
        panchayat_id = md.panchayat_id
        msg = ''
        md_l = ward_member_details.objects.filter(panchayat_id=panchayat_id,member_name__contains=query)
        context = {'member_list': md_l, 'msg': msg}
        return render(request, './myapp/ward_member_result.html', context)
    else:
        return render(request, './myapp/ward_member_search.html')


def ward_user_search(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    if request.method == 'POST':
        query = request.POST.get('query')
        md = ward_member_details.objects.get(user_id=int(request.session['user_id']))
        panchayat_id = md.panchayat_id
        msg = ''
        md_l = user_details.objects.filter(panchayat_id=panchayat_id,house_no__contains=query)
        context = {'user_list': md_l, 'msg': msg}
        return render(request, './myapp/ward_user_result.html', context)
    else:
        return render(request, './myapp/ward_user_search.html')


def ward_user_messages_view(request):
    user_id = request.session['user_id']
    wd = ward_member_details.objects.get(user_id = int(user_id))
    ud_l = user_details.objects.all()
    pm_l = ward_user_messages.objects.filter(panchayat_id=wd.panchayat_id, ward_no=wd.ward_no)
    msg =''
    if len(pm_l) ==0:
        msg = 'No Messages'
    context = {'message_list': pm_l,'user_list':ud_l, 'msg': msg}
    return render(request, 'myapp/ward_user_messages_view.html', context)

def ward_user_messages_reply(request):
    if request.method == 'POST':

        user_id = request.session['user_id']
        message_id = int(request.POST.get('message_id'))
        msg = request.POST.get('answer')

        um = ward_user_messages.objects.get(id=int(message_id))
        um.remarks = msg
        um.rdt = datetime.today().strftime('%Y-%m-%d')
        um.rtm = datetime.today().strftime('%H:%M:%S')
        um.save()

        wd = ward_member_details.objects.get(user_id=int(user_id))
        ud_l = user_details.objects.all()
        pm_l = ward_user_messages.objects.filter(panchayat_id=wd.panchayat_id, ward_no=wd.ward_no)
        msg = ''
        if len(pm_l) == 0:
            msg = 'No Messages'
        context = {'message_list': pm_l, 'user_list': ud_l, 'msg': msg}
        return render(request, 'myapp/ward_user_messages_view.html', context)
    else:
        user_id = request.session['user_id']
        message_id = int(request.GET.get('id'))

        context = { 'message_id': message_id}
        return render(request, './myapp/ward_user_messages_reply.html', context)

def ward_panchayat_settings_view(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)
    user_id = request.session['user_id']
    ud = ward_member_details.objects.get(user_id=int(user_id))
    pd_l = panchayat_settings.objects.filter(id=ud.panchayat_id)
    context = {'panchayat_list':pd_l,'block_id': user_id}
    return render(request, './myapp/ward_panchayat_settings_view.html',context)

# def export_pdf(request):
#      response = HttpResponse(content_type='application/pdf')
#      response['Content-Disposition'] = 'inline; attachment; filename=User Details' + '.pdf'
#      response['Content-Transfer-Encoding'] = 'binary'
#
#      try:
#          uname = request.session['user_name']
#          print(uname)
#      except:
#          return admin_login(request)
#      pp_l = taxcollection.objects.all()
#      context = {'myapp': pp_l}
#      # return render(request, './myapp/pdf-output.html', context)
#
#      html_string = render_to_string('./myapp/pdf-output.html', {'myapp': pp_l})
#      html = HTML(string=html_string)
#
#      result = html.write_pdf()
#
#      with tempfile.NamedTemporaryFile(delete=True) as output:
#          output.write(result)
#          output.flush()
#          output.seek(0)
#          response.write(output.read())
#
#      return response

def export_pdf(request):
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = 'inline; attachment; filename=User Details' + '.pdf'
     response['Content-Transfer-Encoding'] = 'binary'

     user_id = request.session['user_id']
     pd = panchayat_settings.objects.get(user_id=int(user_id))
     ud_l = user_details.objects.all()
     pm_l = taxcollection.objects.filter(panchayat_id=pd.id)
     msg = ''
     if len(pm_l) == 0:
         msg = 'No data'
     context = {'tax_list': pm_l, 'user_list': ud_l, 'msg': msg}


     # return render(request, './myapp/pdf-output.html', context)

     html_string = render_to_string('./myapp/pdf-output.html', context)
     html = HTML(string=html_string)

     result = html.write_pdf()

     with tempfile.NamedTemporaryFile(delete=True) as output:
         output.write(result)
         output.flush()
         output.seek(0)
         response.write(output.read())

     return response

def invoice_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=User Details' + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    t_id = request.GET.get('t_id')
    user_id = request.session['user_id']
    pm_l = taxcollection.objects.get(id=int(t_id), user_id=int(user_id))
    context = {'tax_item': pm_l, 'msg': ''}

    if pm_l.status != "Payment Success":
        pm_l = taxcollection.objects.filter(user_id=int(user_id))
        msg = 'Unable to print the Invoice: Payment not done'

        if len(pm_l) == 0:
            msg = 'No Data'
        context = {'tax_list': pm_l, 'msg': msg}
        return render(request, 'myapp/user_tax_view.html', context)

    html_string = render_to_string('./myapp/invoice_pdf.html', context)
    html = HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response
