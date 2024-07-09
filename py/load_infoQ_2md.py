import os
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def download_image(image_url, folder_path):
	"""
	下载图片并保存到指定文件夹
	"""
	response = requests.get(image_url, stream=True)
	if response.status_code == 200:
		filename = os.path.basename(urlparse(image_url).path)
		filepath = os.path.join(folder_path, filename)
		with open(filepath, 'wb') as f:
			for chunk in response.iter_content(1024):
				f.write(chunk)
		return filename
	return None


def process_code_elements(content):
	"""
	处理代码块元素，确保每个 <code> 元素后都有一个换行符
	"""
	for code in content.find_all('code'):
		code.insert_after('\n')


def convert_article_to_md(url, output_dir):
	"""
	从指定网站下载文章并转换为 Markdown 格式，保存标题和目录样式，下载图片并替换图片引用路径
	"""
	# 设置 Selenium WebDriver
	options = Options()
	options.add_argument('--headless')  # 无头模式
	options.add_argument('--disable-gpu')
	options.add_argument(
		"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
	service = Service()
	driver = webdriver.Chrome(service=service, options=options)

	try:
		driver.get(url)

		# 确定使用哪个CSS类来定位主要内容
		if 'xie.infoq.cn' in urlparse(url).netloc:
			content_class = 'main'
		else:
			content_class = 'article-main'

		# 等待页面完全加载
		WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.CLASS_NAME, content_class))
		)

		# 获取页面源码并使用 BeautifulSoup 解析
		soup = BeautifulSoup(driver.page_source, 'html.parser')

		# 定位主要内容（class="article-main"）
		content = soup.find('div', class_=content_class)

		if content:
			# 获取文章标题
			title = soup.find('title').text.strip()

			# 创建一个文件夹来存储图片
			images_folder = os.path.join(output_dir, title, ".images")
			os.makedirs(images_folder, exist_ok=True)

			process_code_elements(content)

			# 下载并替换图片路径
			for img in content.find_all('img'):
				img_url = urljoin(url, img['src'])
				if not img_url.startswith('http'):
					continue
				img_filename = download_image(img_url, images_folder)
				if img_filename:
					img['src'] = os.path.join(".images", img_filename)

			# 将 HTML 转换为 Markdown
			article_md = md(str(content), heading_style="ATX")

			# 保存 Markdown 文件
			md_file_path = os.path.join(output_dir, title, f"{title}.md")
			with open(md_file_path, 'w', encoding='utf-8') as md_file:
				md_file.write(article_md)

			print(f"文章已保存为 {md_file_path}")
		else:
			print("未找到 class 'article-main' 的主要内容")

	except TimeoutException:
		print("页面加载超时。请检查URL是否正确或网络连接。")
	except WebDriverException as e:
		print(f"WebDriver 出现问题：{e}")
	except Exception as e:
		print(f"发生错误：{e}")
	finally:
		driver.quit()


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("用法: python script.py <文章URL>")
		sys.exit(1)

	article_url = sys.argv[1]
	# article_url = " https://www.infoq.cn/article/QjlXW9yE3uweDJdqgY3a"
	output_directory = "./note"

	# 创建输出目录
	Path(output_directory).mkdir(parents=True, exist_ok=True)

	convert_article_to_md(article_url, output_directory)
