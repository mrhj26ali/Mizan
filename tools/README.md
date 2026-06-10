# Mizan Tools

This folder contains the necessary tools for compiling the Mizan grammar.

## Setup Instructions

1. **Download the ANTLR4 complete JAR file:**
   - Download `antlr-4.13.2-complete.jar` from [antlr.org](https://www.antlr.org/download/antlr-4.13.2-complete.jar) and place it in this `tools/` folder.

2. **Create the alias batch file:**
   - Create a file named `init_antlr_alias.bat` in this `tools/` folder.
   - Add the following content to it (update the path if your project is located elsewhere):

```bat
@echo off

:: Set the path to the JAR file
set "ANTLR_JAR=C:\Users\DELL\Desktop\Projects\Mizan\tools\antlr-4.13.2-complete.jar"

:: Use the full path to doskey to ensure Windows finds it
C:\Windows\System32\doskey.exe antlr4=java -jar "%ANTLR_JAR%" $*
C:\Windows\System32\doskey.exe grun=java -cp ".;%ANTLR_JAR%" org.antlr.v4.gui.TestRig $*

echo ANTLR 4.13.2 Shortcuts Enabled!