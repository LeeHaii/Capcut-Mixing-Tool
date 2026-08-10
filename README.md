# 🎬 CapCut Mixing Tool

A lightweight utility for automating repetitive CapCut editing workflows by **randomly shuffling video clips between timeline markers**.

CapCut Mixing Tool can scan your CapCut projects, let you select multiple projects at once, and automatically rearrange clips inside marker-defined sections while preserving the rest of the project structure.

> ⚠️ **Important:** This tool directly modifies CapCut project files. Always back up important projects before processing them.

---

## ✨ Features

* 🎲 Randomly shuffle clips between CapCut timeline markers
* 📁 Automatically detect CapCut projects
* 🔎 Search projects by name
* ☑️ Process multiple projects at once
* 🏷️ Use marker pairs to define shuffle regions
* 💾 Directly update `draft_content.json`
* 🧩 Preserve unrelated project data such as text, keyframes, transitions, and other tracks
* 🔄 Optional CapCut cache refresh
* 🆔 Automatically regenerate project metadata when cache refresh is enabled
* 🖥️ Simple Tkinter desktop interface
* 📦 Prebuilt Windows executables available in `dist/`

---

## 🎯 How It Works

The tool uses **CapCut timeline markers** to determine which clips should be shuffled.

Markers are processed in pairs:

```text
Marker 1 ───────────── Marker 2
        clips shuffled

Marker 3 ───────────── Marker 4
        clips shuffled

Marker 5 ───────────── Marker 6
        clips shuffled
```

For every marker pair, the tool:

1. Finds video clips completely inside the marker range.
2. Randomizes their order.
3. Places the shuffled clips back into the timeline.
4. Recalculates their timeline positions.
5. Saves the modified CapCut project.

Only the selected video track is shuffled.

---

## 📋 Example

Imagine your CapCut timeline looks like this:

```text
Marker A                              Marker B
   │                                    │
   ▼                                    ▼

[ Clip 1 ][ Clip 2 ][ Clip 3 ][ Clip 4 ]
```

After running the tool, you might get:

```text
Marker A                              Marker B
   │                                    │
   ▼                                    ▼

[ Clip 3 ][ Clip 1 ][ Clip 4 ][ Clip 2 ]
```

Running the tool again generates another random arrangement.

---

## 🚀 Quick Start

### Option 1 — Run the Windows executable

Download or clone the repository:

```bash
git clone https://github.com/LeeHaii/Capcut-Mixing-Tool.git
```

Open:

```text
dist/
```

Then run one of the provided `.exe` files.

No Python installation is required when using the packaged executable.

---

### Option 2 — Run from source

Make sure Python 3 is installed.

Clone the repository:

```bash
git clone https://github.com/LeeHaii/Capcut-Mixing-Tool.git
cd Capcut-Mixing-Tool
```

Run:

```bash
python gui.py
```

The main application uses Python's standard library, including Tkinter.

---

## 🎬 Preparing Your CapCut Project

Before using the tool:

### 1. Open your project in CapCut

Arrange your clips normally.

### 2. Add timeline markers

Add markers around every section you want randomized.

For example:

```text
M1       M2        M3       M4
│        │         │        │
▼        ▼         ▼        ▼

[A][B][C]          [D][E][F]
└──────┘           └──────┘
 Shuffle            Shuffle
 Range 1             Range 2
```

The project must contain **at least two markers**.

An even number of markers is recommended so every marker has a matching pair.

### 3. Save and close CapCut

Closing CapCut before modifying its project files is recommended to prevent CapCut from overwriting the modified draft.

### 4. Back up your project

The tool modifies CapCut's project JSON directly.

Create a copy of important projects before processing them.

---

## 🖥️ Using the GUI

### Step 1 — Select the CapCut master folder

Click:

```text
Browse
```

Select the directory containing your CapCut project folders.

The tool detects folders containing:

```text
draft_content.json
```

---

### Step 2 — Find your project

Use the search box to filter projects by name.

```text
Search Projects:
[ my project... ]
```

---

### Step 3 — Select projects

Check one or more projects:

```text
☑ Project A
☑ Project B
☐ Project C
```

Multiple projects can be processed in one run.

---

### Step 4 — Choose cache refresh behavior

The following option is enabled by default:

```text
☑ Force CapCut cache refresh
  (rename folder & update metadata)
```

When enabled, the tool renames the processed project to force CapCut to reload the modified draft.

For example:

```text
My Project
```

becomes:

```text
My Project - shuffled
```

Running it again may produce:

```text
My Project - shuffled (1)
My Project - shuffled (2)
...
```

