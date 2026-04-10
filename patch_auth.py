import re

with open("app.py", "r") as f:
    content = f.read()

auth_logic = """
import hashlib

USER_FILE = "temp_users.txt"

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def do_signup(username, password):
    if not username or not password:
        return "Username and password required.", gr.update(), gr.update()
    
    users = {}
    import os
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            for line in f:
                if ":" in line:
                    u, p = line.strip().split(":", 1)
                    users[u] = p
                    
    if username in users:
        return "Username already exists.", gr.update(), gr.update()
        
    with open(USER_FILE, "a") as f:
        f.write(f"{username}:{hash_pw(password)}\\n")
        
    return "Signup successful! You can now login.", gr.update(), gr.update()

def do_login(username, password):
    if not username or not password:
        return "Username and password required.", gr.update(), gr.update()
        
    users = {}
    import os
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            for line in f:
                if ":" in line:
                    u, p = line.strip().split(":", 1)
                    users[u] = p
                    
    if username in users and users[username] == hash_pw(password):
        return "Login successful!", gr.update(visible=False), gr.update(visible=True)
        
    return "Invalid username or password.", gr.update(), gr.update()

# Create Gradio interface
"""

auth_ui = """    
    with gr.Column(visible=True) as auth_ui:
        gr.Markdown("# Welcome to GovGuideBot\\nPlease Login or Sign Up to continue.")
        with gr.Tabs():
            with gr.Tab("Login"):
                login_user = gr.Textbox(label="Username")
                login_pw = gr.Textbox(label="Password", type="password")
                login_btn = gr.Button("Login", variant="primary")
                login_msg = gr.Markdown("")
            with gr.Tab("Sign Up"):
                signup_user = gr.Textbox(label="New Username")
                signup_pw = gr.Textbox(label="New Password", type="password")
                signup_btn = gr.Button("Sign Up", variant="primary")
                signup_msg = gr.Markdown("")
                
    with gr.Column(visible=False) as main_ui:
"""

# Replace `# Create Gradio interface` with logic
content = content.replace("# Create Gradio interface\n", auth_logic)

# Replace `with gr.Blocks... as demo:\n    ` with the auth UI
blocks_match = re.search(r'(with gr\.Blocks.*?as demo:\n)(\s+)', content)
if blocks_match:
    prefix = blocks_match.group(1)
    indent = blocks_match.group(2)
    new_blocks = prefix + auth_ui

    content = content.replace(blocks_match.group(0), new_blocks)

    # Now we need to add exactly 4 spaces to everything until `# Event handlers`
    main_ui_parts = content.split("    with gr.Column(visible=False) as main_ui:\n")
    if len(main_ui_parts) == 2:
        ui_and_handlers = main_ui_parts[1].split("    # Event handlers\n")
        if len(ui_and_handlers) == 2:
            indented_ui = ""
            for line in ui_and_handlers[0].split("\n"):
                if line.strip():
                    indented_ui += "    " + line + "\n"
                else:
                    indented_ui += "\n"
            
            # Now we add the event handlers, and we MUST append the login/signup handlers
            handlers = "    # Event handlers\n"
            handlers += """
    login_btn.click(
        do_login,
        inputs=[login_user, login_pw],
        outputs=[login_msg, auth_ui, main_ui]
    )
    
    signup_btn.click(
        do_signup,
        inputs=[signup_user, signup_pw],
        outputs=[signup_msg, auth_ui, main_ui]
    )
    
"""
            handlers += ui_and_handlers[1]
            
            content = main_ui_parts[0] + "    with gr.Column(visible=False) as main_ui:\n" + indented_ui + handlers

with open("app.py", "w") as f:
    f.write(content)
print("done patching app.py")
