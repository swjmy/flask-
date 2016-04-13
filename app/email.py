from threading import Thread
from flask import current_app,render_template
from flask.ext.mail import Message
from . import mail

'''
App Context,Request Context是TheadLocal对象
它们存在LocalStack(一种ThreadLocal型的栈数据结构)中,
栈顶存放的是当前的Context(这个应该可以理解的)
LocalProxy使用代理模式，realobject指向LocalStack的栈顶。
App Context是线程隔离的，所以在新线程中要用with(访问完毕自动关闭)app的App Context'''
def send_async_email(app,msg):
     with app.app_context():
         '''
         within this block, current_app points to app
         导入的这个mail对象还没有init(app)
         所以要获取app的App Context'''
         mail.send(msg)

def send_email(recipient,subject,template,**kwargs):
    '''
    #current_app是一个ProxyStack
    #get_current_object从LocalStack取得栈顶元素
    #为什么要获取app?直接send不就行了？
    #因为要孵化出新的线程去执行send，app,msg被作为参数传递
    #需要用到app.config
    '''''
    app = current_app._get_current_object()
    msg =Message(subject=subject,recipients=[recipient],
                 sender=app.config['FLASKY_MAIL_SENDER'])
    msg.body= render_template(template+'.txt',**kwargs)
    msg.html=render_template(template+'html',**kwargs)
    thr = Thread(target='send_async_email',args=(app,msg))
    thr.start()
    return thr





