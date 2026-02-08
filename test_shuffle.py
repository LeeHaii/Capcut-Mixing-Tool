import os
from suffle_capcu_track import shuffle_segments_between_marker_pairs

# Replace this with your actual CapCut project folder path
# For example: r"C:\CapCut Project\CapCut Drafts\TESTTS"
project_path = r"C:\CapCut Project\CapCut Drafts\AmerimaTest"

if not os.path.exists(project_path):
    print(f"❌ Project path not found: {project_path}")
else:
    print(f"✅ Testing with project: {project_path}")
    try:
        shuffle_segments_between_marker_pairs(project_path)
    except Exception as e:
        print(f"❌ Error: {e}")
