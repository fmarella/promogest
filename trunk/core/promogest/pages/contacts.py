#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

import hashlib

from core import Environment
from core.lib.utils import *
from core.lib.page import Page

import Image,ImageDraw
from random import randint as rint
import ImageFont

def createcaptcha():
    """
    Creiamo una immagine con dei valori random ed un font trash_.tff
    """
    img = Image.new("RGB", (220,75), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Trash_.ttf", 52)
    r,g,b = rint(0,255), rint(0,255), rint(0,255)
    dr = (rint(0,255) - r)/300.
    dg = (rint(0,255) - g)/300.
    db = (rint(0,255) - b)/300.
    for i in range(300):
        r,g,b = r+dr, g+dg, b+db
        draw.line((i,0,i,300), fill=(int(r),int(g),int(b)))
    string = ""
    values = "1234567890QWERTYUIOPASDFGHJKLZXCVBNM"
    for a in range(5):
        b =  rint(0,35)
        string += values[b]

    draw.text((20, 20), string, font=font)
    img.save("templates/captcha.png", "PNG")
    return string

def contacts(req, static=None, subdpmain=None):
    """
    funzione per la cattura dati form contatti
    """
    captchamd5=""
    captcha = req.form.get('captcha')
    name = req.form.get('name')
    stringmd5 = req.form.get('string')
    lastname = req.form.get('lastname')
    company = req.form.get('company')
    address = req.form.get('adress')
    city = req.form.get('city')
    telephone = req.form.get('telephone')
    email = req.form.get('email')
    obj = req.form.get('oggetto')
    body = req.form.get('body')

    if captcha:
        captchamd5 = hashlib.md5(captcha).hexdigest()
    if not captcha:
        string = createcaptcha()
        pageData = {'file' : 'contacts',
                    'string':hashlib.md5(string).hexdigest(),
                    'sent' : "False"}
        return Page(req).render(pageData)
    elif captchamd5 == stringmd5:
        SendMail(req=req,email=email).sendContact(obj=obj, note=body, name = name +" "+ lastname, telefono = telephone)
        pageData = {'file' : 'contacts',
                    'sent' : "True"}
        return Page(req).render(pageData)
    else:
        string = createcaptcha()
        print "ERRORE NEL RICONOSCIMENTO DEL captcha", string ,captcha
        pageData = {'file' : 'contacts',
                    'string':hashlib.md5(string).hexdigest(),
                    'sent' : "False"
}
        return Page(req).render(pageData)
