import random
import json
import os
from pathlib import Path


def shuffle_segments_between_marker_pairs(project_path):
    """
    Load a CapCut project, shuffle video segments between marker pairs,
    and save changes back.
    
    Marker pairs are processed sequentially:
    - (marker[0], marker[1])
    - (marker[2], marker[3])
    - (marker[4], marker[5])
    - etc.
    
    PARAMETERS
    ----------
    project_path : str
        Path to the CapCut project folder
        (e.g., 'C:\\Users\\YourName\\AppData\\Local\\CapCut\\User Data\\Projects\\...')
    
    RETURNS
    -------
    None
        Modifies the project in-place and saves changes
    """
    
    # =========================================================================
    # STEP 1: Load the draft_content.json directly
    # =========================================================================
    draft_json_path = os.path.join(project_path, "draft_content.json")

    if not os.path.exists(draft_json_path):
        raise ValueError("draft_content.json not found in project folder")

    with open(draft_json_path, 'r', encoding='utf-8') as f:
        project_data = json.load(f)
    
    # =========================================================================
    # STEP 2: Process shuffling on the original structure
    # =========================================================================
    _shuffle_in_draft_format(project_data)
    
    # =========================================================================
    # STEP 3: Write back to the original file
    # =========================================================================
    with open(draft_json_path, 'w', encoding='utf-8') as f:
        json.dump(project_data, f, indent=2)
    
    print(f"✅ Successfully shuffled segments in: {project_path}")


def _shuffle_in_draft_format(project_data):
    """
    Perform the shuffling logic directly on the original CapCut draft_content.json format.
    
    This preserves all other project data (text layers, keyframes, transitions, etc.)
    while only shuffling the video segments between marker pairs.
    """
    
    # =========================================================================
    # STEP 1: Extract markers and validate
    # =========================================================================
    time_marks_obj = project_data.get('time_marks', {})
    
    # Extract marker start times from mark_items
    mark_items = time_marks_obj.get('mark_items', []) if isinstance(time_marks_obj, dict) else []
    
    # Convert marker objects to just their start times (in milliseconds)
    markers = sorted([m['time_range']['start'] for m in mark_items], reverse=True)
    
    if len(markers) < 2:
        raise ValueError("Project must contain at least 2 markers")
    
    # =========================================================================
    # STEP 2: Find the video tracks
    # =========================================================================
    tracks = project_data.get('tracks', [])
    if not tracks:
        raise ValueError("Project has no tracks")
    
    # Find video tracks with segments
    video_tracks = [t for t in tracks if t.get('type') == 'video' and t.get('segments')]
    if not video_tracks:
        raise ValueError("No video track with segments found")
    
    # Use the track with the most segments (most likely the main content track)
    target_track = max(video_tracks, key=lambda t: len(t.get('segments', [])))
    
    # =========================================================================
    # STEP 3: Process each pair of markers
    # =========================================================================
    for pair_idx in range(0, len(markers) - 1, 2):
        marker_start = markers[pair_idx + 1]  # Earlier marker
        marker_end = markers[pair_idx]        # Later marker
        
        if marker_start >= marker_end:
            continue  # Skip invalid pairs
        
        # =====================================================================
        # STEP 4: Find segments within this marker pair range
        # =====================================================================
        segments = target_track.get('segments', [])
        segments_in_range = [
            seg for seg in segments
            if seg.get('target_timerange', {}).get('start', 0) >= marker_start 
            and (seg.get('target_timerange', {}).get('start', 0) + seg.get('target_timerange', {}).get('duration', 0)) <= marker_end
        ]
        
        if not segments_in_range:
            continue  # No segments in this range
        
        # =====================================================================
        # STEP 5: Shuffle segments in this range
        # =====================================================================
        random.shuffle(segments_in_range)
        
        # =====================================================================
        # STEP 6: Rebuild timeline and reorder in array for this marker pair
        # =====================================================================
        # Get the indices where these segments are located in the main array
        segment_indices = [segments.index(seg) for seg in segments_in_range]
        
        # Put the shuffled segments back into their original index positions
        for idx, seg in zip(sorted(segment_indices), segments_in_range):
            segments[idx] = seg
        
        # Update their start times in the new shuffled order
        cursor = marker_start
        
        for seg in segments_in_range:
            seg_duration = seg.get('target_timerange', {}).get('duration', 0)
            seg['target_timerange']['start'] = cursor
            cursor += seg_duration