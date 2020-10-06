############################################################################################
#      NSIS Installation Script created by NSIS Quick Setup Script Generator v1.09.18
#               Entirely Edited with NullSoft Scriptable Installation System                
#              by Vlasis K. Barkas aka Red Wine red_wine@freemail.gr Sep 2006               
############################################################################################
!addplugindir "${NSISDIR}\Plugins"

!define APP_NAME "TritonAuth"
!define COMP_NAME "Dániel Derzsi"
!define WEB_SITE "https://tohka.us"
!define VERSION "10.00.00.00"
!define COPYRIGHT "© Dániel Derzsi 2020"
!define DESCRIPTION "TritonAuth"
!define INSTALLER_NAME "tritonauth_setup.exe"
!define MAIN_APP_EXE "tritonauth_setup.exe"
!define INSTALL_TYPE "SetShellVarContext all"
!define REG_ROOT "HKLM"
!define REG_APP_PATH "Software\Microsoft\Windows\CurrentVersion\App Paths\${MAIN_APP_EXE}"
!define UNINSTALL_PATH "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"


######################################################################

VIProductVersion  "${VERSION}"
VIAddVersionKey "ProductName"  "${APP_NAME}"
VIAddVersionKey "CompanyName"  "${COMP_NAME}"
VIAddVersionKey "LegalCopyright"  "${COPYRIGHT}"
VIAddVersionKey "FileDescription"  "${DESCRIPTION}"
VIAddVersionKey "FileVersion"  "${VERSION}"

######################################################################

SetCompressor ZLIB
Name "${APP_NAME}"
Caption "${APP_NAME}"
OutFile "${INSTALLER_NAME}"
BrandingText "${APP_NAME}"
XPStyle on
InstallDirRegKey "${REG_ROOT}" "${REG_APP_PATH}" ""
InstallDir "$PROGRAMFILES\TritonAuth"

######################################################################

!include "MUI2.nsh"

!define MUI_ICON "icon.ico"

!define MUI_ABORTWARNING
!define MUI_UNABORTWARNING

!insertmacro MUI_PAGE_WELCOME

!ifdef LICENSE_TXT
!insertmacro MUI_PAGE_LICENSE "${LICENSE_TXT}"
!endif

!insertmacro MUI_PAGE_DIRECTORY

!ifdef REG_START_MENU
!define MUI_STARTMENUPAGE_NODISABLE
!define MUI_STARTMENUPAGE_DEFAULTFOLDER "TritonAuth"
!define MUI_STARTMENUPAGE_REGISTRY_ROOT "${REG_ROOT}"
!define MUI_STARTMENUPAGE_REGISTRY_KEY "${UNINSTALL_PATH}"
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "${REG_START_MENU}"
!insertmacro MUI_PAGE_STARTMENU Application $SM_Folder
!endif

!insertmacro MUI_PAGE_INSTFILES

!insertmacro MUI_UNPAGE_CONFIRM

!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

######################################################################

Section -MainProgram
${INSTALL_TYPE}
SetOverwrite ifnewer
SetOutPath "$INSTDIR"
AccessControl::GrantOnFile "$INSTDIR" "(S-1-1-0)" "ListDirectory + GenericRead + GenericExecute + GenericWrite" 
AccessControl::EnableFileInheritance "$INSTDIR"
File "dist\TritonAuth.exe"
File "icon.ico"
File /r "..\icons"
CreateShortCut "$DESKTOP\TritonAuth.lnk" "$INSTDIR\TritonAuth.exe" "" "$INSTDIR\icon.ico" 0

WriteUninstaller "$INSTDIR\uninstall.exe"

WriteRegStr ${REG_ROOT} "${REG_APP_PATH}" "" "$INSTDIR\${MAIN_APP_EXE}"
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "DisplayName" "${APP_NAME}"
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "UninstallString" "$INSTDIR\uninstall.exe"
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "DisplayIcon" "$INSTDIR\${MAIN_APP_EXE}"
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "DisplayVersion" "${VERSION}"
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "Publisher" "${COMP_NAME}"

ExecShell "" "$InstDir\TritonAuth.exe"
Quit
SectionEnd

######################################################################

Section Uninstall
${INSTALL_TYPE}
Delete /REBOOTOK "$INSTDIR\TritonAuth.exe"
Delete /REBOOTOK "$INSTDIR\uninstall.exe"
RMDir /R /REBOOTOK "$INSTDIR\resources"
RMDir /R /REBOOTOK "$INSTDIR\user"

RMDir /R /REBOOTOK "$INSTDIR"

Delete /REBOOTOK "$DESKTOP\${APP_NAME}.lnk"

Delete /REBOOTOK "$DESKTOP\${APP_NAME}.lnk"
RMDir /R /REBOOTOK "$SMPROGRAMS\TritonAuth"

DeleteRegKey ${REG_ROOT} "${REG_APP_PATH}"
DeleteRegKey ${REG_ROOT} "${UNINSTALL_PATH}"
SectionEnd

######################################################################

