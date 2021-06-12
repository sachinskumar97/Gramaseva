from django.contrib import admin

# Register your models here.
# state_settings,district_settings, block_settings, panchayat_settings, ward_member_details
# user_details, user_login, panchayat_news, ward_news,ward_news_user_messages,panchayat_user_messages
# ward_user_messages,

from .models import state_settings,district_settings, block_settings, panchayat_settings, ward_member_details
from .models import user_details, user_login, panchayat_news, ward_news,ward_news_user_messages,panchayat_user_messages
from .models import ward_user_messages, ward_covid,taxcollection

admin.site.register(state_settings)
admin.site.register(district_settings)
admin.site.register(block_settings)
admin.site.register(panchayat_settings)
admin.site.register(ward_member_details)
admin.site.register(user_details)
admin.site.register(user_login)
admin.site.register(panchayat_news)
admin.site.register(ward_news)
admin.site.register(ward_news_user_messages)
admin.site.register(panchayat_user_messages)
admin.site.register(ward_user_messages)
admin.site.register(ward_covid)
admin.site.register(taxcollection)