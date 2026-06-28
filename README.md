# Fracture

A utility for damaging (mutating) files with protection of critical structures. Allows you to make random changes to the bytes of a file, keeping it open to images and videos.

## Starting from source

```bash
pip install pillow
python main.py
```

## Compilation in .exe

Make sure that PyInstaller is installed:

```bash
pip install pyinstaller
```

Build from the '.spec` file (recommended):

```bash
pyinstaller main.spec
```

The finished '.exe` will appear in the `dist/` folder.

## Usage

1. Launch the program (`main.exe ` or `python main.py `).
2. Poke **"Review"** and select the file.
3. Specify ** the number of bytes** to change (the more— the more damage).
4. Press **"Mutate"**.
5. The program will create a copy with the suffix `_mutated` in the same folder.

### Protection of structures

Critical bytes (headers, markers) are automatically protected for images so that the file remains openable. For the remaining files, the first 1024 bytes (header) are protected. If the mutation violates the integrity, the program automatically reduces the number of bytes being modified.