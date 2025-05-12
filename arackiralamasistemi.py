import sys
import json
import uuid
import hashlib
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt6.QtCore import QDateTime, QRect

class Arac:
    def __init__(self, arac_id, model):
        self.arac_id = arac_id
        self.model = model
        self.kiralanmis = False

    def arac_durumu_guncelle(self, durum):
        self.kiralanmis = durum

    def to_dict(self):
        return {
            "arac_id": self.arac_id,
            "model": self.model,
            "kiralanmis": self.kiralanmis
        }

class Musteri:
    def __init__(self, musteri_id, ad_soyad, telefon, sifre):
        self.musteri_id = musteri_id
        self.ad_soyad = ad_soyad
        self.telefon = telefon
        self.sifre = hashlib.sha256(sifre.encode()).hexdigest()

    def to_dict(self):
        return {
            "musteri_id": self.musteri_id,
            "ad_soyad": self.ad_soyad,
            "telefon": self.telefon,
            "sifre": self.sifre
        }

class Kiralama:
    def __init__(self, kiralama_id, arac, musteri, sure, kiralama_tarihi, teslim_tarihi, beyan_onay):
        self.kiralama_id = kiralama_id
        self.arac = arac
        self.musteri = musteri
        self.sure = sure
        self.ucret = sure * 600  # Günlük 600 TL
        self.kiralama_tarihi = kiralama_tarihi
        self.teslim_tarihi = teslim_tarihi
        self.beyan_onay = beyan_onay

    def kiralama_yap(self):
        if self.arac.kiralanmis:
            raise ValueError("Bu araç zaten kiralanmış.")
        self.arac.arac_durumu_guncelle(True)

    def kiralama_iptal_et(self):
        if self.arac:
            self.arac.arac_durumu_guncelle(False)
            self.arac = None
            self.musteri = None
            self.sure = 0
            self.ucret = 0
            self.kiralama_tarihi = None
            self.teslim_tarihi = None
            self.beyan_onay = False

    def kiralama_bilgisi(self):
        return {
            "kiralama_id": self.kiralama_id,
            "arac": self.arac.to_dict(),
            "musteri": self.musteri.to_dict(),
            "sure": self.sure,
            "ucret": self.ucret,
            "kiralama_tarihi": self.kiralama_tarihi,
            "teslim_tarihi": self.teslim_tarihi,
            "beyan_onay": self.beyan_onay
        }

