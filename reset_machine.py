import os
import json
import uuid
import hashlib
import shutil
import sys
import ctypes
from colorama import Fore, Style, init

# 初始化colorama
init()

# 定义emoji和颜色常量
EMOJI = {
    "FILE": "📄",
    "BACKUP": "💾",
    "SUCCESS": "✅",
    "ERROR": "❌",
    "INFO": "ℹ️",
    "RESET": "🔄",
}


class MachineIDResetter:
    def __init__(self):
        self.setup_error_recovery()
        # 检查并提升权限
        if not self.check_admin_privileges():
            self.self_elevate()
            sys.exit(0)

        # 判断操作系统
        if os.name == "nt":  # Windows
            self.db_path = os.path.join(
                os.getenv("APPDATA"), "Cursor", "User", "globalStorage", "storage.json"
            )
        else:  # macOS
            self.db_path = os.path.expanduser(
                "~/Library/Application Support/Cursor/User/globalStorage/storage.json"
            )

    def setup_error_recovery(self):
        """设置全局错误恢复"""

        def handle_exception(exc_type, exc_value, exc_traceback):
            print(
                f"{Fore.RED}{EMOJI['ERROR']} 发生未处理的错误: {exc_value}{Style.RESET_ALL}"
            )
            input(f"{EMOJI['INFO']} 按回车键退出...")
            sys.exit(1)

        sys.excepthook = handle_exception

    def check_admin_privileges(self):
        """检查是否具有管理员权限"""
        try:
            if os.name == "nt":  # Windows
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:  # Unix-like
                return os.geteuid() == 0
        except:
            return False

    def self_elevate(self):
        """自动提升到管理员权限"""
        print(f"{Fore.YELLOW}{EMOJI['INFO']} 请求管理员权限...{Style.RESET_ALL}")
        if os.name == "nt":  # Windows
            script = os.path.abspath(sys.argv[0])
            params = " ".join(sys.argv[1:])
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{script}" {params}', None, 1
            )
        else:  # Unix-like
            os.system(f'sudo "{sys.executable}" "{os.path.abspath(sys.argv[0])}"')

    def set_readonly(self, filepath, readonly=True):
        """设置文件只读模式"""
        try:
            if os.name == "nt":  # Windows
                import stat

                if readonly:
                    os.chmod(filepath, stat.S_IREAD)
                else:
                    os.chmod(filepath, stat.S_IWRITE | stat.S_IREAD)
            else:  # Unix-like
                if readonly:
                    os.chmod(filepath, 0o444)
                else:
                    os.chmod(filepath, 0o644)
            return True
        except Exception as e:
            print(
                f"{Fore.RED}{EMOJI['ERROR']} 无法设置文件权限: {str(e)}{Style.RESET_ALL}"
            )
            return False

    def generate_new_ids(self):
        """生成新的机器ID"""
        # 生成新的UUID
        dev_device_id = str(uuid.uuid4())

        # 生成新的machineId (64个字符的十六进制)
        machine_id = hashlib.sha256(os.urandom(32)).hexdigest()

        # 生成新的macMachineId (128个字符的十六进制)
        mac_machine_id = hashlib.sha512(os.urandom(64)).hexdigest()

        # 生成新的sqmId
        sqm_id = "{" + str(uuid.uuid4()).upper() + "}"

        return {
            "telemetry.devDeviceId": dev_device_id,
            "telemetry.macMachineId": mac_machine_id,
            "telemetry.machineId": machine_id,
            "telemetry.sqmId": sqm_id,
        }

    def reset_machine_ids(self, set_readonly=True):
        """重置机器ID并备份原文件"""
        try:

            print(f"{Fore.CYAN}{EMOJI['INFO']} 正在检查配置文件...{Style.RESET_ALL}")

            # 检查文件是否存在
            if not os.path.exists(self.db_path):
                print(
                    f"{Fore.RED}{EMOJI['ERROR']} 配置文件不存在: {self.db_path}{Style.RESET_ALL}"
                )
                return False

            # 如果文件是只读的，先移除只读属性
            self.set_readonly(self.db_path, False)

            # 读取现有配置
            print(f"{Fore.CYAN}{EMOJI['FILE']} 读取当前配置...{Style.RESET_ALL}")
            with open(self.db_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            # 备份原文件
            backup_path = self.db_path + ".bak"
            print(
                f"{Fore.YELLOW}{EMOJI['BACKUP']} 创建配置备份: {backup_path}{Style.RESET_ALL}"
            )
            shutil.copy2(self.db_path, backup_path)

            # 生成新的ID
            print(f"{Fore.CYAN}{EMOJI['RESET']} 生成新的机器标识...{Style.RESET_ALL}")
            new_ids = self.generate_new_ids()

            # 更新配置
            config.update(new_ids)

            # 保存新配置
            print(f"{Fore.CYAN}{EMOJI['FILE']} 保存新配置...{Style.RESET_ALL}")
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)

            # 设置文件为只读（如果需要）
            if set_readonly:
                print(
                    f"{Fore.CYAN}{EMOJI['INFO']} 设置配置文件为只读模式...{Style.RESET_ALL}"
                )
                self.set_readonly(self.db_path, True)

            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} 机器标识重置成功！{Style.RESET_ALL}")
            print(f"\n{Fore.CYAN}新的机器标识:{Style.RESET_ALL}")
            for key, value in new_ids.items():
                print(f"{EMOJI['INFO']} {key}: {Fore.GREEN}{value}{Style.RESET_ALL}")

            return True

        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} 重置过程出错: {str(e)}{Style.RESET_ALL}")
            return False


if __name__ == "__main__":
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['RESET']} Cursor 机器标识重置工具{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")

    resetter = MachineIDResetter()
    resetter.reset_machine_ids()

    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    input(f"{EMOJI['INFO']} 按回车键退出...")
