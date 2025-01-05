import sqlite3
import os
from colorama import Fore, Style, init

# 初始化colorama
init()

# 定义emoji和颜色常量
EMOJI = {
    "DB": "🗄️",
    "UPDATE": "🔄",
    "SUCCESS": "✅",
    "ERROR": "❌",
    "WARN": "⚠️",
    "INFO": "ℹ️",
    "KEY": "🔑",
}


class CursorAuthManager:
    """Cursor认证信息管理器"""

    def __init__(self):
        # 判断操作系统
        if os.name == "nt":  # Windows
            self.db_path = os.path.join(
                os.getenv("APPDATA"), "Cursor", "User", "globalStorage", "state.vscdb"
            )
        else:  # macOS
            self.db_path = os.path.expanduser(
                "~/Library/Application Support/Cursor/User/globalStorage/state.vscdb"
            )

    def update_auth(self, email=None, access_token=None, refresh_token=None):
        """
        更新Cursor的认证信息
        :param email: 新的邮箱地址
        :param access_token: 新的访问令牌
        :param refresh_token: 新的刷新令牌
        :return: bool 是否成功更新
        """
        updates = []
        # 登录状态
        updates.append(("cursorAuth/cachedSignUpType", "Auth_0"))

        if email is not None:
            updates.append(("cursorAuth/cachedEmail", email))
        if access_token is not None:
            updates.append(("cursorAuth/accessToken", access_token))
        if refresh_token is not None:
            updates.append(("cursorAuth/refreshToken", refresh_token))

        if not updates:
            print(
                f"{Fore.YELLOW}{EMOJI['WARN']} 没有提供任何要更新的值{Style.RESET_ALL}"
            )
            return False

        conn = None
        try:
            print(f"{Fore.CYAN}{EMOJI['DB']} 连接到 Cursor 数据库...{Style.RESET_ALL}")
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            for key, value in updates:

                # 如果没有更新任何行,说明key不存在,执行插入
                # 检查 accessToken 是否存在
                check_query = f"SELECT COUNT(*) FROM itemTable WHERE key = ?"
                cursor.execute(check_query, (key,))
                if cursor.fetchone()[0] == 0:
                    insert_query = "INSERT INTO itemTable (key, value) VALUES (?, ?)"
                    cursor.execute(insert_query, (key, value))
                else:
                    update_query = "UPDATE itemTable SET value = ? WHERE key = ?"
                    cursor.execute(update_query, (value, key))

                if cursor.rowcount > 0:
                    print(
                        f"{Fore.GREEN}{EMOJI['SUCCESS']} {key.split('/')[-1]} 更新成功{Style.RESET_ALL}"
                    )
                else:
                    print(
                        f"{Fore.YELLOW}{EMOJI['WARN']} {key.split('/')[-1]} 未找到或值未变化{Style.RESET_ALL}"
                    )

            conn.commit()
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} 数据库更新完成{Style.RESET_ALL}")
            return True

        except sqlite3.Error as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} 数据库错误: {str(e)}{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} 发生错误: {str(e)}{Style.RESET_ALL}")
            return False
        finally:
            if conn:
                conn.close()
                print(f"{Fore.CYAN}{EMOJI['DB']} 数据库连接已关闭{Style.RESET_ALL}")
