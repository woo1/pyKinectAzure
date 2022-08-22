## 1.libk4abt 관련 오류 해결
error : Failed to load body tracker library libk4abt.so: cannot open shared object file: No such file or directory
<br>
### 설치를 위한 환경 세팅
https://docs.microsoft.com/en-us/windows-server/administration/linux-package-repository-for-microsoft-software
<br>
우분투 18.04에 맞춘 환경 세팅<br>
````buildoutcfg
curl -sSL https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
sudo apt-add-repository https://packages.microsoft.com/ubuntu/18.04/prod
sudo apt-get update
````

### 설치
````buildoutcfg
sudo apt install libk4abt1.1-dev
````
