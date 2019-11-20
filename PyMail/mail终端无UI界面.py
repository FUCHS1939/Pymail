#!/usr/bin/python
# coding:utf-8
"""
Created on Thur Nov 7 21:25:28 2019
@author: fuchs1939
"""

import re
import os
import zmail
from contextlib import suppress

dict_account = {"USERNAME": "", "PASSWORD": ""}
pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


def printfline(): print("____________________________________________________________\n")


"""
____________________________________________________________

    1. 显示收信箱        2. 查看邮件
    3. 查看最新的邮件      4. 删除邮件
    5. 发送新邮件        6. 备份邮箱全部邮件
    7.退出
    请输入菜单序号选择：

"""


# 登录后显示菜单
def showmenu():
    try:
        printfline()
        i = int(input("\t1. 显示收信箱\t\t2. 查看邮件\n\t3. 查看最新的邮件\t4. 删除邮件\n\t5. 发送新邮件\t\t6. 备份邮箱全部邮件\n\t7.退出\n\t请输入菜单序号选择："))
    except ValueError:
        print("非法输入")
        showmenu()
    if (i == 1):
        showmaillist()
        showmenu()
    elif (i == 2):
        getmailidandshowmail()
        showmenu()
    elif (i == 3):
        shownewestmail()
        showmenu()
    elif (i == 4):
        deletemail()
        showmenu()
    elif (i == 5):
        sendmail()
        showmenu()
    elif (i == 6):
        save_all_mail()
    elif (i == 7):
        exit()
    else:
        print("非法输入")
        showmenu()


# 用于 登录邮箱
def login():
    global server
    while (True):
        printfline()
        print("   在使用程序之前请确保你已经打开了邮箱的POP3和SMTP功能")
        print("         并且拥有用于POP3和SMTP客户端的授权密码\n")

        while (True):
            dict_account["USERNAME"] = input("\n请输入邮箱账号：")
            if (re.match(pattern, dict_account["USERNAME"]) == None):
                print("请注意邮箱格式")
            else:
                break
        print("\n请注意这里输入的并不为登录密码，而是用于POP3和SMTP客户端的授权密码")
        dict_account["PASSWORD"] = input("请输入授权密码：")
        server = zmail.server(dict_account["USERNAME"], dict_account["PASSWORD"])
        if server.smtp_able():
            pass
        else:
            print("无法连接SMTP服务，请检查邮箱账号和授权密码")
        if server.pop_able():
            print("\n\t\t\t登录成功")
            printfline()
            break
        else:
            print("无法连接POP3服务，请检查邮箱账号和授权密码")
    showmenu()


# 发送邮件
def sendmail():
    attachmentslist = []  # 附件列表
    recipients = []  # 收件人列表
    mail = {
        "from": "",  # 发信人名字
        "subject": "",  # 标题
        "content_text": "",  # 内容
        "attachments": attachmentslist,  # 附件
    }

    # 设置发信者名字
    printfline()
    str = input("是否设置发信者名字，默认否，输入y或Y则进入设置：")
    if (str == "y" or str == "Y"):
        while (True):
            str = input("请输入发信者名字：")
            if str.isspace() or len(str) == 0:
                print("发信者名字不能为空")
                printfline()
            else:
                mail["from"] = str + "<" + dict_account["USERNAME"] + ">"
                break

    # 设置邮件标题
    while (True):
        printfline()
        mail["subject"] = input("请输入邮件标题：")
        if mail["subject"].isspace() or len(mail["subject"]) == 0:
            print("邮件标题不能为空")
        else:
            break

    # 输入邮件内容
    while (True):
        printfline()
        mail["content_text"] = input("请输入邮件内容,最后以#end为结尾:\n")
        if (mail["content_text"].isspace() or len(mail["content_text"]) == 0):
            print("邮件内容不能为空")
        else:
            break
    while (re.search("#end", mail["content_text"]) == None):
        mail["content_text"] = mail["content_text"] + "\n" + input()

    # 设置附带附件
    printfline()
    str = input("是否附带附件，默认否，输入y或Y则添加附件：")
    if (str == "y" or str == "Y"):
        while (True):
            str = input("请输入附件path，检查无误后回车:")
            try:
                if (os.path.isfile(str)):
                    attachmentslist.append(str)
                    print("附件添加成功", end="")
                else:
                    print("附件添加失败，检查是否输入了错误的文件path")
            except:
                print("附件添加失败，检查是否输入了错误的文件path格式")
            str = input("是否继续附带附件，默认否，输入y或Y则添加附件：")
            if (str != "y" and str != "Y"):
                break
            printfline()

    # 设置收信人
    while (True):
        printfline()
        str = input("请输入收件人邮箱：")
        if (re.match(pattern, str) == None):
            print("请注意邮箱格式")
        else:
            recipients.append(str)
            str = input("是否继续添加收信人，默认否，输入y或Y则添加：")
            if (str != "y" and str != "Y"):
                break
    # 发送邮件
    try:
        server.send_mail(recipients, mail, auto_add_from=True, auto_add_to=True)
    except:
        print("发送失败")
    else:
        print("发送成功")


