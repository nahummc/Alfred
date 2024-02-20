from cx_Freeze import setup, Executable

setup(
    name="AlfredBot",
    version="0.0",
    description="Description of your application",
    executables=[Executable("main.py")],
    options={
        "build_exe": {
            "packages": ["AlfredsPacking"],
            "include_files": ["log.py", "dbhandler.py", "alfred.py", "api/coin.py", "main.py", "reqs.txt", "setup.py"]
        }
    }
)
