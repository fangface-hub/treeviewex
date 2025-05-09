from setuptools import setup, find_packages

setup(
    name="treeviewex",  # パッケージ名
    version="1.0.0",  # バージョン
    description="A TreeView extension for Tkinter",  # 説明
    author="fangface",  # 作者名
    url="https://github.com/fangface-hub/treeviewex",  # プロジェクトのURL
    packages=find_packages(),  # パッケージを自動検出
    install_requires=[],  # 必要な依存関係をリストアップ
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # 対応するPythonのバージョン
)
