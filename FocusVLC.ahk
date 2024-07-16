Persistent
SetTimer(FocusVLC,1000) ; Check every second
return

FocusVLC()
{ ; V1toV2: Added bracket
global ; V1toV2: Made function global
ErrorLevel := ProcessExist("vlc.exe") ; Check if VLC is running
if (ErrorLevel) ; If VLC is running (ErrorLevel is non-zero)
{
    if !WinActive("ahk_exe vlc.exe") ; If VLC is not the active window
    {
        WinActivate("ahk_exe vlc.exe") ; Activate VLC
    }
}
return
} ; V1toV2: Added bracket in the end