The associated `draft_meta_info.json` is also updated when available.

---

### Step 5 — Process

Click:

```text
Process Selected Projects
```

The tool will process each selected CapCut project and display the results when finished.

---

## 🔄 CapCut Cache Refresh

CapCut may continue displaying cached project data even after `draft_content.json` has been changed.

To work around this, the tool can:

* Rename the project directory
* Update `draft_fold_path`
* Generate a new `draft_id`
* Save the modified metadata

This encourages CapCut to load the newly modified project instead of its cached copy.

You can disable this behavior using the checkbox in the GUI.

---

## 📂 Project Structure

```text
Capcut-Mixing-Tool/
│
├── gui.py
│   └── Desktop GUI
│
├── suffle_capcu_track.py
│   └── Core CapCut clip shuffling logic
│
├── test_shuffle.py
│   └── Basic shuffle testing script
│
├── capgenie_test.py
│   └── Experimental CapGenie test
│
├── gui.spec
│   └── PyInstaller build configuration
│
├── dist/
│   ├── ClipShuffler.exe
│   └── gui.exe
│
└── README.md
```

---

## 🧠 Shuffle Logic

The program reads CapCut's:

```text
draft_content.json
```

and extracts timeline markers from:

```text
time_marks -> mark_items
```

It then finds video tracks containing segments.

When multiple video tracks exist, the track containing the **largest number of segments** is selected as the main track.

For each marker pair, clips whose complete timeline range falls within the two markers are collected.

Their order is randomized using Python's:

```python
random.shuffle()
```

The shuffled segments are then placed back into the timeline.

Other project information remains untouched wherever possible.

---

## 📁 CapCut Project Folder

A typical project may contain files similar to:

```text
My CapCut Project/
├── draft_content.json
├── draft_meta_info.json
└── ...
```

The GUI only lists project directories containing a `draft_content.json` file.

The shuffle processor can also recursively locate additional `draft_content.json` files inside the selected project.

---

## ⚠️ Important Notes

This project modifies undocumented/internal CapCut project files.

Because CapCut may change its project format between versions, compatibility cannot be guaranteed.

Before using the tool:

* Back up important CapCut projects
* Prefer closing CapCut before processing
* Test on a duplicate project first
* Verify the shuffled project before continuing your edit

Use this software at your own risk.

---

## 🛠️ Build the Executable

The repository includes a PyInstaller spec file.

Install PyInstaller:

```bash
pip install pyinstaller
```

Build using:

```bash
pyinstaller gui.spec
```

The generated executable should appear inside:

```text
dist/
```

---

## 🐛 Troubleshooting

### No projects appear

Make sure you selected the folder that directly contains your CapCut project directories.

Each recognized project must contain:

```text
draft_content.json
```

---

### "Project must contain at least 2 markers"

Add at least two timeline markers inside CapCut.

The markers define the beginning and end of a shuffle range.

---

### "No video track with segments found"

The project must contain a video track with clips.

Make sure the project isn't empty and that your clips are on a standard video track.

---

### CapCut still shows the old clip order

Enable:

```text
Force CapCut cache refresh
```

This renames the project and updates its metadata so CapCut treats it as refreshed project data.

---

### Project does not appear correctly after processing

Restore your backup and test the tool on a duplicate project.

CapCut's internal draft format may vary depending on the application version.

---

## 🤝 Contributing

Contributions, fixes, and improvements are welcome.

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/my-feature
```

3. Commit your changes

```bash
git commit -m "Add my feature"
```

4. Push the branch

```bash
git push origin feature/my-feature
```

5. Open a Pull Request

---

## 💡 Ideas for Future Development

Possible improvements include:

* Automatic project backups
* Select specific tracks to shuffle
* Select marker ranges individually
* Shuffle seed support
* Undo/restore functionality
* Drag-and-drop project selection
* Shuffle preview before saving
* Better CapCut version compatibility detection
* Logging and error reports
* Automatic CapCut project folder detection

---

## ⚖️ Disclaimer

This project is an independent utility and is **not affiliated with, endorsed by, or associated with CapCut or ByteDance**.

CapCut is a trademark of its respective owner.

The tool modifies CapCut project data directly. Always maintain backups of important work.

---

## 👤 Author

**Tran Duc Thang / LeeHaii**

GitHub: [@LeeHaii](https://github.com/LeeHaii)

Facebook: [rhymx2k3](https://www.facebook.com/rhymx2k3/)

---

## ⭐ Support

If this project saves you time, consider giving the repository a ⭐ on GitHub.
