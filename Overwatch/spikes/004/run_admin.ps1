$pythonPath = "C:\Users\willi\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none\python.exe"
$script = "C:\Users\willi\the-system\Overwatch\spikes\004\admin_test.py"
$ps = Start-Process -FilePath $pythonPath -ArgumentList "'$script'" -Verb RunAs -WindowStyle Hidden -PassThru -Wait
Write-Host "Exit code: $($ps.ExitCode)"
