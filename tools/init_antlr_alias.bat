@echo off

:: Set the path to the JAR file
set "ANTLR_JAR=C:\Users\DELL\Desktop\Projects\Mizan\tools\antlr-4.13.2-complete.jar"

:: Use the full path to doskey to ensure Windows finds it
C:\Windows\System32\doskey.exe antlr4=java -jar "%ANTLR_JAR%" $*
C:\Windows\System32\doskey.exe grun=java -cp ".;%ANTLR_JAR%" org.antlr.v4.gui.TestRig $*

echo ANTLR 4.13.2 Shortcuts Enabled!