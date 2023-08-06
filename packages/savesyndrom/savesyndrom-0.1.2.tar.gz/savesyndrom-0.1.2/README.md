# savesyndrom

A GUI application that counts how many times you save your files with `ctrl+s`.

## Install and use

* First option

You can install this package, using

```shell
pip install savesyndrom
```

and run by

```shell
python -m savesyndrom
```

If you use Linux, please, run this application with root rights. Example:

```shell
sudp python3 -m savesyndrom
```

## Build

If you copy this repo on your computer, you can build it to executable file.

For build you should install `pyinstaller` by command

```shell
pip install pyinstaller
```

After that type this command for build executable file

```shell
pyinstaller --onefile --noconsole --name savesyndrom main.py
```

In `dist` directory you can find executable file `savesyndrom` or `savesyndrom.exe`
