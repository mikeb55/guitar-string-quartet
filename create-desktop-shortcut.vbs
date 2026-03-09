Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")

ScriptPath = FSO.GetParentFolderName(WScript.ScriptFullName)
HtaPath = ScriptPath & "\launch-gsq-engine.hta"

DesktopPath = WshShell.SpecialFolders("Desktop")
ShortcutPath = DesktopPath & "\Launch Guitar-String-Quartet Engine.lnk"

Set Shortcut = WshShell.CreateShortcut(ShortcutPath)
Shortcut.TargetPath = HtaPath
Shortcut.WorkingDirectory = ScriptPath
Shortcut.Description = "Menu launcher for the Guitar-String-Quartet master composition engine"
Shortcut.Save
