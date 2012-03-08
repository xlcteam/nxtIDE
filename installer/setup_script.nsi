; setup_script.nsi

;--------------------------------

!include "MUI.nsh"

!define inst_icon "nxtIDE.ico"
; !define uninst_icon ""



; The name of the installer
Name "nxtIDE_setup.exe"

; The file to write
OutFile "nxtIDE_setup.exe"
; The default installation directory
InstallDir $PROGRAMFILES\nxtIDE

; Request application privileges for Windows Vista
RequestExecutionLevel admin

;--------------------------------

; Pages
icon "${inst_icon}"
; UninstallIcon "${uninst_icon}"

!insertmacro MUI_PAGE_WELCOME
;LangString PAGE_TITLE ${LANG_ENGLISH} "nxtIDE"
;LangString PAGE_SUBTITLE ${LANG_ENGLISH} "Brought to you by XLC Team"


;!insertmacro MUI_LANGUAGE "English"
Page directory
Page instfiles


UninstPage uninstConfirm
UninstPage instfiles

;-------------------------------

; The stuff to install
Section "..\build" ;No components page, name is not important
	SetShellVarContext all
  ; Set output path to the installation directory.
  SetOutPath $INSTDIR

  ; Put file there
  File /r nxtemu
  File /r nxted
  writeUninstaller "$INSTDIR\uninstall.exe"
  CreateDirectory "$SMPROGRAMS\nxtIDE"
  CreateDirectory "$INSTDIR\nxtemu\__progs__"
	AccessControl::GrantOnFile "$INSTDIR\nxtemu\" "(BU)" "FullAccess"
  ;AccessControl::GrantOnFile "$INSTDIR\nxtemu\__progs__" "(BU)" "FullAccess"
  AccessControl::GrantOnFile "$INSTDIR\nxted\" "(BU)" "FullAccess"
  CreateShortCut "$SMPROGRAMS\nxtIDE\Uninstall.lnk" "$INSTDIR\Uninstall.exe" "" "$INSTDIR\Uninstall.exe" 0

SectionEnd ; end the section


Section
	SetShellVarContext all
	SetOutPath "$INSTDIR\nxted\"
	CreateShortCut $DESKTOP\nxted.lnk $INSTDIR\nxted\nxted.exe 
SectionEnd


section
	SetShellVarContext all
	SetOutPath "$INSTDIR\nxted\"
	CreateShortCut "$SMPROGRAMS\nxtIDE\nxted.lnk" "$INSTDIR\nxted\nxted.exe" "" "$INSTDIR\nxted\nxted.exe" 0
SectionEnd


section
	SetShellVarContext all
	SetOutPath "$INSTDIR\nxtemu\"
	CreateShortCut "$SMPROGRAMS\nxtIDE\nxtemu.lnk" "$INSTDIR\nxtemu\nxtemu.exe" "" "$INSTDIR\nxtemu\nxtemu.exe" 0
SectionEnd	


Section
	SetShellVarContext all
	SetOutPath "$INSTDIR\nxtemu\"
	CreateShortCut $DESKTOP\nxtemu.lnk $INSTDIR\nxtemu\nxtemu.exe 
SectionEnd



section "Uninstall"
	SetShellVarContext all
 	Delete $INSTDIR\nxted\pynxc\nxc\win32\*.*
	RMDir  $INSTDIR\nxted\pynxc\nxc\win32
	RMDir  $INSTDIR\nxted\pynxc\nxc
	Delete $INSTDIR\nxted\pynxc\*.*
	RMDir  $INSTDIR\nxted\pynxc
	Delete $INSTDIR\nxted\*.*
	Delete $INSTDIR\nxtemu\*.*
	Delete $INSTDIR\nxtemu\__progs__\*.*
	RMDir  $INSTDIR\nxtemu\__progs__
	Delete $INSTDIR\nxtemu\floor\*.*
	RMDir  $INSTDIR\nxtemu\floor
	Delete $INSTDIR\nxtemu\icons\*.*
	RMDir  $INSTDIR\nxtemu\icons
	Delete $INSTDIR\nxtemu\theme\default\*.*
	RMDir  $INSTDIR\nxtemu\theme\default
	RMDir  $INSTDIR\nxtemu\theme	
	RMDir  $INSTDIR\nxtemu
	RMDir  $INSTDIR\nxted
	Delete $INSTDIR\uninstall.exe
	RMDir  $INSTDIR
	Delete "$DESKTOP\nxted.lnk"
	Delete "$DESKTOP\nxtemu.lnk"
	Delete "$SMPROGRAMS\nxtIDE\*.*"
	RmDir  "$SMPROGRAMS\nxtIDE"
sectionEnd
