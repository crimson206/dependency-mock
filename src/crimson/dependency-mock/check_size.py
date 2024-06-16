import os
import subprocess
import platform
import shutil

def get_directory_size(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def create_virtual_env(env_name="env"):
    subprocess.run(f"python -m venv {env_name}", shell=True)

def install_package(package_name, env_name="env"):
    if platform.system() == 'Windows':
        activate_script = f"{env_name}\\Scripts\\activate"
        subprocess.run(f"{activate_script} && pip install {package_name}", shell=True)
    else:
        activate_script = f"source {env_name}/bin/activate"
        subprocess.run(f"{activate_script} && pip install {package_name}", shell=True, executable='/bin/bash')

def main(package_name):
    env_name = "env"
    
    # 1. 가상 환경 생성 및 초기 용량 계산
    create_virtual_env(env_name)
    initial_size = get_directory_size(env_name)
    print(f"Initial virtual environment size: {initial_size / (1024 * 1024):.2f} MB")
    
    # 2. 패키지 설치
    install_package(package_name, env_name)
    
    # 3. 설치 후 용량 계산
    final_size = get_directory_size(env_name)
    print(f"Final virtual environment size: {final_size / (1024 * 1024):.2f} MB")
    
    # 4. 설치된 패키지 용량 계산
    installed_package_size = final_size - initial_size
    print(f"Installed package size: {installed_package_size / (1024 * 1024):.2f} MB")
    
    # 5. 가상 환경 삭제 (선택 사항)
    shutil.rmtree(env_name)
    print(f"Virtual environment '{env_name}' has been removed.")

if __name__ == "__main__":
    package_name = input("Enter the package name: ")
    main(package_name)
