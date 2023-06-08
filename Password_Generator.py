import random
import string
import PySimpleGUI as sg
import pyperclip


class PembuatPassword:
    def __init__(self, panjang, kombinasi):
        self.panjang = panjang
        self.kombinasi = kombinasi

    def buat_password(self):
        if self.panjang < 8:
            sg.popup_ok(
                "Panjang password minimal 8 karakter!",
                button_color=("white", "green"),
                text_color=("black"),
                background_color=("lightblue"),
            )
            return

        if self.panjang > 20:
            sg.popup_ok(
                "Panjang password maksimal 20 karakter!",
                button_color=("white", "green"),
                text_color=("black"),
                background_color=("lightblue"),
            )
            return

        kombinasi_terpilih = []
        if self.kombinasi["kapital"]:
            kombinasi_terpilih.append(string.ascii_uppercase)
        if self.kombinasi["kecil"]:
            kombinasi_terpilih.append(string.ascii_lowercase)
        if self.kombinasi["angka"]:
            kombinasi_terpilih.append(string.digits)
        if self.kombinasi["simbol"]:
            kombinasi_terpilih.append(string.punctuation)

        if not kombinasi_terpilih:
            sg.popup_ok(
                "Harap pilih minimal satu kombinasi karakter!",
                button_color=("white", "green"),
                text_color=("black"),
                background_color=("lightblue"),
            )
            return

        password = []
        for _ in range(self.panjang):
            char_pool = random.choice(kombinasi_terpilih)
            password.append(random.choice(char_pool))

        random.shuffle(password)
        password = "".join(password)
        return password


class GUIPassword:
    def __init__(self):
        self.layout = [
            [sg.Text("Panjang Password :", text_color=("black"), background_color=("lightblue")), sg.Input(key="PANJANG")],
            [sg.Checkbox("Huruf Kapital", key="kapital", text_color=("black"), background_color=("lightblue"), pad=((100, 10), (10, 10))), sg.Checkbox("Huruf Kecil", key="kecil", text_color=("black"), background_color=("lightblue"), pad=((25, 10), (10, 10)))],
            [sg.Checkbox("Angka", key="angka", text_color=("black"), background_color=("lightblue"), pad=((100, 10), (10, 10))), sg.Checkbox("Simbol", key="simbol", text_color=("black"), background_color=("lightblue"), pad=((62, 10), (10, 10)))],
            [sg.Button("Buat Password", button_color=("white", "green"), pad=((170, 10), (0, 10)))],
            [sg.Text("Password :", text_color=("black"), background_color=("lightblue"), pad=((55, 10), (10, 10))), sg.Input(key="PASSWORD", disabled=True, pad=((0, 10), (10, 10)))],
            [sg.Text("Daftar Password", text_color=("black"), background_color=("lightblue"), pad=((160, 0), (0, 0)))],
            [sg.Listbox([], size=(40, 4), key="PASSWORD_LIST", pad=((70, 0), (0, 0)))],
            [sg.Button("Salin", button_color=("white", "blue"), pad=((200, 10), (10, 10)))],
            [sg.Button("Keluar", button_color=("white", "firebrick"), pad=((370, 10), (10, 10)))],
        ]
        self.window = sg.Window("Pembuat Password", self.layout, size=(450, 390), background_color=("lightblue"))
        self.daftar_password = []

    def update_daftar_password(self, password):
        self.daftar_password.append(password)
        self.window["PASSWORD_LIST"].update(values=self.daftar_password)

    def jalankan(self):
        while True:
            event, values = self.window.read()
            if event == "Keluar" or event == sg.WINDOW_CLOSED:
                break
            elif event == "Buat Password":
                input_panjang = values["PANJANG"]
                kombinasi = {
                    "kapital": values["kapital"],
                    "kecil": values["kecil"],
                    "angka": values["angka"],
                    "simbol": values["simbol"],
                }

                if not input_panjang:
                    sg.popup_ok(
                        "Harap masukkan panjang password!",
                        button_color=("white", "green"),
                        text_color=("black"),
                        background_color=("lightblue"),
                    )
                    continue
                try:
                    panjang = int(input_panjang)
                except ValueError:
                    sg.popup_ok(
                        "Karakter yang dimasukkan tidak valid!",
                        button_color=("white", "green"),
                        text_color=("black"),
                        background_color=("lightblue"),
                    )
                    continue

                generator = PembuatPassword(panjang, kombinasi)
                password = generator.buat_password()
                if password:
                    self.window["PASSWORD"].update(password)
                    self.update_daftar_password(password)
            elif event == "Salin":
                password_terpilih = self.window["PASSWORD_LIST"].get()
                if password_terpilih:
                    password_terpilih = password_terpilih[0]
                    pyperclip.copy(password_terpilih)

        self.window.close()


if __name__ == "__main__":
    gui = GUIPassword()
    gui.jalankan()
