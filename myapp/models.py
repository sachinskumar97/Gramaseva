from django.db import models

# Create your models here.
class user_login(models.Model):
    uname = models.CharField(max_length=100)
    passwd = models.CharField(max_length=25)
    u_type = models.CharField(max_length=10)

class state_settings(models.Model):
    state_name = models.CharField(max_length=50)
    state_code = models.CharField(max_length=10)

class district_settings(models.Model):
    state_id = models.IntegerField()
    district_name = models.CharField(max_length=50)
    district_code = models.CharField(max_length=10)

class block_settings(models.Model):
    district_id = models.IntegerField()
    block_name = models.CharField(max_length=50)
    block_code = models.CharField(max_length=10)

class panchayat_settings(models.Model):
    block_id = models.IntegerField()
    user_id = models.IntegerField()
    panchayat_name = models.CharField(max_length=50)
    panchayat_code = models.CharField(max_length=10)
    addr = models.CharField(max_length=500)
    pin = models.CharField(max_length=25)
    pre_name = models.CharField(max_length=50)
    pre_contact = models.CharField(max_length=25)
    pre_email = models.CharField(max_length=250)
    sec_name = models.CharField(max_length=50)
    sec_contact = models.CharField(max_length=25)
    sec_email = models.CharField(max_length=250)
    ward_count = models.CharField(max_length=10)
    status = models.CharField(max_length=25)

class ward_member_details(models.Model):
    user_id = models.IntegerField()
    panchayat_id = models.IntegerField()
    ward_no = models.CharField(max_length=10)
    member_name = models.CharField(max_length=50)
    addr = models.CharField(max_length=500)
    pin = models.CharField(max_length=25)
    contact = models.CharField(max_length=25)
    email = models.CharField(max_length=250)
    status = models.CharField(max_length=25)

class user_details(models.Model):
    user_id = models.IntegerField()
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    panchayat_id = models.IntegerField()
    house_no = models.CharField(max_length=10)
    ward_no = models.CharField(max_length=10)
    addr = models.CharField(max_length=500)
    district_id = models.IntegerField()
    state_id = models.IntegerField()
    pin = models.CharField(max_length=25)
    gender = models.CharField(max_length=25)
    dob = models.CharField(max_length=10)
    contact = models.CharField(max_length=25)
    email = models.CharField(max_length=250)
    aadhaar_no = models.CharField(max_length=25)
    status = models.CharField(max_length=25)


class panchayat_news(models.Model):
    panchayat_id = models.IntegerField()
    user_id = models.IntegerField()
    title = models.CharField(max_length=25)
    descrp = models.CharField(max_length=500)
    file_name = models.CharField(max_length=250)
    dt = models.CharField(max_length=25)
    tm = models.CharField(max_length=25)
    status = models.CharField(max_length=25)

class ward_news(models.Model):
    panchayat_id = models.IntegerField()
    user_id = models.IntegerField()
    ward_no = models.CharField(max_length=25)
    title = models.CharField(max_length=25)
    descrp = models.CharField(max_length=500)
    file_name = models.CharField(max_length=250)
    dt = models.CharField(max_length=25)
    tm = models.CharField(max_length=25)
    status = models.CharField(max_length=25)

class ward_covid(models.Model):
    panchayat_id = models.IntegerField()
    user_id = models.IntegerField()
    ward_no = models.CharField(max_length=25)
    poscase = models.CharField(max_length=25)
    negcase = models.CharField(max_length=500)
    dt = models.CharField(max_length=25)
    status = models.CharField(max_length=25)


class ward_news_user_messages(models.Model):
    ward_news_id = models.IntegerField()
    user_id = models.IntegerField()
    remarks = models.CharField(max_length=250)
    dt = models.CharField(max_length=25)
    tm = models.CharField(max_length=25)
    status = models.CharField(max_length=25)

class panchayat_user_messages(models.Model):
    panchayat_id = models.IntegerField()
    user_id = models.IntegerField()
    title = models.CharField(max_length=50)
    message = models.CharField(max_length=500)
    dt = models.CharField(max_length=25)
    tm = models.CharField(max_length=25)
    remarks = models.CharField(max_length=500)
    rdt = models.CharField(max_length=25)
    rtm = models.CharField(max_length=25)
    status = models.CharField(max_length=25)

class ward_user_messages(models.Model):
    panchayat_id = models.IntegerField()
    user_id = models.IntegerField()
    ward_no = models.CharField(max_length=25)
    title = models.CharField(max_length=50)
    message = models.CharField(max_length=500)
    dt = models.CharField(max_length=25)
    tm = models.CharField(max_length=25)
    remarks = models.CharField(max_length=500)
    rdt = models.CharField(max_length=25)
    rtm = models.CharField(max_length=25)
    status = models.CharField(max_length=25)

class licence_request(models.Model):
    panchayat_id = models.IntegerField()
    user_id = models.IntegerField()
    title = models.CharField(max_length=50)
    descp = models.CharField(max_length=500)
    image = models.CharField(max_length=500)
    dt = models.CharField(max_length=25)
    tm = models.CharField(max_length=25)
    status = models.CharField(max_length=25)

class taxcollection(models.Model):
    panchayat_id = models.IntegerField()
    user_id = models.IntegerField()
    houseno = models.CharField(max_length=50)
    amount = models.CharField(max_length=500)
    status = models.CharField(max_length=25)
    dt = models.CharField(max_length=25)
    tm = models.CharField(max_length=25)

class taxpayment(models.Model):
    name = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    paid = models.BooleanField(default=False)



