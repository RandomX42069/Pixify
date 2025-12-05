import stdlib.__entry__ as stdlib
import src._pyxify_init as _pyxify_init, subprocess, atexit, pathlib, os, sys

def main(argv):
    filesystem = stdlib.filesystem()
    if not argv:
        return
    file = argv[0]

    _instance = pathlib.Path(os.path.abspath(file))

    runtimeDir = pathlib.Path(f"pyxify.{_instance.stem}")
    def atEnd(direc):
        filesystem.rmdir(str(direc))
    atexit.register(atEnd, runtimeDir)

    if not filesystem.isExistAndFile(str(_instance)):
        print(f"File doesn't exist: {file}")
        return

    res = subprocess.Popen(
        "python -V", shell=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = res.communicate()
    if res.returncode != 0:
        print("Python isn't installed")
        sys.exit(1)

    runtimeDir.mkdir(parents=True, exist_ok=True)

    pyxify_code = _pyxify_init.pyxify_parse(filesystem.readFromFile(str(_instance)).decode("utf-8"))

    pyxify_file = runtimeDir / f"{_instance.stem}.python.pyxify"
    filesystem.createFile(str(pyxify_file))
    with open(pyxify_file, "w", encoding="utf-8") as f:
        f.write(pyxify_code)

    result = subprocess.Popen(f"python \"{pyxify_file}\"", shell=True)
    result.communicate()


if __name__ == "__main__":
    main(sys.argv[1:])