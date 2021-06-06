@echo off
rem 在这种写法可读性好，也能执行多语句，但兼容性不太好
set varA=%1
@REM echo %varA%
if DEFINED  %1 (
    echo %varA% is A
    echo AAA
)

pause