# initalize the flask application


# enter the pyhton virtual env
source venv/Scripts/activate;

# flasky 环境变量设置
export FLASK_APP="touring.py";
export FLASK_DEBUG=1;
export FLASK_CONFIG="development";

# 邮件相关配置
export MAIL_SERVER="smtp.163.com";
export MAIL_USERNAME="egyonic001s";
export MAIL_PASSWORD="smg521";
export FLASKY_ADMIN="egyonic001s@163.com";
export MAIL_PORT=587;
export MAIL_USE_TLS=$False;
export MAIL_USE_SSL=$True;