# 显示收信箱
def showmaillist():
    printfline()
    getmail_list = []
    num = server.stat()[0]
    print("共检查到有{}封邮件".format(num))
    if num % 10:
        n = num // 10 + 1
    else:
        n = num // 10
    for i in range(n):
        getmail_list = server.get_mails(start_index=1 + 10 * i, end_index=10 * (i + 1))
        print("ID\t  标题")
        for j in range(len(getmail_list)):
            print("{}\t {}".format(j + 1 + 10 * i, getmail_list[j]["subject"]))
        print("已经显示了{}封邮件".format(10 * i + len(getmail_list)), end="")
        str = input("是否继续显示邮件,默认继续，输入n停止显示")
        if (str == "n" or str == "N"):
            return 1
    print("邮件列表全部显示完毕")


# 获取查看邮件的ID
def getmailidandshowmail():
    while (True):
        printfline()
        str = input("请输入查看邮件的ID,若不知道所需邮件的ID，请先查阅收信箱,可输入e返回上一级：")
        if str == "e" or str == "E":
            break
        else:
            try:
                str = int(str)
            except ValueError:
                print("ID应该为全数字")
            else:
                if (str < server.stat()[0]):
                    showmail(str)
                    break
                else:
                    print("ID不能超过邮件数量上限")


# 显示邮件内容
def showmail(id):
    mail = server.get_mail(id)
    str = mail["content_text"][0].replace("\\r", " ").replace("\\n", "\n")
    print(str)


# 显示最新的邮件内容
def shownewestmail():
    mail = server.get_latest()
    str = mail["content_text"][0].replace("\\r", " ").replace("\\n", "\n")
    print(str)


# 删除邮件
def deletemail():
    while (True):
        printfline()
        str = input("请输入删除邮件的ID,若不知道所需邮件的ID，请先查阅收信箱,可输入e返回上一级：")
        if str == "e" or str == "E":
            break
        else:
            try:
                str = int(str)
            except ValueError:
                print("ID应该为全数字")
            else:
                if (str < server.stat()[0]):
                    i = input("是否确认删除该邮件？确认请输入y,其他输入则取消操作：")
                    if i == "Y" or i == "y":
                        break
                    server.delete(str)
                    break
                else:
                    print("ID不能超过邮件数量上限")


def get_walk():
    if os.path.exists(backup_walk_path):
        with open(backup_walk_path, mode='r') as f:
            _walk = int(f.read())
        return _walk
    return 1


def save_walk(_walk):
    with open(backup_walk_path, mode='w') as f:
        f.write(str(_walk))


def safe_str(o, max_len=250):
    if o is None:
        return ''
    s = str(o).replace('/', '：').replace('\\', '_').replace('*', 'x').replace('?', '_').replace('"', '_').replace('<',
                                                                                                                  '《').replace(
        '>', '》').replace('|', '_')
    if len(s) > max_len:
        return s[:max_len]
    return s


# 备份全部邮件
def save_all_mail():
    global backup_walk_path
    backup_dir = '{}_backup/'.format(dict_account["USERNAME"])
    persist_walk = True
    walk_steps = 20
    backup_walk_path = backup_dir + '_mail_walk.txt'

    mail_count, mail_size = server.stat()

    # 如果报错就创建目录
    with suppress(FileExistsError):
        os.mkdir(backup_dir)

    walk = get_walk() if persist_walk else 1
    while walk <= mail_count:
        mails = server.get_mails(start_index=walk, end_index=walk + walk_steps)
        for mail in mails:
            zmail.save(mail,
                       name=safe_str(mail['subject']) + '.eml',
                       target_path=backup_dir,
                       overwrite=True)
            print('{} {} {}\{}'.format(mail['subject'], mail['date'], walk, mail_count))
            walk += 1
            if persist_walk:
                save_walk(walk)


if __name__ == "__main__":
    login()


