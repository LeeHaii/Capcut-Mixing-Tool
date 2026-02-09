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
    print("\n🔄 STEP 1: Loading draft_content.json...")
    draft_json_path = os.path.join(project_path, "draft_content.json")
    print(f"   Project path: {project_path}")
    print(f"   Looking for: {draft_json_path}")

    if not os.path.exists(draft_json_path):
        raise ValueError("draft_content.json not found in project folder")

    with open(draft_json_path, 'r', encoding='utf-8') as f:
        project_data = json.load(f)
    print("   ✓ Successfully loaded draft_content.json")
    
    # =========================================================================
    # STEP 2: Process shuffling on the original structure
    # =========================================================================
    print("\n🔄 STEP 2: Starting shuffling process...")
    _shuffle_in_draft_format(project_data)
    print("   ✓ Shuffling completed")
    
    # =========================================================================
    # STEP 3: Write back to the original file
    # =========================================================================
    print("\n🔄 STEP 3: Writing changes back to draft_content.json...")
    with open(draft_json_path, 'w', encoding='utf-8') as f:
        json.dump(project_data, f, indent=2)
    print("   ✓ Successfully saved changes")
    
    print(f"\n✅ Successfully shuffled segments in: {project_path}\n")


def _shuffle_in_draft_format(project_data):
    """
    Perform the shuffling logic directly on the original CapCut draft_content.json format.
    
    This preserves all other project data (text layers, keyframes, transitions, etc.)
    while only shuffling the video segments between marker pairs.
    """
    
    # =========================================================================
    # STEP 1: Extract markers and validate
    # =========================================================================
    print("   [1.1] Extracting markers from time_marks...")
    time_marks_obj = project_data.get('time_marks', {})
    
    # Extract marker start times from mark_items
    mark_items = time_marks_obj.get('mark_items', []) if isinstance(time_marks_obj, dict) else []
    print(f"       Found {len(mark_items)} marker items")
    
    # Convert marker objects to just their start times (in milliseconds)
    markers = sorted([m['time_range']['start'] for m in mark_items], reverse=True)
    print(f"       Marker times (ms): {markers}")
    
    if len(markers) < 2:
        raise ValueError("Project must contain at least 2 markers")
    
    # =========================================================================
    # STEP 2: Find the video tracks
    # =========================================================================
    print("   [1.2] Finding video tracks...")
    tracks = project_data.get('tracks', [])
    if not tracks:
        raise ValueError("Project has no tracks")
    print(f"       Total tracks found: {len(tracks)}")
    
    # Find video tracks with segments
    video_tracks = [t for t in tracks if t.get('type') == 'video' and t.get('segments')]
    print(f"       Video tracks with segments: {len(video_tracks)}")
    if not video_tracks:
        raise ValueError("No video track with segments found")
    
    # Use the track with the most segments (most likely the main content track)
    target_track = max(video_tracks, key=lambda t: len(t.get('segments', [])))
    target_track_segment_count = len(target_track.get('segments', []))
    print(f"       Selected track with {target_track_segment_count} segments")
    
    # =========================================================================
    # STEP 3: Process each pair of markers
    # =========================================================================
    print(f"   [1.3] Processing {len(markers) // 2} marker pairs...")
    
    for pair_idx in range(0, len(markers) - 1, 2):
        marker_start = markers[pair_idx + 1]  # Earlier marker
        marker_end = markers[pair_idx]        # Later marker
        
        print(f"       Processing pair {pair_idx // 2 + 1}: {marker_start}ms - {marker_end}ms")
        
        if marker_start >= marker_end:
            print(f"           ⚠ Invalid pair (start >= end), skipping")
            continue  # Skip invalid pairs
        
        # =====================================================================
        # STEP 4: Find segments within this marker pair range
        # =====================================================================
        print(f"           [2.1] Finding segments in range...")
        segments = target_track.get('segments', [])
        segments_in_range = [
            seg for seg in segments
            if seg.get('target_timerange', {}).get('start', 0) >= marker_start 
            and (seg.get('target_timerange', {}).get('start', 0) + seg.get('target_timerange', {}).get('duration', 0)) <= marker_end
        ]
        print(f"           [2.1] Found {len(segments_in_range)} segments in this range")
        
        if not segments_in_range:
            print(f"           ⚠ No segments in this range, skipping")
            continue  # No segments in this range
        
        # =====================================================================
        # STEP 5: Shuffle segments in this range
        # =====================================================================
        print(f"           [2.2] Shuffling {len(segments_in_range)} segments...")
        random.shuffle(segments_in_range)
        print(f"           [2.2] Shuffling complete")
        
        # =====================================================================
        # STEP 6: Rebuild timeline and reorder in array for this marker pair
        # =====================================================================
        print(f"           [2.3] Rebuilding timeline...")
        # Get the indices where these segments are located in the main array
        segment_indices = [segments.index(seg) for seg in segments_in_range]
        
        # Put the shuffled segments back into their original index positions
        for idx, seg in zip(sorted(segment_indices), segments_in_range):
            segments[idx] = seg
        
        print(f"           [2.3] Reordering segment start times...")
        # Update their start times in the new shuffled order
        cursor = marker_start
        
        for seg_num, seg in enumerate(segments_in_range):
            seg_duration = seg.get('target_timerange', {}).get('duration', 0)
            old_start = seg['target_timerange'].get('start', 0)
            seg['target_timerange']['start'] = cursor
            print(f"               Segment {seg_num + 1}: {old_start}ms → {cursor}ms (duration: {seg_duration}ms)")
            cursor += seg_duration
        
        print(f"           ✓ Pair {pair_idx // 2 + 1} completed\n")