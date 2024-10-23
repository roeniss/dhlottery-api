import os

def write_py_file_tree_with_top_folder(root_folder, output_file):
    root_folder_name = os.path.basename(os.path.normpath(root_folder))  # 최상위 폴더명 가져오기
    with open(output_file, 'w') as file:
        for dirpath, _, filenames in os.walk(root_folder):
            # .py 파일만 필터링
            py_files = [f for f in filenames if f.endswith('.py')]
            if py_files:
                for py_file in py_files:
                    # 경로와 파일명을 원하는 형식으로 작성
                    relative_path = os.path.relpath(dirpath, root_folder)
                    full_path = os.path.join(root_folder_name, relative_path)  # 상위 폴더명 포함 경로
                    file.write(f"{full_path}: {py_file}\n")

# 예시로 사용할 경로 및 출력 파일
root_folder = 'src/dhapi'  # 루트 폴더 경로 지정
output_file = 'py_file_tree.txt'  # 결과를 저장할 파일 경로 지정

write_py_file_tree_with_top_folder(root_folder, output_file)
