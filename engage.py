import os

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

def list_files(folder):
    path = os.path.join(BASE, folder)
    print(f"\n📁 {folder}\n" + "-"*40)
    for file in os.listdir(path):
        print("•", file)
    print("-"*40)

def read_file(folder, filename):
    full_path = os.path.join(BASE, folder, filename)
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as f:
            print("\n" + f.read())
    else:
        print("⚠️ File not found.")

def main():
    while True:
        print("\n💍 WEDDING COMMAND CENTER")
        for key, (label, _) in SECTIONS.items():
            print(f"{key}. {label}")
        print("9. Exit")

        choice = input("Select a section: ")
        if choice == "9":
            print("Exiting…")
            break
        elif choice in SECTIONS:
            label, folder = SECTIONS[choice]
            list_files(folder)
            filename = input("Enter filename to view (or press Enter to go back): ")
            if filename:
                read_file(folder, filename)
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
