# Final Project for CS214: ALgorithm and Complexity
Yanjie Ze, May 2021

# 1 Basic Information
这是CS214:算法与复杂性（英文班）的Final Project。
授课老师：高晓沨教授，王磊副教授

# 2 Usage
```shell
python baseline.py
```

# 3 Experiment Record
## Baseline 1: Depth Based
Find Optimal Solution. 
Final time=22.416667

## Baseline 2: Job Step Based
Optimal Solution.
**threshold=5**: final time = 33.358333

# 4 Distinguishing Feature
This section we introduce some distinguishing Feature in our **Python** implementation.
1. **Automatic Data Loader**: Different from other teams who **modify the toy data's form** into other forms like **.txt**, we use python to directly load the toy data, which means that **the whole process is automatic** and can be exectued without any human's handcraft modification.
2. **Automatic Linear Programming**: Supported by the python package **pulp**, we can make the process of LP as the undivided part.
3. 
# Last: Coding命名规范
1. class名字统一大写开头，如DataLoader。
2. 变量名用小写单词加下划线，如data_loader。
3. 文件名用单词加下划线，如data_loader.py。