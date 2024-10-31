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
        script_dir = os.path.dirname(script_path)
        
        # Create a batch file to run the script
        batch_path = os.path.join(script_dir, 'run_wallpaper_changer.bat')
        with open(batch_path, 'w') as f:
            f.write('@echo off\n')
            f.write(f'cd /d "{script_dir}"\n')
            f.write(f'python "{script_path}" --scheduled-run >> "{script_dir}\\wallpaper_changer.log" 2>&1\n')

        # Make the batch file executable
        os.chmod(batch_path, 0o755)

        # Convert interval from seconds to minutes
        interval_minutes = max(1, interval // 60)

        try:
            # First try to delete any existing task
            subprocess.run(f'schtasks /delete /tn "{task_name}" /f', 
                         shell=True, 
                         stderr=subprocess.DEVNULL,
                         stdout=subprocess.DEVNULL)
        except:
            pass  # Ignore if task doesn't exist

        # Create XML file for task definition
        xml_path = os.path.join(script_dir, 'task_definition.xml')
        xml_content = f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Wallpaper Changer Task</Description>
  </RegistrationInfo>
  <Triggers>
    <TimeTrigger>
      <Repetition>
        <Interval>PT{interval_minutes}M</Interval>
        <StopAtDurationEnd>false</StopAtDurationEnd>
      </Repetition>
      <StartBoundary>2024-01-01T00:00:00</StartBoundary>
      <Enabled>true</Enabled>
    </TimeTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>false</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{batch_path}</Command>
      <WorkingDirectory>{script_dir}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>"""

        with open(xml_path, 'w', encoding='utf-16') as f:
            f.write(xml_content)

        try:
            # Create the task using the XML definition
            result = subprocess.run(
                f'schtasks /create /tn "{task_name}" /xml "{xml_path}" /f',
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                raise Exception(f"Failed to create task: {result.stderr}")

            # Clean up the XML file
            os.remove(xml_path)
            
            print(f"Successfully created scheduled task: {task_name}")
            
        except Exception as e:
            print(f"Error creating scheduled task: {str(e)}")
            if os.path.exists(xml_path):
                os.remove(xml_path)
            raise

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
                <string>--scheduled-run</string>
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
        cron_command = f"*/{interval // 60} * * * * /usr/bin/python3 {script_path} --scheduled-run"
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
            try:
                subprocess.run(f'schtasks /delete /tn "{task_name}" /f', 
                             shell=True,
                             check=True,
                             capture_output=True)
                print(f"Successfully removed task: {task_name}")
            except subprocess.CalledProcessError as e:
                if "The system cannot find the file specified" not in str(e.stderr):
                    print(f"Error removing task: {str(e)}")

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
