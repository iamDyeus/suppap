import subprocess
import os
import sys

class TaskScheduler:
    def __init__(self, os_type):
        self.os_type = os_type

    def schedule_task(self, task_name, interval):
        if self.os_type == 'Windows':
            self._schedule_windows(task_name, interval)
        elif self.os_type == 'Darwin':  # macOS
            self._schedule_macos(task_name, interval)
        else:  # Linux
            self._schedule_linux(task_name, interval)

    def setup_autostart(self):
        if self.os_type == 'Windows':
            self._setup_autostart_windows()
        elif self.os_type == 'Darwin':  # macOS
            self._setup_autostart_macos()
        else:  # Linux
            self._setup_autostart_linux()

    def ensure_task_running(self):
        if self.os_type == 'Windows':
            self._ensure_task_running_windows()
        elif self.os_type == 'Darwin':  # macOS
            self._ensure_task_running_macos()
        else:  # Linux
            self._ensure_task_running_linux()

    def _schedule_windows(self, task_name, interval):
        script_path = os.path.abspath(sys.argv[0])
        # Convert interval from seconds to minutes, ensuring a minimum of 1 minute
        interval_minutes = max(1, interval // 60)
        command = f'schtasks /create /tn {task_name} /tr "python {script_path}" /sc minute /mo {interval_minutes} /f'
        print(f"Running command: {command}")
        subprocess.run(command, shell=True, check=True)

    def _schedule_macos(self, script_path, interval):
        plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
        <dict>
            <key>Label</key>
            <string>com.wallpaperchanger</string>
            <key>ProgramArguments</key>
            <array>
                <string>/usr/bin/python3</string>
                <string>{script_path}</string>
            </array>
            <key>StartInterval</key>
            <integer>{interval}</integer>
        </dict>
        </plist>'''
        
        plist_path = os.path.expanduser('~/Library/LaunchAgents/com.wallpaperchanger.plist')
        with open(plist_path, 'w') as f:
            f.write(plist_content)
        
        subprocess.run(['launchctl', 'load', plist_path], check=True)

    def _schedule_linux(self, script_path, interval):
        cron_command = f"*/{interval // 60} * * * * /usr/bin/python3 {script_path}"
        current_crontab = subprocess.check_output('crontab -l', shell=True, universal_newlines=True)
        new_crontab = current_crontab + cron_command + '\n'
        subprocess.run('echo "{}" | crontab -'.format(new_crontab), shell=True, check=True)

    def _setup_autostart_windows(self):
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(key, "WallpaperChanger", 0, winreg.REG_SZ, sys.executable)
            winreg.CloseKey(key)
        except WindowsError:
            print("Unable to set up autostart on Windows")

    def _setup_autostart_macos(self):
        plist_path = os.path.expanduser('~/Library/LaunchAgents/com.wallpaperchanger.plist')
        plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
        <dict>
            <key>Label</key>
            <string>com.wallpaperchanger</string>
            <key>ProgramArguments</key>
            <array>
                <string>{sys.executable}</string>
                <string>{os.path.abspath(__file__)}</string>
            </array>
            <key>RunAtLoad</key>
            <true/>
        </dict>
        </plist>'''
        with open(plist_path, 'w') as f:
            f.write(plist_content)
        subprocess.run(['launchctl', 'load', plist_path], check=True)

    def _setup_autostart_linux(self):
        autostart_dir = os.path.expanduser('~/.config/autostart')
        if not os.path.exists(autostart_dir):
            os.makedirs(autostart_dir)
        desktop_file = os.path.join(autostart_dir, 'wallpaperchanger.desktop')
        with open(desktop_file, 'w') as f:
            f.write(f'''[Desktop Entry]
            Type=Application
            Name=WallpaperChanger
            Exec={sys.executable} {os.path.abspath(__file__)}
            Hidden=false
            NoDisplay=false
            X-GNOME-Autostart-enabled=true
            ''')

    def _ensure_task_running_windows(self):
        result = subprocess.run(['schtasks', '/query', '/tn', 'WallpaperChanger'], capture_output=True, text=True)
        if "ERROR: The system cannot find the file specified." in result.stderr:
            self.schedule_task("WallpaperChanger", 3600)  # Reschedule if task not found

    def _ensure_task_running_macos(self):
        result = subprocess.run(['launchctl', 'list', 'com.wallpaperchanger'], capture_output=True, text=True)
        if result.returncode != 0:
            self.schedule_task("com.wallpaperchanger", 3600)  # Reschedule if task not found

    def _ensure_task_running_linux(self):
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        if "WallpaperChanger" not in result.stdout:
            self.schedule_task("WallpaperChanger", 3600)  # Reschedule if task not found

    def remove_from_startup(self):
        """Remove the application from startup programs."""
        if self.os_type == 'Windows':
            self._remove_from_startup_windows()
        elif self.os_type == 'Darwin':  # macOS
            self._remove_from_startup_macos()
        else:  # Linux
            self._remove_from_startup_linux()

    def _remove_from_startup_windows(self):
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
            winreg.DeleteValue(key, "WallpaperChanger")
            winreg.CloseKey(key)
        except WindowsError:
            print("Unable to remove from startup on Windows")

    def _remove_from_startup_macos(self):
        plist_path = os.path.expanduser('~/Library/LaunchAgents/com.wallpaperchanger.plist')
        if os.path.exists(plist_path):
            os.remove(plist_path)
            subprocess.run(['launchctl', 'unload', plist_path], check=True)

    def _remove_from_startup_linux(self):
        autostart_file = os.path.expanduser('~/.config/autostart/wallpaperchanger.desktop')
        if os.path.exists(autostart_file):
            os.remove(autostart_file)

    def remove_task(self, task_name):
        """Remove the scheduled task."""
        if self.os_type == 'Windows':
            self._remove_task_windows(task_name)
        elif self.os_type == 'Darwin':  # macOS
            self._remove_task_macos(task_name)
        else:  # Linux
            self._remove_task_linux(task_name)

    def _remove_task_windows(self, task_name):
        subprocess.run(f'schtasks /delete /tn {task_name} /f', shell=True, check=True)

    def _remove_task_macos(self, task_name):
        plist_path = os.path.expanduser(f'~/Library/LaunchAgents/{task_name}.plist')
        if os.path.exists(plist_path):
            subprocess.run(['launchctl', 'unload', plist_path], check=True)
            os.remove(plist_path)

    def _remove_task_linux(self, task_name):
        # Remove the cron job
        current_crontab = subprocess.check_output('crontab -l', shell=True, universal_newlines=True)
        new_crontab = '\n'.join(line for line in current_crontab.splitlines() if task_name not in line)
        subprocess.run('echo "{}" | crontab -'.format(new_crontab), shell=True, check=True)