class Ui_arackiralamasistemi(object):
    def setupUi(self, arackiralamasistemi):
        arackiralamasistemi.setObjectName("arackiralamasistemi")
        arackiralamasistemi.resize(550, 300)
        arackiralamasistemi.setWindowTitle("Araç Kiralama Sistemi")
        
        self.txtmusteri = QtWidgets.QTextBrowser(arackiralamasistemi)
        self.txtmusteri.setGeometry(QRect(50, 10, 191, 141))
        self.txtmusteri.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; font-style:italic;\">Kayıt Ol</span></p></body></html>")
        self.txtmusteri.setObjectName("txtmusteri")
        
        self.lntelefonnumara = QtWidgets.QLineEdit(arackiralamasistemi)
        self.lntelefonnumara.setGeometry(QRect(80, 30, 131, 21))
        self.lntelefonnumara.setObjectName("lntelefonnumara")
        
        self.lnkullanicadi = QtWidgets.QLineEdit(arackiralamasistemi)
        self.lnkullanicadi.setGeometry(QRect(80, 60, 131, 21))
        self.lnkullanicadi.setObjectName("lnkullanicadi")
        
        self.linesifre = QtWidgets.QLineEdit(arackiralamasistemi)
        self.linesifre.setGeometry(QRect(80, 90, 131, 20))
        self.linesifre.setObjectName("linesifre")
        
        self.bttamamla = QtWidgets.QPushButton(arackiralamasistemi)
        self.bttamamla.setGeometry(QRect(160, 130, 60, 17))
        self.bttamamla.setText("tamamla")
        self.bttamamla.setObjectName("bttamamla")
        
        self.textBrowser_2 = QtWidgets.QTextBrowser(arackiralamasistemi)
        self.textBrowser_2.setGeometry(QRect(310, 10, 191, 141))
        self.textBrowser_2.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; font-style:italic;\">Mevcut Araçlar</span></p></body></html>")
        self.textBrowser_2.setObjectName("textBrowser_2")
        
        self.radioButton = QtWidgets.QRadioButton(arackiralamasistemi)
        self.radioButton.setGeometry(QRect(320, 30, 100, 20))
        self.radioButton.setText("Toyota Corolla")
        self.radioButton.setObjectName("radioButton")
        
        self.radioButton_2 = QtWidgets.QRadioButton(arackiralamasistemi)
        self.radioButton_2.setGeometry(QRect(320, 50, 100, 20))
        self.radioButton_2.setText("Honda Civic")
        self.radioButton_2.setObjectName("radioButton_2")
        
        self.radioButton_3 = QtWidgets.QRadioButton(arackiralamasistemi)
        self.radioButton_3.setGeometry(QRect(320, 70, 100, 20))
        self.radioButton_3.setText("Ford Odak")
        self.radioButton_3.setObjectName("radioButton_3")
        
        self.radioButton_4 = QtWidgets.QRadioButton(arackiralamasistemi)
        self.radioButton_4.setGeometry(QRect(320, 90, 100, 20))
        self.radioButton_4.setText("BMW 3 Serisi")
        self.radioButton_4.setObjectName("radioButton_4")
        
        self.radioButton_5 = QtWidgets.QRadioButton(arackiralamasistemi)
        self.radioButton_5.setGeometry(QRect(320, 110, 100, 20))
        self.radioButton_5.setText("Renault Clio")
        self.radioButton_5.setObjectName("radioButton_5")
        
        self.txtkiralamatarihi = QtWidgets.QTextEdit(arackiralamasistemi)
        self.txtkiralamatarihi.setGeometry(QRect(50, 160, 191, 41))
        self.txtkiralamatarihi.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; font-style:italic;\">Kiralanma Tarihi</span></p></body></html>")
        self.txtkiralamatarihi.setObjectName("txtkiralamatarihi")
        
        self.txtteslimtarihi = QtWidgets.QTextEdit(arackiralamasistemi)
        self.txtteslimtarihi.setGeometry(QRect(310, 160, 191, 41))
        self.txtteslimtarihi.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; font-style:italic;\">Teslim Tarihi</span></p></body></html>")
        self.txtteslimtarihi.setObjectName("txtteslimtarihi")
        
        self.toolbsec = QtWidgets.QToolButton(arackiralamasistemi)
        self.toolbsec.setGeometry(QRect(440, 130, 41, 16))
        self.toolbsec.setText("seç")
        self.toolbsec.setObjectName("toolbsec")
        
        self.dateTimekt = QtWidgets.QDateTimeEdit(arackiralamasistemi)
        self.dateTimekt.setGeometry(QRect(50, 182, 191, 22))
        self.dateTimekt.setObjectName("dateTimekt")
        
        self.dateTimett = QtWidgets.QDateTimeEdit(arackiralamasistemi)
        self.dateTimett.setGeometry(QRect(310, 182, 191, 22))
        self.dateTimett.setObjectName("dateTimett")
        
        
        
        self.checkbeyan = QtWidgets.QCheckBox(arackiralamasistemi)
        self.checkbeyan.setGeometry(QRect(30, 210, 550, 31))
        self.checkbeyan.setText("Araca zarar gelecek herhangi bir durumda bütün masrafları karşılayacağımı beyan ederim.")
        self.checkbeyan.setObjectName("checkbeyan")
        
        self.pushButton = QtWidgets.QPushButton(arackiralamasistemi)
        self.pushButton.setGeometry(QRect(410, 250, 117, 20))
        self.pushButton.setText("İşlemi Tamamla")
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(arackiralamasistemi)
        QtCore.QMetaObject.connectSlotsByName(arackiralamasistemi)

    def retranslateUi(self, arackiralamasistemi):
        pass

