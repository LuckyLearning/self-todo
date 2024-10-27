from music.src.move_files import move_files
from music.src.scan_files import scan_files_and_get_info

# 定义配置常量
ROOT_DIR = 'E:\\Music'
MUSIC_EXTENSIONS = ['.mp3', '.flac', '.wav', '.ogg', '.m4a']
DELETE_ERROR_FILES = True

def main():
    # 第一步：扫描文件并获取音乐信息
    print("第一步：扫描文件并获取音乐信息...")
    correct_files_info, error_files_info = scan_files_and_get_info(
        root_dir=ROOT_DIR,
        music_extensions=MUSIC_EXTENSIONS,
        delete_error_files=DELETE_ERROR_FILES
    )

    # 第三步：根据音乐信息移动文件
    print("第二步：根据音乐信息移动文件...")
    move_files(root_dir=ROOT_DIR, files_info=correct_files_info)

if __name__ == "__main__":
    # 统计耗时
    import time
    start_time = time.time()
    print("程序开始运行...")
    main()
    print(f"程序运行结束，耗时：{time.time() - start_time:.2f}秒")
