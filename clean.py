# Fix non-breaking spaces in a script file
docu = str(input("masukan script python (.py): "))

with open(docu, "r", encoding="utf-8") as f:
    code = f.read()

code = code.replace('\u00A0', ' ')

with open(docu, "w", encoding="utf-8") as f:
    f.write(code)

print(f"Non-breaking spaces replaced. Use {docu}")

