import os
import shutil

from tqdm import tqdm


# 检查并创建艺术家文件夹，确保文件夹名称不包含空格
def check_and_create_artist_folder(artist, root_dir):
	artist_folder = os.path.join(root_dir, artist.strip())
	if not os.path.exists(artist_folder):
		os.makedirs(artist_folder)
	return artist_folder


# 检查并创建重复文件文件夹
def check_and_create_same_file_folder(root_dir):
	same_file_folder = os.path.join(root_dir, 'a_same_file')
	if not os.path.exists(same_file_folder):
		os.makedirs(same_file_folder)
	return same_file_folder


# 根据艺术家分组并移动文件
def group_and_move_files(files_info, root_dir):
	files_to_move = [(row['文件路径'], row['艺术家'].strip()) for row in files_info]

	same_file_folder = check_and_create_same_file_folder(root_dir)
	same_file_count = 0

	for file_path, artist in tqdm(files_to_move, desc="检查并移动文件到对应位置"):
		artist_folder = check_and_create_artist_folder(artist, root_dir)
		file_name = os.path.basename(file_path)
		target_file_path = os.path.join(artist_folder, file_name)

		# 检查文件是否已经在目标位置
		print(f"检查文件： {file_path}  是否需要移动")
		if os.path.dirname(file_path) != artist_folder:
			if os.path.exists(target_file_path):
				same_file_count += 1
				# 如果目标位置已存在同名文件，则移动到same_file文件夹
				shutil.move(file_path, os.path.join(same_file_folder, file_name))
				print(f"文件: {file_name} 重复，已移动到文件夹: {same_file_folder} ")
			else:
				shutil.move(file_path, artist_folder)
				print(f"已移动到{artist_folder}:  {file_name} ")
		else:
			print(f"文件 {file_name}  已存在于正确位置: {target_file_path}")

	print(f"已移动到same_file文件夹的文件数量: {same_file_count}")
	if same_file_count == 0:
		os.rmdir(same_file_folder)


# 删除空文件夹
def delete_empty_folders(root_dir):
	for folder_name in tqdm(os.listdir(root_dir), desc="扫描文件夹，并删除空文件夹"):
		folder_path = os.path.join(root_dir, folder_name)
		if os.path.isdir(folder_path) and not os.listdir(folder_path):
			os.rmdir(folder_path)
			print(f"已删除空文件夹: {folder_path}")


def move_files(root_dir, files_info):
	group_and_move_files(files_info, root_dir)
	delete_empty_folders(root_dir)
