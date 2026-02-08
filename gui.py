import tkinter as tk
from tkinter import filedialog, messagebox
import os
from pathlib import Path
from suffle_capcu_track import shuffle_segments_between_marker_pairs


class CapCutShuffleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CapCut Project Shuffler")
        self.root.geometry("600x500")
        
        self.project_folder = None
        self.projects = {}  # {folder_name: folder_path}
        self.project_vars = {}  # {folder_name: BooleanVar}
        
        # =====================================================================
        # STEP 1: Folder Selection Section
        # =====================================================================
        folder_frame = tk.Frame(root, padx=10, pady=10)
        folder_frame.pack(fill=tk.X)
        
        tk.Label(folder_frame, text="CapCut Master Folder:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        folder_button_frame = tk.Frame(folder_frame)
        folder_button_frame.pack(fill=tk.X, pady=5)
        
        self.folder_label = tk.Label(folder_button_frame, text="No folder selected", fg="gray")
        self.folder_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Button(folder_button_frame, text="Browse", command=self.select_folder, width=12).pack(side=tk.RIGHT)
        
        # =====================================================================
        # STEP 2: Project Selection Section (Checkboxes)
        # =====================================================================
        project_frame = tk.Frame(root, padx=10, pady=10)
        project_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(project_frame, text="Select Projects to Process:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        # Scrollable frame with checkboxes
        canvas = tk.Canvas(project_frame)
        scrollbar = tk.Scrollbar(project_frame, orient="vertical", command=canvas.yview)
        
        self.checkbox_frame = tk.Frame(canvas)
        self.checkbox_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.checkbox_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # =====================================================================
        # STEP 3: Process Button
        # =====================================================================
        button_frame = tk.Frame(root, padx=10, pady=10)
        button_frame.pack(fill=tk.X)
        
        tk.Button(
            button_frame,
            text="Process Selected Projects",
            command=self.process_projects,
            bg="green",
            fg="white",
            font=("Arial", 11, "bold"),
            width=30,
            height=2
        ).pack(fill=tk.BOTH, expand=True)
    
    def select_folder(self):
        """Open folder selection dialog."""
        folder = filedialog.askdirectory(title="Select CapCut Master Folder")
        
        if folder:
            self.project_folder = folder
            self.folder_label.config(text=folder, fg="black")
            self.load_projects()
    
    def load_projects(self):
        """Load project folders from the selected master folder."""
        # Clear previous checkboxes
        for widget in self.checkbox_frame.winfo_children():
            widget.destroy()
        
        self.projects = {}
        self.project_vars = {}
        
        if not self.project_folder:
            messagebox.showwarning("No Folder", "Please select a folder first")
            return
        
        try:
            folder_path = Path(self.project_folder)
            
            # Find all subdirectories that contain draft_content.json
            for item in sorted(folder_path.iterdir()):
                if item.is_dir():
                    draft_json = item / "draft_content.json"
                    if draft_json.exists():
                        folder_name = item.name
                        self.projects[folder_name] = str(item)
                        
                        # Create checkbox variable and checkbox
                        var = tk.BooleanVar()
                        self.project_vars[folder_name] = var
                        
                        checkbox = tk.Checkbutton(
                            self.checkbox_frame,
                            text=folder_name,
                            variable=var,
                            font=("Arial", 10),
                            anchor=tk.W
                        )
                        checkbox.pack(fill=tk.X, padx=5, pady=3)
            
            if not self.projects:
                messagebox.showinfo("No Projects", "No CapCut project folders with draft_content.json found")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load projects: {str(e)}")
    
    def process_projects(self):
        """Process all selected projects."""
        selected_projects = [name for name, var in self.project_vars.items() if var.get()]
        
        if not selected_projects:
            messagebox.showwarning("No Selection", "Please select at least one project")
            return
        
        processed_count = 0
        failed_projects = []
        
        for project_name in selected_projects:
            try:
                project_folder_path = self.projects[project_name]
                
                # Run shuffle function with project folder path
                # The function handles loading, processing, and syncing automatically
                shuffle_segments_between_marker_pairs(project_folder_path)
                processed_count += 1
            
            except ValueError as e:
                failed_projects.append(f"{project_name}: {str(e)}")
            except Exception as e:
                failed_projects.append(f"{project_name}: {str(e)}")
        
        # Show results
        message = f"Processed: {processed_count} project(s)"
        if failed_projects:
            message += f"\n\nFailed:\n" + "\n".join(failed_projects)
            messagebox.showinfo("Processing Complete", message)
        else:
            messagebox.showinfo("Success", message)


if __name__ == "__main__":
    root = tk.Tk()
    app = CapCutShuffleGUI(root)
    root.mainloop()
