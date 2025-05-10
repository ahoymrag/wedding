import os
import re
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))

SECTIONS = {
    "1": ("Overview", "01_overview"),
    "2": ("Staff", "02_staff"),
    "3": ("Guests", "03_guests"),
    "4": ("Logistics", "04_logistics"),
    "5": ("Docs", "05_docs"),
    "6": ("Music & AV", "06_music_av"),
    "7": ("Finance", "07_finance"),
    "8": ("Scripts", "08_scripts")
}

def get_file_preview(filepath, max_lines=3):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:max_lines]
            preview = ''.join(lines).strip()
            if len(lines) == max_lines:
                preview += "\n..."
            return preview
    except:
        return "Unable to preview file"

def list_files(folder, show_preview=False):
    path = os.path.join(BASE, folder)
    print(f"\n📁 {folder}\n" + "-"*40)
    files = [f for f in os.listdir(path) if f.endswith(('.md', '.csv', '.txt'))]
    if not files:
        print("No files found in this section.")
    else:
        for i, file in enumerate(files, 1):
            print(f"{i}. {file}")
            if show_preview:
                preview = get_file_preview(os.path.join(path, file))
                print(f"   {preview}\n")
    print("-"*40)
    return files

def format_markdown(content):
    # Convert headers
    content = re.sub(r'^# (.*?)$', r'\n\033[1;36m\1\033[0m\n', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.*?)$', r'\n\033[1;35m\1\033[0m\n', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.*?)$', r'\n\033[1;34m\1\033[0m\n', content, flags=re.MULTILINE)
    
    # Convert bold
    content = re.sub(r'\*\*(.*?)\*\*', r'\033[1m\1\033[0m', content)
    
    # Convert lists
    content = re.sub(r'^- (.*?)$', r'• \1', content, flags=re.MULTILINE)
    
    return content

def search_files(query):
    results = []
    for _, folder in SECTIONS.values():
        path = os.path.join(BASE, folder)
        for file in os.listdir(path):
            if file.endswith(('.md', '.csv', '.txt')):
                filepath = os.path.join(path, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if query.lower() in content.lower():
                            results.append((folder, file))
                except:
                    continue
    return results

def create_file(folder):
    print("\nCreate New File")
    print("-"*40)
    filename = input("Enter filename (with .md, .csv, or .txt extension): ")
    if not filename:
        return
    
    if not filename.endswith(('.md', '.csv', '.txt')):
        print("⚠️ File must end with .md, .csv, or .txt")
        return
    
    filepath = os.path.join(BASE, folder, filename)
    if os.path.exists(filepath):
        print("⚠️ File already exists")
        return
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            if filename.endswith('.md'):
                f.write(f"# {filename[:-3].replace('_', ' ').title()}\n\n")
            f.write(f"Created on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        print(f"✅ Created {filename}")
    except Exception as e:
        print(f"⚠️ Error creating file: {e}")

def read_file(folder, filename):
    full_path = os.path.join(BASE, folder, filename)
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if filename.endswith('.md'):
                content = format_markdown(content)
            print("\n" + content)
            
            while True:
                print("\nOptions:")
                print("1. Go back to section")
                print("2. List files")
                print("3. Edit file")
                print("4. Exit")
                
                choice = input("\nSelect an option: ")
                if choice == "1":
                    return
                elif choice == "2":
                    list_files(folder)
                elif choice == "3":
                    edit_file(full_path)
                elif choice == "4":
                    print("Exiting...")
                    exit()
                else:
                    print("Invalid choice.")
    else:
        print("⚠️ File not found.")

def edit_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("\nEdit File (type 'SAVE' on a new line to save, 'CANCEL' to cancel)")
        print("-"*40)
        print(content)
        print("-"*40)
        
        new_content = []
        while True:
            line = input()
            if line == "SAVE":
                break
            elif line == "CANCEL":
                return
            new_content.append(line)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_content))
        print("✅ File saved successfully")
    except Exception as e:
        print(f"⚠️ Error editing file: {e}")

def show_help():
    print("\n💍 WEDDING COMMAND CENTER HELP")
    print("-"*40)
    print("Navigation:")
    print("• Select a section number to view its files")
    print("• Enter a filename to view its contents")
    print("• Use the menu options to navigate")
    print("\nFeatures:")
    print("• View and edit markdown files")
    print("• Search across all files")
    print("• Create new files")
    print("• Preview file contents")
    print("\nCommands:")
    print("• 'help' - Show this help menu")
    print("• 'search' - Search across all files")
    print("• 'new' - Create a new file")
    print("• 'preview' - Toggle file previews")
    print("• 'exit' - Exit the program")
    print("-"*40)

def main():
    show_preview = False
    while True:
        print("\n💍 WEDDING COMMAND CENTER")
        for key, (label, _) in SECTIONS.items():
            print(f"{key}. {label}")
        print("\nCommands: help, search, new, preview, exit")

        choice = input("\nSelect an option: ").lower()
        
        if choice == "exit":
            print("Exiting…")
            break
        elif choice == "help":
            show_help()
        elif choice == "search":
            query = input("Enter search term: ")
            results = search_files(query)
            if results:
                print(f"\nFound {len(results)} results:")
                for folder, file in results:
                    print(f"• {folder}/{file}")
            else:
                print("No results found.")
        elif choice == "new":
            print("\nSelect section to create file:")
            for key, (label, _) in SECTIONS.items():
                print(f"{key}. {label}")
            section = input("\nSelect section number: ")
            if section in SECTIONS:
                create_file(SECTIONS[section][1])
        elif choice == "preview":
            show_preview = not show_preview
            print(f"File previews {'enabled' if show_preview else 'disabled'}")
        elif choice in SECTIONS:
            label, folder = SECTIONS[choice]
            files = list_files(folder, show_preview)
            if files:
                filename = input("Enter filename to view (or press Enter to go back): ")
                if filename:
                    read_file(folder, filename)
        else:
            print("Invalid choice. Type 'help' for available commands.")

if __name__ == "__main__":
    main()
