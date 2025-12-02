import sys
import requests
import json
import re
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTextEdit, QFrame, QScrollArea,
                             QGroupBox, QProgressBar, QMessageBox, QTabWidget)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QUrl
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtGui import QFont, QPixmap, QIcon, QColor, QPalette, QImage, QPainter


class ServerStatusWorker(QThread):
    """工作线程，用于在后台获取服务器状态"""
    result_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, server_address):
        super().__init__()
        self.server_address = server_address
    
    def run(self):
        try:
            url = f"https://uapis.cn/api/v1/game/minecraft/serverstatus?server={self.server_address}"
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 正在请求: {url}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                # 转换API响应格式以匹配前端期望的格式
                formatted_data = {
                    "success": True,
                    "data": data
                }
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] API响应: {json.dumps(formatted_data, ensure_ascii=False, indent=2)}")
                self.result_ready.emit(formatted_data)
            else:
                error_msg = f"API请求失败: {response.status_code}"
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {error_msg}")
                self.error_occurred.emit(error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"网络错误: {str(e)}"
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {error_msg}")
            self.error_occurred.emit(error_msg)
        except Exception as e:
            error_msg = f"未知错误: {str(e)}"
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {error_msg}")
            self.error_occurred.emit(error_msg)


class PlayerInfoWorker(QThread):
    """工作线程，用于在后台获取玩家信息"""
    result_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, username):
        super().__init__()
        self.username = username
    
    def run(self):
        try:
            url = f"https://uapis.cn/api/v1/game/minecraft/userinfo?username={self.username}"
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 正在请求: {url}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                # 转换API响应格式以匹配前端期望的格式
                formatted_data = {
                    "success": True,
                    "data": data
                }
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] API响应: {json.dumps(formatted_data, ensure_ascii=False, indent=2)}")
                self.result_ready.emit(formatted_data)
            else:
                error_msg = f"API请求失败: {response.status_code}"
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {error_msg}")
                self.error_occurred.emit(error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"网络错误: {str(e)}"
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {error_msg}")
            self.error_occurred.emit(error_msg)
        except Exception as e:
            error_msg = f"未知错误: {str(e)}"
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {error_msg}")
            self.error_occurred.emit(error_msg)


class MinecraftStatusApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle('服务器状态读取器-byMVP')
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(700, 500)
        
        # 设置应用程序样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #000000;
            }
            QLineEdit {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #cccccc;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
            QGroupBox {
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 1ex;
                color: #2c3e50;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
                color: #000000;
            }
            QTextEdit {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #cccccc;
                border-radius: 4px;
            }
        """)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局（水平布局，包含侧边栏和主要内容）
        main_h_layout = QHBoxLayout(central_widget)
        main_h_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建侧边栏
        sidebar = QFrame()
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #3498db;
                border-right: 1px solid #2980b9;
            }
        """)
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        
        # 侧边栏标题
        sidebar_title = QLabel("信息")
        sidebar_title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-bottom: 1px solid white;
                padding-bottom: 10px;
                margin-bottom: 15px;
            }
        """)
        sidebar_layout.addWidget(sidebar_title)
        
        # API信息
        api_label = QLabel("免费API接口：")
        api_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold; margin-top: 10px;")
        sidebar_layout.addWidget(api_label)
        
        method_label = QLabel("GET")
        method_label.setStyleSheet("color: white; font-size: 12px; margin-left: 10px;")
        sidebar_layout.addWidget(method_label)
        
        url_label = QLabel("uapis.cn")
        url_label.setStyleSheet("color: white; font-size: 12px; margin-left: 10px;")
        sidebar_layout.addWidget(url_label)
        
        endpoint_label = QLabel("/api/v1/game/minecraft/serverstatus")
        endpoint_label.setStyleSheet("color: white; font-size: 11px; margin-left: 10px;")
        sidebar_layout.addWidget(endpoint_label)
        
        # 作者信息
        author_label = QLabel("程序作者：MVP")
        author_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
                margin-top: 30px;
                padding-top: 10px;
                border-top: 1px solid white;
            }
        """)
        sidebar_layout.addWidget(author_label)
        
        sidebar_layout.addStretch()
        
        # 主内容区域（垂直布局）
        main_content = QWidget()
        main_layout = QVBoxLayout(main_content)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title_label = QLabel('Minecraft信息查询工具')
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin: 15px;")
        main_layout.addWidget(title_label)
        
        # 创建标签页
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #cccccc;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #e0e0e0;
                border: 1px solid #cccccc;
                border-bottom-color: #cccccc;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #3498db;
                color: white;
            }
        """)
        
        # 服务器状态查询标签
        server_tab = QWidget()
        server_tab_layout = QVBoxLayout(server_tab)
        
        # 输入区域
        input_group = QGroupBox("服务器信息")
        input_layout = QHBoxLayout(input_group)
        
        self.server_input = QLineEdit()
        self.server_input.setPlaceholderText("输入服务器地址 (例如: hypixel.net 或 mc.example.com:25565)")
        self.server_input.returnPressed.connect(self.check_status)
        
        self.check_button = QPushButton("查询状态")
        self.check_button.clicked.connect(self.check_status)
        
        input_layout.addWidget(QLabel("服务器地址:"))
        input_layout.addWidget(self.server_input)
        input_layout.addWidget(self.check_button)
        
        server_tab_layout.addWidget(input_group)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        server_tab_layout.addWidget(self.progress_bar)
        
        # 结果显示区域
        result_group = QGroupBox("服务器状态")
        result_layout = QVBoxLayout(result_group)
        
        self.result_area = QScrollArea()
        self.result_area.setWidgetResizable(True)
        self.result_area.setStyleSheet("QScrollArea { border: none; }")
        
        self.result_content = QWidget()
        self.result_content_layout = QVBoxLayout(self.result_content)
        self.result_content_layout.setSpacing(10)
        self.result_content_layout.setContentsMargins(10, 10, 10, 10)
        
        self.result_area.setWidget(self.result_content)
        result_layout.addWidget(self.result_area)
        
        server_tab_layout.addWidget(result_group)
        
        # 玩家信息查询标签
        player_tab = QWidget()
        player_tab_layout = QVBoxLayout(player_tab)
        
        # 玩家信息输入区域
        player_input_group = QGroupBox("玩家信息")
        player_input_layout = QHBoxLayout(player_input_group)
        
        self.player_input = QLineEdit()
        self.player_input.setPlaceholderText("输入玩家名称或UUID")
        self.player_input.returnPressed.connect(self.check_player_info)
        
        self.player_check_button = QPushButton("查询玩家信息")
        self.player_check_button.clicked.connect(self.check_player_info)
        
        player_input_layout.addWidget(QLabel("玩家名称:"))
        player_input_layout.addWidget(self.player_input)
        player_input_layout.addWidget(self.player_check_button)
        
        player_tab_layout.addWidget(player_input_group)
        
        # 玩家信息进度条
        self.player_progress_bar = QProgressBar()
        self.player_progress_bar.setVisible(False)
        self.player_progress_bar.setRange(0, 0)  # Indeterminate progress
        player_tab_layout.addWidget(self.player_progress_bar)
        
        # 玩家信息结果显示区域
        player_result_group = QGroupBox("玩家信息")
        player_result_layout = QVBoxLayout(player_result_group)
        
        self.player_result_area = QScrollArea()
        self.player_result_area.setWidgetResizable(True)
        self.player_result_area.setStyleSheet("QScrollArea { border: none; }")
        
        self.player_result_content = QWidget()
        self.player_result_content_layout = QVBoxLayout(self.player_result_content)
        self.player_result_content_layout.setSpacing(10)
        self.player_result_content_layout.setContentsMargins(10, 10, 10, 10)
        
        self.player_result_area.setWidget(self.player_result_content)
        player_result_layout.addWidget(self.player_result_area)
        
        player_tab_layout.addWidget(player_result_group)
        
        # 添加标签页
        tab_widget.addTab(server_tab, "服务器状态")
        tab_widget.addTab(player_tab, "玩家信息")
        
        main_layout.addWidget(tab_widget)
        
        # 将侧边栏和主内容添加到主布局
        main_h_layout.addWidget(sidebar)
        main_h_layout.addWidget(main_content)
        
        # 状态栏
        status_bar = self.statusBar()
        if status_bar:
            status_bar.showMessage('就绪-MVP')
        
    def check_status(self):
        """检查服务器状态"""
        server_address = self.server_input.text().strip()
        
        if not server_address:
            QMessageBox.warning(self, "输入错误", "请输入服务器地址")
            return
            
        # 禁用按钮并显示进度条
        self.check_button.setEnabled(False)
        self.check_button.setText("查询中...-MVP")
        self.progress_bar.setVisible(True)
        status_bar = self.statusBar()
        if status_bar:
            status_bar.showMessage('正在查询服务器状态...')
        
        # 清空之前的结果
        self.clear_result_area()
        
        # 创建并启动工作线程
        self.worker = ServerStatusWorker(server_address)
        self.worker.result_ready.connect(self.display_result)
        self.worker.error_occurred.connect(self.show_error)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.start()
        
    def check_player_info(self):
        """检查玩家信息"""
        player_name = self.player_input.text().strip()
        
        if not player_name:
            QMessageBox.warning(self, "输入错误", "请输入玩家名称或UUID")
            return
            
        # 禁用按钮并显示进度条
        self.player_check_button.setEnabled(False)
        self.player_check_button.setText("查询中...")
        self.player_progress_bar.setVisible(True)
        status_bar = self.statusBar()
        if status_bar:
            status_bar.showMessage('正在查询玩家信息...')
        
        # 清空之前的结果
        self.clear_player_result_area()
        
        # 创建并启动工作线程
        self.player_worker = PlayerInfoWorker(player_name)
        self.player_worker.result_ready.connect(self.display_player_result)
        self.player_worker.error_occurred.connect(self.show_player_error)
        self.player_worker.finished.connect(self.on_player_worker_finished)
        self.player_worker.start()
        
    def clear_result_area(self):
        """清空结果区域"""
        for i in reversed(range(self.result_content_layout.count())):
            item = self.result_content_layout.itemAt(i)
            if item and item.widget():
                widget_item = item.widget()
                if widget_item:
                    widget_item.setParent(None)
                    
    def clear_player_result_area(self):
        """清空玩家信息结果区域"""
        for i in reversed(range(self.player_result_content_layout.count())):
            item = self.player_result_content_layout.itemAt(i)
            if item and item.widget():
                widget_item = item.widget()
                if widget_item:
                    widget_item.setParent(None)

                
    def display_result(self, data):
        """显示查询结果"""
        status_bar = self.statusBar()
        if status_bar:
            status_bar.showMessage('查询完成-MVP')
        
        if not data.get("success"):
            error_msg = data.get("message", "查询失败-MVP")
            self.show_error(f"API返回错误: {error_msg}")
            return
            
        result = data.get("data", {})
        
        # 显示基本信息
        info_frame = QFrame()
        info_layout = QVBoxLayout(info_frame)
        
        # 状态标题
        status_title = QLabel("服务器信息")
        status_title_font = QFont()
        status_title_font.setPointSize(16)
        status_title_font.setBold(True)
        status_title.setFont(status_title_font)
        status_title.setStyleSheet("color: #2c3e50;")
        info_layout.addWidget(status_title)
        
        # 在线状态
        online_status = result.get("online", False)
        status_text = "在线" if online_status else "离线"
        status_color = "#2ecc71" if online_status else "#e74c3c"
        
        status_label = QLabel(f"服务器状态: <span style='color: {status_color}; font-weight: bold;'>{status_text}</span>")
        status_label.setStyleSheet("font-size: 14px;")
        info_layout.addWidget(status_label)
        
        # IP地址和端口
        ip = result.get("ip", "未知")
        port = result.get("port", "未知")
        ip_label = QLabel(f"服务器地址: {ip}:{port}")
        ip_label.setStyleSheet("font-size: 14px;")
        info_layout.addWidget(ip_label)
        
        # 玩家数
        players = result.get("players", 0)
        max_players = result.get("max_players", 0)
        players_label = QLabel(f"玩家数量: {players} / {max_players}")
        players_label.setStyleSheet("font-size: 14px;")
        info_layout.addWidget(players_label)
        
        # 版本信息
        version = result.get("version", "未知")
        version_label = QLabel(f"游戏版本: {version}")
        version_label.setStyleSheet("font-size: 14px;")
        info_layout.addWidget(version_label)
        
        self.result_content_layout.addWidget(info_frame)
        
        # MOTD信息
        if online_status:
            motd_frame = QFrame()
            motd_layout = QVBoxLayout(motd_frame)
            
            motd_title = QLabel("MOTD信息")
            motd_title.setFont(status_title_font)
            motd_title.setStyleSheet("color: #2c3e50;")
            motd_layout.addWidget(motd_title)
            
            # 带格式的MOTD
            motd_html = result.get("motd_html", "无")
            motd_html_label = QLabel("带格式MOTD:")
            motd_html_label.setStyleSheet("font-size: 14px;")
            motd_layout.addWidget(motd_html_label)
            
            motd_html_display = QTextEdit()
            motd_html_display.setHtml(motd_html)
            motd_html_display.setMaximumHeight(100)
            motd_html_display.setReadOnly(True)
            motd_layout.addWidget(motd_html_display)
            
            # 纯文本MOTD
            motd_clean = result.get("motd_clean", "无")
            motd_clean_label = QLabel("纯文本MOTD:")
            motd_clean_label.setStyleSheet("font-size: 14px;")
            motd_layout.addWidget(motd_clean_label)
            
            motd_clean_display = QTextEdit()
            motd_clean_display.setPlainText(motd_clean)
            motd_clean_display.setMaximumHeight(100)
            motd_clean_display.setReadOnly(True)
            motd_layout.addWidget(motd_clean_display)
            
            self.result_content_layout.addWidget(motd_frame)
            
    def show_error(self, message):
        """显示错误信息"""
        status_bar = self.statusBar()
        if status_bar:
            status_bar.showMessage('查询失败')
        self.clear_result_area()
        
        error_frame = QFrame()
        error_layout = QVBoxLayout(error_frame)
        
        error_title = QLabel("错误")
        error_title_font = QFont()
        error_title_font.setPointSize(14)
        error_title_font.setBold(True)
        error_title.setFont(error_title_font)
        error_title.setStyleSheet("color: #e74c3c;")
        error_layout.addWidget(error_title)
        
        error_label = QLabel(message)
        error_label.setStyleSheet("color: #e74c3c; font-size: 13px;")
        error_label.setWordWrap(True)
        error_layout.addWidget(error_label)
        
        self.result_content_layout.addWidget(error_frame)
        
    def on_worker_finished(self):
        """工作线程完成时调用"""
        self.check_button.setEnabled(True)
        self.check_button.setText("查询状态")
        self.progress_bar.setVisible(False)
        
    def on_player_worker_finished(self):
        """玩家信息工作线程完成时调用"""
        self.player_check_button.setEnabled(True)
        self.player_check_button.setText("查询玩家信息")
        self.player_progress_bar.setVisible(False)
        
    def display_player_result(self, data):
        """显示玩家信息查询结果"""
        status_bar = self.statusBar()
        if status_bar:
            status_bar.showMessage('玩家信息查询完成')
        
        if not data.get("success"):
            error_msg = data.get("message", "查询失败")
            self.show_player_error(f"API返回错误: {error_msg}")
            return
            
        result = data.get("data", {})
        
        # 显示玩家基本信息
        info_frame = QFrame()
        info_layout = QVBoxLayout(info_frame)
        
        # 玩家信息标题
        info_title = QLabel("玩家信息")
        info_title_font = QFont()
        info_title_font.setPointSize(16)
        info_title_font.setBold(True)
        info_title.setFont(info_title_font)
        info_title.setStyleSheet("color: #2c3e50;")
        info_layout.addWidget(info_title)
        
        # 状态码
        code = result.get("code", "未知")
        code_label = QLabel(f"状态码: {code}")
        code_label.setStyleSheet("font-size: 14px;")
        info_layout.addWidget(code_label)
        
        # 玩家名称
        username = result.get("username", "未知")
        username_label = QLabel(f"玩家名称: {username}")
        username_label.setStyleSheet("font-size: 14px;")
        info_layout.addWidget(username_label)
        
        # 玩家UUID
        uuid = result.get("uuid", "未知")
        uuid_label = QLabel(f"玩家UUID: {uuid}")
        uuid_label.setStyleSheet("font-size: 14px;")
        info_layout.addWidget(uuid_label)
        
        # 玩家皮肤URL
        skin_url = result.get("skin_url", "无")
        skin_title = QLabel("皮肤信息:")
        skin_title.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
        info_layout.addWidget(skin_title)
        
        skin_url_label = QLabel(f"皮肤URL: {skin_url}")
        skin_url_label.setStyleSheet("font-size: 12px;")
        skin_url_label.setWordWrap(True)
        info_layout.addWidget(skin_url_label)
        
        # 如果有皮肤URL，尝试显示皮肤图片
        if skin_url and skin_url != "无":
            skin_display_label = QLabel("皮肤预览:")
            skin_display_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
            info_layout.addWidget(skin_display_label)
            
            # 添加皮肤图片显示区域
            self.skin_label = QLabel()
            self.skin_label.setStyleSheet("QLabel {background-color: #ecf0f1; border: 1px solid #bdc3c7; padding: 5px; min-height: 128px; min-width: 128px;}")
            self.skin_label.setAlignment(Qt.AlignCenter)
            self.skin_label.setText("正在加载皮肤...")
            info_layout.addWidget(self.skin_label)
            
            # 创建网络访问管理器来加载皮肤图片
            self.network_manager = QNetworkAccessManager()
            self.network_manager.finished.connect(lambda reply: self.on_skin_image_loaded(reply, self.skin_label))
            request = QNetworkRequest(QUrl(skin_url))
            self.network_manager.get(request)
        
        self.player_result_content_layout.addWidget(info_frame)
        
    def show_player_error(self, message):
        """显示玩家信息查询错误信息"""
        status_bar = self.statusBar()
        if status_bar:
            status_bar.showMessage('玩家信息查询失败')
        self.clear_player_result_area()
        
        error_frame = QFrame()
        error_layout = QVBoxLayout(error_frame)
        
        error_title = QLabel("错误")
        error_title_font = QFont()
        error_title_font.setPointSize(16)
        error_title_font.setBold(True)
        error_title.setFont(error_title_font)
        error_title.setStyleSheet("color: #e74c3c;")
        error_layout.addWidget(error_title)
        
        error_label = QLabel(message)
        error_label.setStyleSheet("color: #e74c3c; font-size: 14px;")
        error_label.setWordWrap(True)
        error_layout.addWidget(error_label)
        
        self.player_result_content_layout.addWidget(error_frame)
        
    def on_skin_image_loaded(self, reply, label):
        """皮肤图片加载完成后的处理"""
        if reply.error():
            label.setText("皮肤加载失败") 
            return
            
        image_data = reply.readAll()
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        
        if not pixmap.isNull():
            # 缩放图片以适应显示区域
            pixmap = pixmap.scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(pixmap)
        else:
            label.setText("皮肤加载失败")
            
        reply.deleteLater()


def main():
    app = QApplication(sys.argv)
    window = MinecraftStatusApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()