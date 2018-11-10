import xadmin
from .models import EmailVerifyRecord,Banner


#xadmin中这里是继承object，不在是继承admin
class EmailVerifyRecordAdmin(object):
    #显示的列
    list_display=['code','email','send_type','send_time']
    #搜索的字段，不要添加时间搜索
    search_fields=['code','email','send_type']
    #过滤
    list_filter=['code','email','send_type','send_time']


class BannerAdmin(object):
    list_display=['title','image','url','index','add_time']
    search_fields=['title','image','url','index']
    list_filter=['title','image','url','index','add_time']





#xadmin的全局配置
from xadmin import views
#创建xadmin的最基本的管理配置器，并y与view绑定
class BaseSetting(object):
    #开启主题功能
    enable_themes=True
    use_bootswatch=True


class GlobalSettings(object):
    #修改title
    site_title="个人资料库管理中心"
    #修改footer
    site_footer='未来梦想'
    #收起菜单
    menu_style='accordion'

xadmin.site.register(views.CommAdminView,GlobalSettings)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin )
xadmin.site.register(Banner,BannerAdmin)