class AracKiralamaSistemi(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_arackiralamasistemi()
        self.ui.setupUi(self)

        # Veri yapıları
        self.araclar = []
        self.musteriler = []
        self.kiralamalar = []

        # Başlangıç verilerini yükle
        self.verileri_yukle()

        # Buton olaylarını bağla
        self.ui.bttamamla.clicked.connect(self.musteri_kaydet)
        self.ui.pushButton.clicked.connect(self.kiralama_yap)
        self.ui.toolbsec.clicked.connect(self.kiralama_bilgilerini_goster)

    def verileri_yukle(self):
        # Araçları yükle
        try:
            with open("araclar.json", "r", encoding="utf-8") as f:
                arac_verileri = json.load(f)
                self.araclar = [Arac(d["arac_id"], d["model"]) for d in arac_verileri]
                for arac, veri in zip(self.araclar, arac_verileri):
                    arac.kiralanmis = veri["kiralanmis"]
        except FileNotFoundError:
            # Varsayılan araçlar
            self.araclar = [
                Arac(str(uuid.uuid4()), "Toyota Corolla"),
                Arac(str(uuid.uuid4()), "Honda Civic"),
                Arac(str(uuid.uuid4()), "Ford Odak"),
                Arac(str(uuid.uuid4()), "BMW 3 Serisi"),
                Arac(str(uuid.uuid4()), "Renault Clio")
            ]
            self.araclari_kaydet()

        # Müşterileri yükle
        try:
            with open("musteriler.json", "r", encoding="utf-8") as f:
                musteri_verileri = json.load(f)
                self.musteriler = [Musteri(d["musteri_id"], d["ad_soyad"], d["telefon"], d["sifre"]) for d in musteri_verileri]
        except FileNotFoundError:
            self.musteriler = []

        # Kiralamaları yükle
        try:
            with open("kiralamalar.json", "r", encoding="utf-8") as f:
                kiralama_verileri = json.load(f)
                for d in kiralama_verileri:
                    musteri_id = d.get("musteri", {}).get("musteri_id")
                    arac_id = d.get("arac", {}).get("arac_id")
                    musteri = next((m for m in self.musteriler if m.musteri_id == musteri_id), None)
                    arac = next((a for a in self.araclar if a.arac_id == arac_id), None)
                    if musteri and arac:
                        kiralama = Kiralama(
                            d.get("kiralama_id"),
                            arac,
                            musteri,
                            d.get("sure"),
                            d.get("kiralama_tarihi"),
                            d.get("teslim_tarihi"),
                            d.get("beyan_onay", False)
                        )
                        self.kiralamalar.append(kiralama)
        except FileNotFoundError:
            self.kiralamalar = []
        except json.JSONDecodeError:
            print("Hata: kiralamalar.json dosyası bozuk, boş bir liste kullanılacak.")
            self.kiralamalar = []

    def araclari_kaydet(self):
        with open("araclar.json", "w", encoding="utf-8") as f:
            json.dump([arac.to_dict() for arac in self.araclar], f, indent=4, ensure_ascii=False)

    def musterileri_kaydet(self):
        with open("musteriler.json", "w", encoding="utf-8") as f:
            json.dump([musteri.to_dict() for musteri in self.musteriler], f, indent=4, ensure_ascii=False)

    def kiralamalari_kaydet(self):
        with open("kiralamalar.json", "w", encoding="utf-8") as f:
            json.dump([kiralama.kiralama_bilgisi() for kiralama in self.kiralamalar], f, indent=4, ensure_ascii=False)

    def musteri_kaydet(self):
        telefon = self.ui.lntelefonnumara.text()
        ad_soyad = self.ui.lnkullanicadi.text()
        sifre = self.ui.linesifre.text()

        if not telefon or not ad_soyad or not sifre:
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen tüm müşteri bilgilerini doldurun!")
            return

        if any(m.ad_soyad == ad_soyad for m in self.musteriler):
            QMessageBox.warning(self, "Hata", "Bu kullanıcı adı zaten mevcut!")
            return

        musteri_id = str(uuid.uuid4())
        musteri = Musteri(musteri_id, ad_soyad, telefon, sifre)
        self.musteriler.append(musteri)
        self.musterileri_kaydet()
        QMessageBox.information(self, "Başarılı", "Müşteri kaydı tamamlandı!")

    def kiralama_yap(self):
        ad_soyad = self.ui.lnkullanicadi.text()
        kiralama_tarihi = self.ui.dateTimekt.dateTime().toString("yyyy-MM-dd HH:mm")
        teslim_tarihi = self.ui.dateTimett.dateTime().toString("yyyy-MM-dd HH:mm")
        beyan_onay = self.ui.checkbeyan.isChecked()

        secilen_arac = None
        if self.ui.radioButton.isChecked():
            secilen_arac = next((a for a in self.araclar if a.model == "Toyota Corolla"), None)
        elif self.ui.radioButton_2.isChecked():
            secilen_arac = next((a for a in self.araclar if a.model == "Honda Civic"), None)
        elif self.ui.radioButton_3.isChecked():
            secilen_arac = next((a for a in self.araclar if a.model == "Ford Odak"), None)
        elif self.ui.radioButton_4.isChecked():
            secilen_arac = next((a for a in self.araclar if a.model == "BMW 3 Serisi"), None)
        elif self.ui.radioButton_5.isChecked():
            secilen_arac = next((a for a in self.araclar if a.model == "Renault Clio"), None)

        if not ad_soyad or not secilen_arac:
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen kullanıcı adı ve araç seçimi yapın!")
            return

        musteri = next((m for m in self.musteriler if m.ad_soyad == ad_soyad), None)
        if not musteri:
            QMessageBox.warning(self, "Hata", "Bu kullanıcı adına sahip müşteri bulunamadı!")
            return

        if secilen_arac.kiralanmis:
            QMessageBox.warning(self, "Hata", f"{secilen_arac.model} zaten kiralık!")
            return

        kiralama_dt = QDateTime.fromString(kiralama_tarihi, "yyyy-MM-dd HH:mm")
        teslim_dt = QDateTime.fromString(teslim_tarihi, "yyyy-MM-dd HH:mm")
        if kiralama_dt >= teslim_dt:
            QMessageBox.warning(self, "Hata", "Teslim tarihi kiralama tarihinden sonra olmalı!")
            return

        sure = kiralama_dt.daysTo(teslim_dt)
        if sure <= 0:
            QMessageBox.warning(self, "Hata", "Kiralama süresi en az 1 gün olmalı!")
            return

        kiralama_id = str(uuid.uuid4())
        kiralama = Kiralama(kiralama_id, secilen_arac, musteri, sure, kiralama_tarihi, teslim_tarihi, beyan_onay)
        try:
            kiralama.kiralama_yap()
            self.kiralamalar.append(kiralama)
            self.araclari_kaydet()
            self.kiralamalari_kaydet()
            QMessageBox.information(self, "Başarılı", f"{secilen_arac.model} kiralandı! Ücret: {kiralama.ucret} TL")
        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))

    def kiralama_bilgilerini_goster(self):
        self.ui.textBrowser_2.clear()
        if not self.kiralamalar:
            self.ui.textBrowser_2.setText("Henüz kiralama yapılmamış.")
            return

        table_content = (
            "<table border='1' style='width:100%; border-collapse: collapse;'>"
            "<tr><th>Kullanıcı</th><th>Araç</th><th>Süre</th><th>Ücret</th><th>Kiralama</th><th>Teslim</th></tr>"
        )
        for kiralama in self.kiralamalar:
            table_content += (
                f"<tr><td>{kiralama.musteri.ad_soyad}</td>"
                f"<td>{kiralama.arac.model}</td>"
                f"<td>{kiralama.sure} gün</td>"
                f"<td>{kiralama.ucret} TL</td>"
                f"<td>{kiralama.kiralama_tarihi}</td>"
                f"<td>{kiralama.teslim_tarihi}</td></tr>"
            )
        table_content += "</table>"
        self.ui.textBrowser_2.setHtml(table_content)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AracKiralamaSistemi()
    window.show()
    sys.exit(app.exec())