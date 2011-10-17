#-*- coding: utf-8 -*-
#
#PromoCMS
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

pageCommonDict = {"staticMenuActive":"StaticMenuAction(req=self.req).staticMenuActive()",
                "staticMenuList":"StaticMenuAction(req=self.req).staticMenuList()",
                "staticMenuAdd":"StaticMenuAction(req=self.req).staticMenuAdd()",
                "staticMenuDel":"StaticMenuAction(req=self.req).staticMenuDel()",
                "staticMenuEdit":"StaticMenuAction(req=self.req).staticMenuEdit()",
                "staticPagesList":"StaticPagesAction(req=self.req).staticPagesList()",
                "staticPagesAdd" :"StaticPagesAction(req=self.req).staticPagesAdd()",
                "staticPagesDel" : "StaticPagesAction(req=self.req).staticPagesDel()",
                "staticPagesEdit" :"StaticPagesAction(req=self.req).staticPagesEdit()",
                "contact":"ContactForm(req=self.req).contact()",
                "feedList": "FeedAction(req=self.req).feedList()",
                "feedAdd": "FeedAction(req=self.req).feedAdd()",
                "feedDel": "FeedAction(req=self.req).feedDel()",
                "feedEdit": "FeedAction(req=self.req).feedEdit()",
                "login" : "Login(req=self.req).login()",
                "logout":"Login(req=self.req).logout()",
                "roleList": "RoleActionAction(req=self.req).roleList()",
                "roleAdd": "RoleActionAction(req=self.req).roleAdd()",
                "roleActiveAction":"RoleActionAction(req=self.req).roleActiveAction()",
                "roleDel":  "RoleActionAction(req=self.req).roleDel()",
                "roleMod": "RoleActionAction(req=self.req).roleMod()",
                "roleUpdate":"RoleActionAction(req=self.req).roleUpdate()",
                "roleActionActive": "RoleActionAction(req=self.req).roleActionActive()",
                "siteAdmin": "SiteAdmin(req=self.req).siteAdmin()",
                "showPage": "Static(req=self.req).showPage()",
                "userList":"UserAction(req=self.req).userList()",
                "userAdd":"UserAction(req=self.req).userAdd()",
                "userDel":"UserAction(req=self.req).userDel()",
                "userActive":"UserAction(req=self.req).userActive()",
                "userMod":"UserAction(req=self.req).userMod()",
                "userUpdate":"UserAction(req=self.req).userUpdate()",
                "userDetail":"UserAction(req=self.req).userDetail()",
                "userProfile":"UserProfile(req=self.req).userProfile()",
                "insertProfile":"UserProfile(req=self.req).insertProfile()",
}