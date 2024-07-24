import zipfile
import rarfile
from threading import Thread

def handle_zip(passwords):
    for password in passwords:
        try:
            with zipfile.ZipFile(path_zip, 'r') as myzip:
                myzip.setpassword(password.encode())
                if choose_2_zip == "1":
                    zip_content = myzip.read(text_name_zip)
                    print(zip_content)
                elif choose_2_zip == "3":
                    existing_content_zip = myzip.read(text_name_zip)
                    new_content_zip = existing_content_zip + "\n".encode('utf-8') + additional_text_zip.encode('utf-8')
                    with zipfile.ZipFile(path_zip, 'w') as myzip:
                        myzip.writestr(text_name_zip, new_content_zip)
                        print(new_content_zip)
                elif choose_2_zip == "4":
                    myzip.printdir()
                else:
                    myzip.extractall(path=extraction_zip)
            print(f"Successful with password: {password}")
            success_flag[0] = True
            return  # Exit the function after finding a successful password
        except Exception as e:
            print(f"Error extracting with password '{password}': {e}")

def handle_rar(passwords):
    for password in passwords:
        try:
            with rarfile.RarFile(path_rar, 'r') as myrar:
                myrar.setpassword(password.encode())
                if choose_2_rar == "1":
                    rar_content = myrar.read(text_name_rar)
                    print(rar_content)
                elif choose_2_rar == "3":
                    myrar.printdir()
                else:
                    myrar.extractall(path=extraction_rar)
                    print("Successfully extracted all files.")
                    print(f"Successfully extracted {file_name}")
                    success_flag[0] = True
                    return
            print(f"Successful with password: {password}")
            return  # Exit the function after finding a successful password
        except Exception as e:
            print(f"Error extracting with password '{password}': {e}")

choose = input("Which file you want to handle: (rar/zip)\n")

if choose == "rar":
    choose_2_rar = input("How you want to handle with the file.rar: (1=read, 2=extract, 3=list)\n")
    path_rar = input("Enter the path to your rar file that you want to handle:\n")
    if choose_2_rar == "1":
        text_name_rar = input("Enter the name of the file you want to read:\n")
    elif choose_2_rar == "2":
        extraction_rar = input("Enter the path to extraction:\n")
    else:
        path_rar = input("Enter the path to your rar file that you want to handle:\n")

else:
    choose_2_zip = input("How you want to handle with the file.zip: (1=read, 2=extract, 3=write, 4=list)\n")
    path_zip = input("Enter the path to your zip file that you want to handle:\n")
    if choose_2_zip in ["1", "3"]:
        text_name_zip = input("Enter the name of the file you want to read/write:\n")
        if choose_2_zip == "3":
            additional_text_zip = input("Enter the text you want to append to the text file:\n")
    elif choose_2_zip == "2":
        extraction_zip = input("Enter the path to extraction:\n")

passwords_file_path = input("Enter the path to your text file that contains the list of passwords:\n")
with open(passwords_file_path, "r", encoding="latin-1") as b:
    passwords = b.read().splitlines()

success_flag = [False]

# Start two threads to attempt passwords
threads = []
chunk_size = len(passwords) // 2  # Split the passwords list into two chunks
for chunk in [passwords[:chunk_size], passwords[chunk_size:]]:
    if choose == "rar":
        t = Thread(target=handle_rar, args=(chunk,))
    else:
        t = Thread(target=handle_zip, args=(chunk,))
    threads.append(t)
    t.start()

# Wait for all threads to finish
for t in threads:
    t.join()

# Check if any thread succeeded
if not success_flag[0]:
    print("No correct password found.")
