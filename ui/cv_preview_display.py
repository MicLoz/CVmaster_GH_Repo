import FreeSimpleGUI as Fsg

def show_cv_preview(content, content_store):
    """Displays the CV content in a new PySimpleGUI window."""

    #Sets the content to the stored content to keep any changes made by the user
    if content_store != "":
        content = content_store

    # Get screen size to set the window size
    screen_width, screen_height = Fsg.Window.get_screen_size()

    # Set the desired preview window size (e.g., 90% of the screen size)
    window_width = int(screen_width * 0.9)  # 90% of screen width
    window_height = int(screen_height * 0.9)  # 90% of screen height

    layout_preview = [
        [Fsg.Text("CV Preview", font=("Helvetica", 16))],
        [Fsg.Text("Char for section start and end:",font=("Courier New", 12)), Fsg.InputText(default_text="¬",
                                                                                              size=(3, 10))],
        [Fsg.Multiline(content, size=(window_width // 10, window_height // 30),
                      disabled=False, key="cv_preview_multiline_ky", autoscroll=True, font=("Courier New", 12))],
        [Fsg.Button("Close", key="close_preview_button_clicked")],
    ]
    window_preview = Fsg.Window("CV Preview", layout_preview, modal=True, enable_close_attempted_event=True)
    return window_preview

def get_stored_content(window_preview):
    return window_preview["cv_preview_multiline_ky"].get()