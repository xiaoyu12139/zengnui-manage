#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Windows文件监控服务
监控指定文件夹的文件变化（增加、删除、修改）
"""

import os
import sys
import time
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import win32serviceutil
import win32service
import win32event
import servicemanager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('file_monitor_service.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FileChangeHandler(FileSystemEventHandler):
    """文件变化处理器"""
    
    def __init__(self, watch_folder):
        super().__init__()
        self.watch_folder = watch_folder
        logger.info(f"开始监控文件夹: {watch_folder}")
    
    def on_created(self, event):
        """文件或文件夹被创建"""
        if not event.is_directory:
            logger.info(f"文件被创建: {event.src_path}")
            self.handle_file_change('created', event.src_path)
    
    def on_deleted(self, event):
        """文件或文件夹被删除"""
        if not event.is_directory:
            logger.info(f"文件被删除: {event.src_path}")
            self.handle_file_change('deleted', event.src_path)
    
    def on_modified(self, event):
        """文件或文件夹被修改"""
        if not event.is_directory:
            logger.info(f"文件被修改: {event.src_path}")
            self.handle_file_change('modified', event.src_path)
    
    def on_moved(self, event):
        """文件或文件夹被移动/重命名"""
        if not event.is_directory:
            logger.info(f"文件被移动: {event.src_path} -> {event.dest_path}")
            self.handle_file_change('moved', event.src_path, event.dest_path)
    
    def handle_file_change(self, action, src_path, dest_path=None):
        """处理文件变化事件"""
        try:
            # 在这里添加你的业务逻辑
            # 例如：发送通知、备份文件、触发其他操作等
            
            if action == 'created':
                logger.info(f"处理文件创建事件: {src_path}")
                # 添加文件创建后的处理逻辑
                
            elif action == 'deleted':
                logger.info(f"处理文件删除事件: {src_path}")
                # 添加文件删除后的处理逻辑
                
            elif action == 'modified':
                logger.info(f"处理文件修改事件: {src_path}")
                # 添加文件修改后的处理逻辑
                
            elif action == 'moved':
                logger.info(f"处理文件移动事件: {src_path} -> {dest_path}")
                # 添加文件移动后的处理逻辑
                
        except Exception as e:
            logger.error(f"处理文件变化事件时出错: {e}")

class FileMonitorService(win32serviceutil.ServiceFramework):
    """Windows文件监控服务"""
    
    _svc_name_ = "FileMonitorService"
    _svc_display_name_ = "文件监控服务"
    _svc_description_ = "监控指定文件夹的文件变化"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.observer = None
        
        # 配置监控的文件夹路径（可以根据需要修改）
        self.watch_folder = r"C:\Users\xiaoyu\Desktop\Code\zengnui-manage\utools"
        
        # 确保监控文件夹存在
        if not os.path.exists(self.watch_folder):
            logger.error(f"监控文件夹不存在: {self.watch_folder}")
            raise FileNotFoundError(f"监控文件夹不存在: {self.watch_folder}")
    
    def SvcStop(self):
        """停止服务"""
        logger.info("正在停止文件监控服务...")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        
        if self.observer:
            self.observer.stop()
            self.observer.join()
        
        logger.info("文件监控服务已停止")
    
    def SvcDoRun(self):
        """运行服务"""
        logger.info("启动文件监控服务...")
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        
        try:
            # 创建文件变化处理器
            event_handler = FileChangeHandler(self.watch_folder)
            
            # 创建观察者
            self.observer = Observer()
            self.observer.schedule(event_handler, self.watch_folder, recursive=True)
            
            # 启动观察者
            self.observer.start()
            logger.info(f"文件监控服务已启动，监控文件夹: {self.watch_folder}")
            
            # 等待停止信号
            win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
            
        except Exception as e:
            logger.error(f"服务运行时出错: {e}")
            servicemanager.LogErrorMsg(f"服务运行时出错: {e}")

def main():
    """主函数 - 用于调试和测试"""
    if len(sys.argv) == 1:
        # 如果没有参数，以调试模式运行
        logger.info("以调试模式运行文件监控服务...")
        print("以调试模式运行文件监控服务...")
        print("按 Ctrl+C 停止服务")
        
        try:
            # 配置监控的文件夹路径
            watch_folder = r"C:\Users\xiaoyu\Desktop\Code\zengnui-manage\utools"
            
            if not os.path.exists(watch_folder):
                error_msg = f"错误: 监控文件夹不存在: {watch_folder}"
                logger.error(error_msg)
                print(error_msg)
                return
            
            # 创建文件变化处理器
            event_handler = FileChangeHandler(watch_folder)
            
            # 创建观察者
            observer = Observer()
            observer.schedule(event_handler, watch_folder, recursive=True)
            
            # 启动观察者
            observer.start()
            start_msg = f"开始监控文件夹: {watch_folder}"
            logger.info(start_msg)
            print(start_msg)
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                stop_msg = "\n正在停止监控..."
                logger.info("正在停止监控...")
                print(stop_msg)
                observer.stop()
            
            observer.join()
            stopped_msg = "监控已停止"
            logger.info(stopped_msg)
            print(stopped_msg)
            
        except Exception as e:
            error_msg = f"运行时出错: {e}"
            logger.error(error_msg)
            print(error_msg)
    else:
        # 作为Windows服务运行
        win32serviceutil.HandleCommandLine(FileMonitorService)

if __name__ == '__main__':
    main()