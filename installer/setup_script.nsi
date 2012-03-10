; setup_script.nsi
; script for nxtIDE installer
;--------------------------------

	!include "MUI2.nsh"
	!define inst_icon "nxtIDE.ico"

; The name of the installer
Name "nxtIDE"

; The file to write
OutFile "nxtIDE_setup.exe"
; The default installation directory
InstallDir $PROGRAMFILES\nxtIDE

; Request application privileges for Windows Vista
RequestExecutionLevel admin

;--------------------------------
;Interface Settings

	!define MUI_ICON "${inst_icon}"
	!define MUI_HEADERIMAGE
	!define MUI_WELCOMEFINISHPAGE_BITMAP "nxtIDE_header.bmp"
	!define MUI_UNWELCOMEFINISHPAGE_BITMAP "nxtIDE_header.bmp"
	!define MUI_HEADERIMAGE_BITMAP "nxtIDE_header.bmp"
	!define MUI_ABORTWARNING

	!define MUI_WELCOMEPAGE_TITLE "Welcome to the nxtIDE Setup Wizard"
	!define MUI_WELCOMEPAGE_TEXT "Brought to you by XLC Team"


	!define MUI_FINISHPAGE_TITLE "nxtIDE was installed successfully."
	!define MUI_FINISHPAGE_TEXT "Ok, now let's begin to code."
	;!define MUI_FINISHPAGE_RUN
  ;!define MUI_FINISHPAGE_RUN_CHECKED
  ;!define MUI_FINISHPAGE_RUN_TEXT "Run program"
	;!define MUI_FINISHPAGE_RUN_FUNCTION "startnxted"


	;uninstall constants
	!define MUI_UNWELCOMEPAGE_TITLE "Welcome to the nxtIDE uninstall Wizard"
	!define MUI_UNWELCOMEPAGE_TEXT "Brought to you by XLC Team"
	
	!define MUI_UNFINISHPAGE_TITLE "nxtIDE was uninstalled successfully."
	!define MUI_UNFINISHPAGE_TEXT "Thank you for using nxtIDE."

;--------------------------------


;pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_DIRECTORY
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

  
;--------------------------------
;Languages
	!insertmacro MUI_LANGUAGE "English"
;--------------------------------





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
