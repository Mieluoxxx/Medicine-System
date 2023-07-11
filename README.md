# Medicine-System

药物管理系统--数据库课程设计
flask + pymysql + flask_sqlachemy

本项目由poetry打包
安装方式为
```bash
poetry install
```
使用方式为
```bash
poetry shell
cd medicine_system
# 注意修改config.py中的mysql配置
flask init-static && flask init-db && flask init-sql && flask init-trigger
python app.py
```