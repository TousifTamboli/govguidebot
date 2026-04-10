with open("app.py", "r") as f:
    lines = f.readlines()

for i in range(149, 292): # line 150 to line 293 (0-indexed 149 to 292)
    line = lines[i]
    if line.strip() and not line.startswith("            "): 
        if line.startswith("        ") and "login_btn.click" in line: # leave handlers alone if possible, but wait
            pass
        # Just add 4 spaces
        lines[i] = "    " + line

with open("app.py", "w") as f:
    f.writelines(lines)
