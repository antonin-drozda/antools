set /p CONFIRM="Do you want to create commit to Git? (y/N): "
if /i "%CONFIRM%"=="y" (
    :: Get library version dynamically
    echo Cau
) else (
    echo Ahoj
)