#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
明日方舟自动化系统测试脚本
用于测试各个功能模块和整体系统性能
"""
import os
import time
import logging
import argparse
import traceback
from datetime import datetime

# 导入功能模块
from modules.emulator import EmulatorController
from modules.image_recognition import ImageRecognizer
from modules.game_controller import GameController
from modules.arknights_login import ArknightsLogin
from modules.arknights_recruitment import ArknightsRecruitment
from modules.arknights_base import ArknightsBase
from modules.arknights_combat import ArknightsCombat
from modules.arknights_reward import ArknightsReward
from main import ArknightsAuto

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_results.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('TestRunner')

class TestRunner:
    """测试运行器类，用于执行各种测试"""
    
    def __init__(self):
        """初始化测试运行器"""
        self.results = {}
        logger.info("测试运行器初始化完成")
    
    def test_emulator_connection(self):
        """
        测试模拟器连接模块
        
        Returns:
            bool: 测试是否通过
        """
        logger.info("开始测试模拟器连接模块...")
        start_time = time.time()
        
        try:
            # 创建模拟器连接器
            emulator = EmulatorController()
            
            # 测试连接
            connected = emulator.connect()
            if not connected:
                logger.error("连接模拟器失败")
                return False
            
            # 获取设备信息
            device_info = emulator.get_device_info()
            logger.info(f"设备信息: {device_info}")
            
            # 测试截图
            screenshot = emulator.take_screenshot("test_screenshot.png")
            if screenshot is None:
                logger.error("截取屏幕截图失败")
                return False
            
            # 测试点击
            emulator.tap(500, 500)
            
            # 测试滑动
            emulator.swipe(500, 700, 500, 300, 300)
            
            # 断开连接
            emulator.disconnect()
            
            elapsed_time = time.time() - start_time
            logger.info(f"模拟器连接模块测试完成，耗时: {elapsed_time:.2f}秒")
            
            self.results["emulator_connection"] = {
                "status": "通过",
                "time": elapsed_time
            }
            return True
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(f"模拟器连接模块测试失败: {str(e)}")
            logger.error(traceback.format_exc())
            
            self.results["emulator_connection"] = {
                "status": "失败",
                "time": elapsed_time,
                "error": str(e)
            }
            return False
    
    def test_image_recognition(self):
        """
        测试图像识别模块
        
        Returns:
            bool: 测试是否通过
        """
        logger.info("开始测试图像识别模块...")
        start_time = time.time()
        
        try:
            # 创建图像识别器
            recognizer = ImageRecognizer("assets/templates")
            
            # 测试加载模板
            if os.path.isdir("assets/templates"):
                count = recognizer.load_templates("assets/templates")
                logger.info(f"已加载 {count} 个模板")
            
            # 测试图像处理
            if os.path.isfile("test_screenshot.png"):
                # 测试模板匹配
                for template_name in recognizer.templates:
                    success, position, score = recognizer.match_template("test_screenshot.png", template_name)
                    logger.info(f"模板 {template_name}: 匹配结果={success}, 位置={position}, 得分={score:.4f}")
                
                # 测试颜色查找
                positions = recognizer.find_color("test_screenshot.png", (255, 0, 0), 50)
                logger.info(f"找到 {len(positions)} 个红色像素")
                
                # 测试文本区域检测
                areas = recognizer.detect_text_area("test_screenshot.png")
                logger.info(f"检测到 {len(areas)} 个可能的文本区域")
            
            elapsed_time = time.time() - start_time
            logger.info(f"图像识别模块测试完成，耗时: {elapsed_time:.2f}秒")
            
            self.results["image_recognition"] = {
                "status": "通过",
                "time": elapsed_time
            }
            return True
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(f"图像识别模块测试失败: {str(e)}")
            logger.error(traceback.format_exc())
            
            self.results["image_recognition"] = {
                "status": "失败",
                "time": elapsed_time,
                "error": str(e)
            }
            return False
    
    def test_game_controller(self):
        """
        测试游戏控制器模块
        
        Returns:
            bool: 测试是否通过
        """
        logger.info("开始测试游戏控制器模块...")
        start_time = time.time()
        
        try:
            # 创建游戏控制器
            controller = GameController()
            
            # 测试连接
            connected = controller.connect_emulator()
            if not connected:
                logger.error("连接模拟器失败")
                return False
            
            # 测试截图
            controller.take_screenshot()
            
            # 测试点击
            controller.tap(500, 500)
            
            # 测试滑动
            controller.swipe(500, 700, 500, 300, 300)
            
            # 测试等待屏幕稳定
            stable = controller.wait_stable_screen(max_retries=3)
            logger.info(f"屏幕稳定: {stable}")
            
            elapsed_time = time.time() - start_time
            logger.info(f"游戏控制器模块测试完成，耗时: {elapsed_time:.2f}秒")
            
            self.results["game_controller"] = {
                "status": "通过",
                "time": elapsed_time
            }
            return True
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(f"游戏控制器模块测试失败: {str(e)}")
            logger.error(traceback.format_exc())
            
            self.results["game_controller"] = {
                "status": "失败",
                "time": elapsed_time,
                "error": str(e)
            }
            return False
    
    def test_login_module(self):
        """
        测试登录模块
        
        Returns:
            bool: 测试是否通过
        """
        logger.info("开始测试登录模块...")
        start_time = time.time()
        
        try:
            # 创建登录模块
            login = ArknightsLogin()
            
            # 测试连接
            connected = login.connect()
            if not connected:
                logger.error("连接模拟器失败")
                return False
            
            # 测试启动游戏
            started = login.start_game(wait_time=10)
            logger.info(f"游戏启动: {started}")
            
            # 测试登录
            if started:
                logged_in = login.login()
                logger.info(f"登录结果: {logged_in}")
            
            elapsed_time = time.time() - start_time
            logger.info(f"登录模块测试完成，耗时: {elapsed_time:.2f}秒")
            
            self.results["login_module"] = {
                "status": "通过",
                "time": elapsed_time
            }
            return True
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(f"登录模块测试失败: {str(e)}")
            logger.error(traceback.format_exc())
            
            self.results["login_module"] = {
                "status": "失败",
                "time": elapsed_time,
                "error": str(e)
            }
            return False
    
    def test_recruitment_module(self):
        """
        测试公开招募模块
        
        Returns:
            bool: 测试是否通过
        """
        logger.info("开始测试公开招募模块...")
        start_time = time.time()
        
        try:
            # 创建公开招募模块
            recruitment = ArknightsRecruitment()
            
            # 测试连接
            connected = recruitment.controller.connect_emulator()
            if not connected:
                logger.error("连接模拟器失败")
                return False
            
            # 测试导航到公开招募界面
            navigated = recruitment.navigate_to_recruitment()
            logger.info(f"导航到公开招募界面: {navigated}")
            
            # 测试检查招募槽位
            if navigated:
                empty_positions, finished_positions = recruitment.check_recruitment_slots()
                logger.info(f"空闲槽位: {len(empty_positions)}, 已完成槽位: {len(finished_positions)}")
                
                # 测试收取已完成的招募
                if finished_positions:
                    collected = recruitment.collect_finished_recruitment(finished_positions)
                    logger.info(f"收取已完成招募: {collected}")
                
                # 测试开始新的招募
                if empty_positions:
                    started = recruitment.start_new_recruitment(empty_positions, use_expedited=False)
                    logger.info(f"开始新的招募: {started}")
            
            # 返回主界面
            recruitment.return_to_main()
            
            elapsed_time = time.time() - start_time
            logger.info(f"公开招募模块测试完成，耗时: {elapsed_time:.2f}秒")
            
            self.results["recruitment_module"] = {
                "status": "通过",
                "time": elapsed_time
            }
            return True
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(f"公开招募模块测试失败: {str(e)}")
            logger.error(traceback.format_exc())
            
            self.results["recruitment_module"] = {
                "status": "失败",
                "time": elapsed_time,
                "error": str(e)
            }
            return False
    
    def test_base_module(self):
        """
        测试基建模块
        
        Returns:
            bool: 测试是否通过
        """
        logger.info("开始测试基建模块...")
        start_time = time.time()
        
        try:
            # 创建基建模块
            base = ArknightsBase()
            
            # 测试连接
            connected = base.controller.connect_emulator()
            if not connected:
                logger.error("连接模拟器失败")
                return False
            
            # 测试导航到基建界面
            navigated = base.navigate_to_base()
            logger.info(f"导航到基建界面: {navigated}")
            
            # 测试收取所有资源
            if navigated:
                collected = base.collect_all_resources()
                logger.info(f"收取所有资源: {collected}")
            
            # 返回主界面
            base.return_to_main()
            
            elapsed_time = time.time() - start_time
            logger.info(f"基建模块测试完成，耗时: {elapsed_time:.2f}秒")
            
            self.results["base_module"] = {
                "status": "通过",
                "time": elapsed_time
            }
            return True
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(f"基建模块测试失败: {str(e)}")
            logger.error(traceback.format_exc())
            
            self.results["base_module"] = {
                "status": "失败",
                "time": elapsed_time,
                "error": str(e)
            }
            return False
    
    def test_combat_module(self):
        """
        测试作战模块
        
        Returns:
            bool: 测试是否通过
        """
        logger.info("开始测试作战模块...")
        start_time = time.time()
        
        try:
            # 创建作战模块
            combat = ArknightsCombat()
            
            # 测试连接
            connected = combat.controller.connect_emulator()
            if not connected:
                logger.error("连接模拟器失败")
                return False
            
            # 测试导航到作战界面
            navigated = combat.navigate_to_combat()
            logger.info(f"导航到作战界面: {navigated}")
            
            # 测试检查自动部署
            if navigated:
                auto_deploy = combat.check_auto_deploy()
                logger.info(f"自动部署状态: {auto_deploy}")
            
            # 返回主界面
            combat.return_to_main()
            
            elapsed_time = time.time() - start_time
            logger.info(f"作战模块测试完成，耗时: {elapsed_time:.2f}秒")
            
            self.results["combat_module"] = {
                "status": "通过",
                "time": elapsed_time
            }
            return True
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(f"作战模块测试失败: {str(e)}")
            logger.error(traceback.format_exc())
            
            self.results["combat_module"] = {
                "status": "失败",
                "time": elapsed_time,
                "error": str(e)
            }
            return False
    
    def test_reward_module(self):
        """
        测试奖励模块
        
        Returns:
            bool: 测试是否通过
        """
        logger.info("开始测试奖励模块...")
        start_time = time.time()
        
        try:
            # 创建奖励模块
            reward = ArknightsReward()
            
            # 测试连接
            connected = reward.controller.connect_emulator()
            if not connected:
                logger.error("连接模拟器失败")
                return False
            
            # 测试收集日常任务奖励
            collected = reward.collect_daily_missions()
            logger.info(f"收集日常任务奖励: {collected}")
            
            # 返回主界面
            reward.return_to_main()
            
            elapsed_time = time.time() - start_time
            logger.info(f"奖励模块测试完成，耗时: {elapsed_time:.2f}秒")
            
            self.results["reward_module"] = {
                "status": "通过",
                "time": elapsed_time
            }
            return True
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(f"奖励模块测试失败: {str(e)}")
            logger.error(traceback.format_exc())
            
            self.results["reward_module"] = {
                "status": "失败",
                "time": elapsed_time,
                "error": str(e)
            }
            return False
    
    def test_main_program(self):
        """
        测试主程序
        
        Returns:
            bool: 测试是否通过
        """
        logger.info("开始测试主程序...")
        start_time = time.time()
        
        try:
            # 创建主程序实例
            auto = ArknightsAuto()
            
            # 测试连接
            connected = auto.connect()
            if not connected:
                logger.error("连接模拟器失败")
                return False
            
            # 修改配置，只执行登录任务
            auto.config["tasks"] = {
                "login": True,
                "recruitment": False,
                "base": False,
                "combat": False,
                "reward": False
            }
            
            # 运行任务
            success = auto.run_tasks()
            logger.info(f"任务执行结果: {success}")
            
            elapsed_time = time.time() - start_time
            logger.info(f"主程序测试完成，耗时: {elapsed_time:.2f}秒")
            
            self.results["main_program"] = {
                "status": "通过",
                "time": elapsed_time
            }
            return True
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(f"主程序测试失败: {str(e)}")
            logger.error(traceback.format_exc())
            
            self.results["main_program"] = {
                "status": "失败",
                "time": elapsed_time,
                "error": str(e)
            }
            return False
    
    def run_all_tests(self):
        """
        运行所有测试
        
        Returns:
            dict: 测试结果
        """
        logger.info("开始运行所有测试...")
        start_time = time.time()
        
        # 运行各个模块的测试
        self.test_emulator_connection()
        self.test_image_recognition()
        self.test_game_controller()

