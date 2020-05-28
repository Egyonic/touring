
venv/Scripts/activate.bat;

# powershell 中的环境变量设置
$env:FLASK_APP="touring.py";
$env:FLASK_DEBUG=1;
$env:FLASK_CONFIG="development";


$env:FLASKY_ADMIN="egyonic001s@163.com";


echo "环境变量设置完毕"
echo "进入局部Python虚拟环境"