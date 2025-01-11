from DrissionPage.common import Keys
import time
import re
from colorama import Fore, Style, init

# 初始化colorama
init()

# 定义emoji和颜色常量
EMOJI = {
    'MAIL': '📧',
    'SEARCH': '🔍',
    'WAIT': '⏳',
    'SUCCESS': '✅',
    'ERROR': '❌',
    'CLEAN': '🧹',
    'INPUT': '⌨️',
    'CODE': '🔢'
}

class EmailVerificationHandler:
    def __init__(self, browser, mail_url="https://tempmail.plus"):
        self.browser = browser
        self.mail_url = mail_url

    def get_verification_code(self, email):
        username = email.split("@")[0]
        code = None

        try:
            print(f"{Fore.CYAN}{EMOJI['MAIL']} 正在处理邮箱验证...{Style.RESET_ALL}")
            # 打开新标签页访问临时邮箱
            tab_mail = self.browser.new_tab(self.mail_url)
            self.browser.activate_tab(tab_mail)

            # 输入用户名
            self._input_username(tab_mail, username)

            # 等待并获取最新邮件
            code = self._get_latest_mail_code(tab_mail)

            # 清理邮件
            self._cleanup_mail(tab_mail)

            # 关闭标签页
            tab_mail.close()

        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} 获取验证码失败: {str(e)}{Style.RESET_ALL}")

        return code

    def _input_username(self, tab, username):
        print(f"{Fore.YELLOW}{EMOJI['INPUT']} 配置临时邮箱...{Style.RESET_ALL}")
        while True:
            if tab.ele("@id=pre_button"):
                tab.actions.click("@id=pre_button")
                time.sleep(0.5)
                tab.run_js('document.getElementById("pre_button").value = ""')
                time.sleep(0.5)
                tab.actions.input(username).key_down(Keys.ENTER).key_up(Keys.ENTER)
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} 邮箱配置完成{Style.RESET_ALL}")
                break
            time.sleep(1)

    def _get_latest_mail_code(self, tab):
        code = None
        print(f"{Fore.CYAN}{EMOJI['WAIT']} 等待验证邮件...{Style.RESET_ALL}")
        while True:
            new_mail = tab.ele("@class=mail")
            if new_mail:
                if new_mail.text:
                    print(f"{Fore.GREEN}{EMOJI['MAIL']} 收到新邮件{Style.RESET_ALL}")
                    tab.actions.click("@class=mail")
                    break
                else:
                    break
            time.sleep(1)

        if tab.ele("@class=overflow-auto mb-20"):
            print(f"{Fore.YELLOW}{EMOJI['SEARCH']} 正在提取验证码...{Style.RESET_ALL}")
            email_content = tab.ele("@class=overflow-auto mb-20").text
            verification_code = re.search(
                r"verification code is (\d{6})", email_content
            )
            if verification_code:
                code = verification_code.group(1)
                print(f"{Fore.GREEN}{EMOJI['CODE']} 验证码获取成功: {code}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}{EMOJI['ERROR']} 未找到验证码{Style.RESET_ALL}")

        return code

    def _cleanup_mail(self, tab):
        print(f"{Fore.CYAN}{EMOJI['CLEAN']} 清理邮箱...{Style.RESET_ALL}")
        if tab.ele("@id=delete_mail"):
            tab.actions.click("@id=delete_mail")
            time.sleep(1)

        if tab.ele("@id=confirm_mail"):
            tab.actions.click("@id=confirm_mail")
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} 邮箱清理完成{Style.RESET_ALL}")
