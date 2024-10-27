import os

import mutagen
from tqdm import tqdm


def scan_files_and_get_info(root_dir, music_extensions, delete_error_files):
	# 初始化两个列表分别存储正确和错误的文件信息
	correct_files_info = []
	error_files_info = []

	# 创建一个生成器，用于遍历音乐文件
	def music_files_generator(root_dir, extensions):
		for subdir, dirs, files in os.walk(root_dir):
			for file in files:
				if os.path.splitext(file)[1].lower() in extensions:
					yield os.path.join(subdir, file)

	# 使用生成器获取音乐文件路径列表
	music_files = list(music_files_generator(root_dir, music_extensions))
	total_files = len(music_files)
	print(f"扫描到 {total_files} 个音乐文件")

	# 使用tqdm显示进度
	for file_path in tqdm(music_files, desc="扫描音乐文件", total=total_files):
		try:
			audio = mutagen.File(file_path, easy=True)
			if audio is not None:
				info = {
					'文件路径': file_path,
					'标题': audio.get('title', [''])[0],
					'艺术家': audio.get('artist', [''])[0],
					'专辑': audio.get('album', [''])[0],
					'流派': audio.get('genre', [''])[0],
					'曲目编号': audio.get('tracknumber', [''])[0],
					'年份': audio.get('date', [''])[0],
				}
				print(info)
				correct_files_info.append(info)
		except Exception as e:
			if delete_error_files:
				print(f"删除错误文件：{file_path}")
				os.remove(file_path)
			else:
				error_info = {
					'文件路径': file_path,
					'错误信息': str(e),
				}
				error_files_info.append(error_info)

	print(f"处理完成，正确文件数：{len(correct_files_info)}, 错误文件数：{len(error_files_info)}")
	return correct_files_info, error_files_info
