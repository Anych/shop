from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from uuslug import slugify
from time import time


def gen_slug(obj, cat):
    new_slug = slugify(cat)
    obj = str(obj)
    new_slug2 = slugify(obj)
    return new_slug2 + '-' + new_slug + '-' + str(int(time()))


def question_email(name, email, question, product_url):
    mail_subject = 'Новый вопрос на сайте'
    message = render_to_string('accounts/question_email.html', {
        'name': name,
        'email': email,
        'question': question,
        'product_url': product_url,
    })
    send_email = EmailMessage(mail_subject, message, to=['mila-iris@mila-iris.kz', 'anuar123@mail.ru',
                                                         'botaonelove@yandex.ru', 'anuar.umarov@gmail.com'])
    send_email.send()


def order_email(order_id):
    mail_subject = 'Новый заказ на сайте'
    message = render_to_string('accounts/new_order.html', {
        'order_id': order_id,
    })
    send_email = EmailMessage(mail_subject, message, to=['mila-iris@mila-iris.kz', 'anuar123@mail.ru',
                                                         'botaonelove@yandex.ru', 'anuar.umarov@gmail.com'])
    send_email.send()
