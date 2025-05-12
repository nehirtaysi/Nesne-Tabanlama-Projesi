from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
import json
import os

class Hasta:
    def __init__(self, isim, tc):
        self.isim = isim
        self.tc = tc
        self.randevu_gecmisi = []

    def randevu_ekle(self, randevu):
        self.randevu_gecmisi.append(randevu)


class Doktor:
    def __init__(self, isim, uzmanlik):
        self.isim = isim
        self.uzmanlik = uzmanlik
        self.musaitlik = []  # uygun randevu saatleri

    def musaitlik_ekle(self, tarih):
        self.musaitlik.append(tarih)

    def musait_mi(self, tarih):
        return tarih in self.musaitlik

    def musaitlik_sil(self, tarih):
        if tarih in self.musaitlik:
            self.musaitlik.remove(tarih)


class Randevu:
    def __init__(self, tarih, doktor, hasta):
        self.tarih = tarih
        self.doktor = doktor
        self.hasta = hasta



class RandevuSistemi:
    def __init__(self):
        self.hastalar = []
        self.doktorlar = []
        self.randevular = []

    def hasta_ekle(self, hasta):
        self.hastalar.append(hasta)

    def doktor_ekle(self, doktor):
        self.doktorlar.append(doktor)

    def randevu_al(self, hasta_tc, doktor_isim, tarih):
        hasta = self.hasta_bul(hasta_tc)
        doktor = self.doktor_bul(doktor_isim)

        if doktor and doktor.musait_mi(tarih):
            yeni_randevu = Randevu(tarih, doktor, hasta)
            self.randevular.append(yeni_randevu)
            hasta.randevu_ekle(yeni_randevu)
            doktor.musaitlik_sil(tarih)
            print("Randevu başarıyla alındı.")
        else:
            print("Seçilen doktor bu tarihte müsait değil.")

    def randevu_iptal(self, hasta_tc, tarih):
        for r in self.randevular:
            if r.hasta.tc == hasta_tc and r.tarih == tarih:
                self.randevular.remove(r)
                r.doktor.musaitlik_ekle(tarih)
                print("Randevu iptal edildi.")
                return
        print("Belirtilen kriterlerde bir randevu bulunamadı.")

    def hasta_bul(self, tc):
        return next((h for h in self.hastalar if h.tc == tc), None)

    def doktor_bul(self, isim):
        return next((d for d in self.doktorlar if d.isim == isim), None)









class Ui_hastanerandevusistemi(object):
    def setupUi(self, hastanerandevusistemi):
        hastanerandevusistemi.setObjectName("hastanerandevusistemi")
        hastanerandevusistemi.resize(1000, 585)
        hastanerandevusistemi.setWindowTitle("Hastane Randevu Sistemi")
        hastanerandevusistemi.setStyleSheet("background-color:#F5F5DC	;")

        # Title label
        self.hastanerandevusistemitxt = QtWidgets.QLabel(hastanerandevusistemi)
        self.hastanerandevusistemitxt.setGeometry(QtCore.QRect(170, 40, 630, 50))
        font = QtGui.QFont("MS Shell Dlg 2", 14, QtGui.QFont.Bold)
        font.setItalic(True)
        self.hastanerandevusistemitxt.setFont(font)
        self.hastanerandevusistemitxt.setText("HASTANE RANDEVU SİSTEMİ")
        self.hastanerandevusistemitxt.setAlignment(QtCore.Qt.AlignCenter)
        self.hastanerandevusistemitxt.setStyleSheet("color: #800000;")

        # Hospital selection text
        self.hastanetxt = QtWidgets.QTextEdit(hastanerandevusistemi)
        self.hastanetxt.setGeometry(QtCore.QRect(100, 150, 250, 36))
        self.hastanetxt.setHtml("<p align=\"center\"><span style=\" color:#A52A2A;\">HASTANE SEÇİNİZ</span></p>")
        self.hastanetxt.setReadOnly(True)
        self.hastanetxt.setStyleSheet("background-color: transparent; color: #A52A2A;")

        # Hospital combo box
        self.hastanebox = QtWidgets.QComboBox(hastanerandevusistemi)
        self.hastanebox.setGeometry(QtCore.QRect(100, 175, 250, 30))
        self.hastanebox.addItems([
            "Arnavutköy Devlet Hastanesi", "Beşiktaş Sait Çiftçi Devlet Hastanesi", "Beykoz Devlet Hastanesi",
            "Avcılar Murat Kölük Devlet Hastanesi", "Başakşehir Devlet Hastanesi", "Bahçelievler Devlet Hastanesi",
            "Bayrampaşa Devlet Hastanesi", "Çatalca İlyas Çokay Devlet Hastanesi", "Eyüpsultan Devlet Hastanesi",
            "Kağıthane Devlet Hastanesi", "Pendik Devlet Hastanesi", "Tuzla Devlet Hastanesi", "Silivri Devlet Hastanesi",
            "Şile Devlet Hastanesi", "Üsküdar Devlet Hastanesi", "Beylikdüzü Devlet Hastanesi"
        ])
        self.hastanebox.setStyleSheet("background-color: #FFFFF0; color: black; padding: 5px; border: 1px solid #cccccc;")

        # Clinic selection text
        self.polikinliktxt = QtWidgets.QTextEdit(hastanerandevusistemi)
        self.polikinliktxt.setGeometry(QtCore.QRect(375, 150, 250, 36))
        self.polikinliktxt.setHtml("<p align=\"center\"><span style=\" color:#A52A2A;\">POLİKİNLİK SEÇİN</span></p>")
        self.polikinliktxt.setReadOnly(True)
        self.polikinliktxt.setStyleSheet("background-color: transparent; color: #A52A2A;")

        # Clinic combo box
        self.polikinlikbox = QtWidgets.QComboBox(hastanerandevusistemi)
        self.polikinlikbox.setGeometry(QtCore.QRect(375, 175,250, 30))
        self.polikinlikbox.addItems([
            "Dahiliye (İç Hastalıkları)", "Kardiyoloji (Kalp ve Damar Hastalıkları)",
            "Gastroenteroloji (Sindirim Sistemi Hastalıkları)", "Kadın Hastalıkları ve Doğum",
            "Çocuk Sağlığı ve Hastalıkları (Pediatri)", "Nöroloji (Sinir Sistemi Hastalıkları)",
            "Göz Hastalıkları (Oftalmoloji)", "Dermatoloji (Cildiye)", "Üroloji (İdrar Yolları ve Erkek Sağlığı)"
        ])
        self.polikinlikbox.setStyleSheet("background-color: #FFFFF0; color: black; padding: 5px; border: 1px solid #cccccc;")

        # Doctor selection text
        self.doktortxt = QtWidgets.QTextBrowser(hastanerandevusistemi)
        self.doktortxt.setGeometry(QtCore.QRect(650, 150, 250, 36))
        self.doktortxt.setHtml("<p align=\"center\"><span style=\" color:#A52A2A;\">DOKTOR SEÇİMİ YAPIN</span></p>")
        self.doktortxt.setStyleSheet("background-color: transparent; color: #A52A2A;")

        # Doctor combo box
        self.doktorbox = QtWidgets.QComboBox(hastanerandevusistemi)
        self.doktorbox.setGeometry(QtCore.QRect(650, 175, 250, 30))
        self.doktorbox.addItems([
            "Prof.Dr. AHMET KEMALETTİN KOLTKA", "Prof.Dr. FİGEN ESEN", "Prof.Dr. MELTEM SAVRAN KARADENİZ",
            "Doç.Dr. HALİL ÇETİNGÖK", "Doç.Dr. ACHMET ALI", "Doç.Dr. DEMET ALTUN BİNGÖL",
            "Dr.Öğr.Üyesi HACER AYŞEN YAVRU", "Dr.Öğr.Üyesi İLKAY ANAKLI", "Dr.Öğr.Üyesi ÖZLEM POLAT",
            "Öğr. Gör. Dr. BASRİ AKDOĞAN", "Öğr. Gör. Dr. EBRU EMRE DEMİREL", "Öğr. Gör. Dr. EMRE SERTAÇ BİNGÜL",
            "Arş.Gör.Dr. AHMET BOZBAY", "Arş.Gör.Dr. AYŞE HÜMA KALYONCU", "Arş.Gör.Dr. AYŞENUR AVARİSLİ"
        ])
        self.doktorbox.setStyleSheet("background-color: #FFFFF0; color: black; padding: 5px; border: 1px solid #cccccc;")

        # TC number text
        self.tctxt = QtWidgets.QTextEdit(hastanerandevusistemi)
        self.tctxt.setGeometry(QtCore.QRect(100, 250, 250, 36))
        self.tctxt.setHtml("<p align=\"center\"><span style=\" font-size:7pt; color:#A52A2A;\">TC KİMLİK NO GİRİNİZ</span></p>")
        self.tctxt.setReadOnly(True)
        self.tctxt.setStyleSheet("background-color: transparent; color: #A52A2A;")

        # TC number input
        self.tcline = QtWidgets.QLineEdit(hastanerandevusistemi)
        self.tcline.setGeometry(QtCore.QRect(100, 275, 250, 30))
        self.tcline.setStyleSheet("background-color: #FFFFF0; color: #black; padding: 5px; border: 1px solid #cccccc;")

        # Name text
        self.adtxt = QtWidgets.QTextEdit(hastanerandevusistemi)
        self.adtxt.setGeometry(QtCore.QRect(375, 250, 250, 36))
        self.adtxt.setHtml("<p align=\"center\"><span style=\" font-size:7pt; color:#A52A2A;\">ADINIZI GİRİNİZ</span></p>")
        self.adtxt.setReadOnly(True)
        self.adtxt.setStyleSheet("background-color: transparent; color: #A52A2A;")

        # Name input
        self.adline = QtWidgets.QLineEdit(hastanerandevusistemi)
        self.adline.setGeometry(QtCore.QRect(375, 275, 250, 30))
        self.adline.setStyleSheet("background-color: #FFFFF0; color: black; padding: 5px; border: 1px solid #cccccc;")

        # Surname text
        self.soyadtxt = QtWidgets.QTextEdit(hastanerandevusistemi)
        self.soyadtxt.setGeometry(QtCore.QRect(650, 250, 250, 36))
        self.soyadtxt.setHtml("<p align=\"center\"><span style=\" font-size:7pt; color:#A52A2A;\">SOY ADINIZI GİRİNİZ</span></p>")
        self.soyadtxt.setReadOnly(True)
        self.soyadtxt.setStyleSheet("background-color: transparent; color: black;")

        # Surname input
        self.soyadline = QtWidgets.QLineEdit(hastanerandevusistemi)
        self.soyadline.setGeometry(QtCore.QRect(650, 275, 250, 30))
        self.soyadline.setStyleSheet("background-color: #FFFFF0; color: black; padding: 5px; border: 1px solid #cccccc;")

        # Date text
        self.tarihtxt = QtWidgets.QTextEdit(hastanerandevusistemi)
        self.tarihtxt.setGeometry(QtCore.QRect(200, 360, 250, 30))
        self.tarihtxt.setHtml("<p align=\"center\"><span style=\" font-size:7pt; color:#A52A2A;\">TARİH SEÇİNİZ</span></p>")
        self.tarihtxt.setReadOnly(True)
        self.tarihtxt.setStyleSheet("background-color: transparent; color: black;")

        # Date edit
        self.dateEdit = QtWidgets.QDateEdit(hastanerandevusistemi)
        self.dateEdit.setGeometry(QtCore.QRect(200, 390, 250, 30))
        self.dateEdit.setStyleSheet("background-color: #FFFFF0; color: black; padding: 5px; border: 1px solid #cccccc;")
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setMinimumDate(QtCore.QDate.currentDate())  # Prevent past dates

        # Time text
        self.saattxt = QtWidgets.QTextEdit(hastanerandevusistemi)
        self.saattxt.setGeometry(QtCore.QRect(550, 360, 250, 30))
        self.saattxt.setHtml("<p align=\"center\"><span style=\" font-size:7pt; color:#A52A2A;\">SAAT SEÇİNİZ</span></p>")
        self.saattxt.setReadOnly(True)
        self.saattxt.setStyleSheet("background-color: transparent; color: #A52A2A;")

        # Time edit
        self.timeEdit = QtWidgets.QTimeEdit(hastanerandevusistemi)
        self.timeEdit.setGeometry(QtCore.QRect(550, 390, 250, 30))
        self.timeEdit.setStyleSheet("background-color: #FFFFF0; color: #black lack; padding: 5px; border: 1px solid #cccccc;")

        # Save button
        self.saveButton = QtWidgets.QPushButton(hastanerandevusistemi)
        self.saveButton.setGeometry(QtCore.QRect(400, 480, 200, 40))
        self.saveButton.setText("Randevuyu Kaydet")
        self.saveButton.setStyleSheet("background-color:#FFFFF0 ; color: #A52A2A; border: none; padding: 8px; ")
        self.saveButton.clicked.connect(self.save_to_json)

    def save_to_json(self):
        # Collect data from UI
        appointment = {
            "hospital": self.hastanebox.currentText(),
            "clinic": self.polikinlikbox.currentText(),
            "doctor": self.doktorbox.currentText(),
            "tc_number": self.tcline.text(),
            "name": self.adline.text(),
            "surname": self.soyadline.text(),
            "date": self.dateEdit.date().toString("yyyy-MM-dd"),
            "time": self.timeEdit.time().toString("HH:mm")
        }

        # Path to JSON file
        json_file = "appointments.json"

        # Load existing data or create new
        if os.path.exists(json_file):
            with open(json_file, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = {"appointments": []}
        else:
            data = {"appointments": []}

        # Append new appointment
        data["appointments"].append(appointment)

        # Save to JSON file
        with open(json_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        # Show confirmation
        QtWidgets.QMessageBox.information(None, "Başarılı", "Randevu kaydedildi!")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    hastanerandevusistemi = QtWidgets.QWidget()
    ui = Ui_hastanerandevusistemi()
    ui.setupUi(hastanerandevusistemi)
    hastanerandevusistemi.show()
    sys.exit(app.exec_())

class Ui_hastanerandevusistemi(object):
    def setupUi(self, hastanerandevusistemi):
        hastanerandevusistemi.setObjectName("hastanerandevusistemi")
        hastanerandevusistemi.resize(800, 400)
        hastanerandevusistemi.setWindowTitle("Form")
        hastanerandevusistemi.setStyleSheet("background-color: white;")

        # Title label (replaced QTextEdit with QLabel for cleaner rendering)
        self.hastanerandevusistemitxt = QtWidgets.QLabel(hastanerandevusistemi)
        self.hastanerandevusistemitxt.setGeometry(QtCore.QRect(200, 20, 400, 50))  # Adjusted width and height
        font = QtGui.QFont("MS Shell Dlg 2", 14, QtGui.QFont.Bold)  # Increased font size slightly
        font.setItalic(True)
        self.hastanerandevusistemitxt.setFont(font)
        self.hastanerandevusistemitxt.setText("HASTANE RANDEVU SİSTEMİ")
        self.hastanerandevusistemitxt.setAlignment(QtCore.Qt.AlignCenter)
        self.hastanerandevusistemitxt.setStyleSheet("color: #000000;")
        self.hastanerandevusistemitxt.setObjectName("hastanerandevusistemitxt")

        # Hospital selection text
        self.hastanetxt = QtWidgets.QTextEdit(hastanerandevusistemi)
        self.hastanetxt.setGeometry(QtCore.QRect(50, 70, 180, 31))
        self.hastanetxt.setHtml(
            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
            "<span style=\" color:#000000;\">HASTANE SEÇİNİZ</span></p></body></html>"
        )
        self.hastanetxt.setObjectName("hastanetxt")
        self.hastanetxt.setReadOnly(True)
        self.hastanetxt.setStyleSheet("background-color: transparent; color: black;")

        # Hospital combo box
        self.hastanebox = QtWidgets.QComboBox(hastanerandevusistemi)
        self.hastanebox.setGeometry(QtCore.QRect(50, 110, 180, 25))
        self.hastanebox.addItems([
            "Arnavutköy Devlet Hastanesi",
            "Beşiktaş Sait Çiftçi Devlet Hastanesi",
            "Beykoz Devlet Hastanesi",
            "Avcılar Murat Kölük Devlet Hastanesi",
            "Başakşehir Devlet Hastanesi",
            "Bahçelievler Devlet Hastanesi",
            "Bayrampaşa Devlet Hastanesi",
            "Çatalca İlyas Çokay Devlet Hastanesi",
            "Eyüpsultan Devlet Hastanesi",
            "Kağıthane Devlet Hastanesi",
            "Pendik Devlet Hastanesi",
            "Tuzla Devlet Hastanesi",
            "Silivri Devlet Hastanesi",
            "Şile Devlet Hastanesi",
            "Üsküdar Devlet Hastanesi",
            "Beylikdüzü Devlet Hastanesi"
        ])
        self.hastanebox.setObjectName("hastanebox")
        self.hastanebox.setStyleSheet("background-color: #f0f0f0; color: black; padding: 5px; border: 1px solid #cccccc;")

        # Clinic selection text
        self.polikinliktxt = QtWidgets.QTextEdit(hastanerandevusistemi)
        self.polikinliktxt.setGeometry(QtCore.QRect(300, 70, 180, 31))
        self.polikinliktxt.setHtml(
            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
            "<span style=\" color:#000000;\">POLİKİNLİK SEÇİN</span></p></body></html>"
        )
        self.polikinliktxt.setObjectName("polikinliktxt")
        self.hastanetxt.setReadOnly(True)
        self.polikinliktxt.setStyleSheet("background-color: transparent; color: black;")

        # Clinic combo box
        self.polikinlikbox = QtWidgets.QComboBox(hastanerandevusistemi)
        self.polikinlikbox.setGeometry(QtCore.QRect(300, 110, 180, 25))
        self.polikinlikbox.addItems([
            "Dahiliye (İç Hastalıkları)",
            "Kardiyoloji (Kalp ve Damar Hastalıkları)",
            "Gastroenteroloji (Sindirim Sistemi Hastalıkları)",
            "Kadın Hastalıkları ve Doğum",
            "Çocuk Sağlığı ve Hastalıkları (Pediatri)",
            "Nöroloji (Sinir Sistemi Hastalıkları)",
            "Göz Hastalıkları (Oftalmoloji)",
            "Dermatoloji (Cildiye)",
            "Üroloji (İdrar Yolları ve Erkek Sağlığı)"
        ])
        self.polikinlikbox.setObjectName("polikinlikbox")
        self.polikinlikbox.setStyleSheet("background-color: #f0f0f0; color: black; padding: 5px; border: 1px solid #cccccc;")

        # Doctor selection text
        self.doktortxt = QtWidgets.QTextBrowser(hastanerandevusistemi)
        self.doktortxt.setGeometry(QtCore.QRect(550, 70, 180, 31))
        self.doktortxt.setHtml(
            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
            "<span style=\" color:#000000;\">DOKTOR SEÇİMİ YAPIN</span></p></body></html>"
        )
        self.doktortxt.setObjectName("doktortxt")
        self.doktortxt.setStyleSheet("background-color: transparent; color: black;")

        # Doctor combo box
        self.doktorbox = QtWidgets.QComboBox(hastanerandevusistemi)
        self.doktorbox.setGeometry(QtCore.QRect(550, 110, 180, 25))
        self.doktorbox.addItems([
            "Prof.Dr. AHMET KEMALETTİN KOLTKA",
            "Prof.Dr. FİGEN ESEN",
            "Prof.Dr. MELTEM SAVRAN KARADENİZ",
            "Doç.Dr. HALİL ÇETİNGÖK",
            "Doç.Dr. ACHMET ALI",
            "Doç.Dr. DEMET ALTUN BİNGÖL",
            "Dr.Öğr.Üyesi HACER AYŞEN YAVRU",
            "Dr.Öğr.Üyesi İLKAY ANAKLI",
            "Dr.Öğr.Üyesi ÖZLEM POLAT",
            "Öğr. Gör. Dr. BASRİ AKDOĞAN",
            "Öğr. Gör. Dr. EBRU EMRE DEMİREL",
            "Öğr. Gör. Dr. EMRE SERTAÇ BİNGÜL",
            "Arş.Gör.Dr. AHMET BOZBAY",
            "Arş.Gör.Dr. AYŞE HÜMA KALYONCU",
            "Arş.Gör.Dr. AYŞENUR AVARİSLİ"
        ])
        self.doktorbox.setObjectName("doktorbox")
        self.doktorbox.setStyleSheet("background-color: #f0f0f0; color: black; padding: 5px; border: 1px solid #cccccc;")

        # TC number text
        self.tctxt = QtWidgets.QTextEdit(hastanerandevusistemi)
        self.tctxt.setGeometry(QtCore.QRect(50, 150, 180, 31))
        self.tctxt.setHtml(
            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
            "<span style=\" font-size:7pt; color:#000000;\">TC KİMLİK NO GİRİNİZ</span></p></body></html>"
        )
        self.tctxt.setObjectName("tctxt")
        self.tctxt.setReadOnly(True)
        self.tctxt.setStyleSheet("background-color: transparent; color: black;")

        # TC number input
        self.tcline = QtWidgets.QLineEdit(hastanerandevusistemi)
        self.tcline.setGeometry(QtCore.QRect(50, 190, 180, 25))
        self.tcline.setObjectName("tcline")
        self.tcline.setStyleSheet("background-color: #f0f0f0; color: black; padding: 5px; border: 1px solid #cccccc;")

        # Name text
        self.adtxt = QtWidgets.QTextEdit(hastanerandevusistemi)
        self.adtxt.setGeometry(QtCore.QRect(300, 150, 180, 31))
        self.adtxt.setHtml(
            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
            "<span style=\" font-size:7pt; color:#000000;\">ADINIZI GİRİNİZ</span></p></body></html>"
        )
        self.adtxt.setObjectName("adtxt")
        self.adtxt.setReadOnly(True)
        self.adtxt.setStyleSheet("background-color: transparent; color: black;")

        # Name input
        self.adline = QtWidgets.QLineEdit(hastanerandevusistemi)
        self.adline.setGeometry(QtCore.QRect(300, 190, 180, 25))
        self.adline.setObjectName("adline")
        self.adline.setStyleSheet("background-color: #f0f0f0; color: black; padding: 5px; border: 1px solid #cccccc;")

        # Surname text
        self.soyadtxt = QtWidgets.QTextEdit(hastanerandevusistemi)
        self.soyadtxt.setGeometry(QtCore.QRect(550, 150, 180, 31))
        self.soyadtxt.setHtml(
            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
            "<span style=\" font-size:7pt; color:#000000;\">SOY ADINIZI GİRİNİZ</span></p></body></html>"
        )
        self.soyadtxt.setObjectName("soyadtxt")
        self.soyadtxt.setReadOnly(True)
        self.soyadtxt.setStyleSheet("background-color: transparent; color: black;")

        # Surname input
        self.soyadline = QtWidgets.QLineEdit(hastanerandevusistemi)
        self.soyadline.setGeometry(QtCore.QRect(550, 190, 180, 25))
        self.soyadline.setObjectName("soyadline")
        self.soyadline.setStyleSheet("background-color: #f0f0f0; color: black; padding: 5px; border: 1px solid #cccccc;")

        # Date text
        self.tarihtxt = QtWidgets.QTextEdit(hastanerandevusistemi)
        self.tarihtxt.setGeometry(QtCore.QRect(200, 230, 180, 31))
        self.tarihtxt.setHtml(
            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
            "<span style=\" font-size:7pt; color:#000000;\">TARİH SEÇİNİZ</span></p></body></html>"
        )
        self.tarihtxt.setObjectName("tarihtxt")
        self.tarihtxt.setReadOnly(True)
        self.tarihtxt.setStyleSheet("background-color: transparent; color: black;")

        # Date edit
        self.dateEdit = QtWidgets.QDateEdit(hastanerandevusistemi)
        self.dateEdit.setGeometry(QtCore.QRect(200, 270, 180, 25))
        self.dateEdit.setObjectName("dateEdit")
        self.dateEdit.setStyleSheet("background-color: #f0f0f0; color: black; padding: 5px; border: 1px solid #cccccc;")

        # Time text
        self.saattxt = QtWidgets.QTextEdit(hastanerandevusistemi)
        self.saattxt.setGeometry(QtCore.QRect(450, 230, 180, 31))
        self.saattxt.setHtml(
            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
            "<span style=\" font-size:7pt; color:#000000;\">SAAT SEÇİNİZ</span></p></body></html>"
        )
        self.saattxt.setObjectName("saattxt")
        self.saattxt.setReadOnly(True)
        self.saattxt.setStyleSheet("background-color: transparent; color: black;")

        # Time edit
        self.timeEdit = QtWidgets.QTimeEdit(hastanerandevusistemi)
        self.timeEdit.setGeometry(QtCore.QRect(450, 270, 180, 25))
        self.timeEdit.setObjectName("timeEdit")
        self.timeEdit.setStyleSheet("background-color: #f0f0f0; color: black; padding: 5px; border: 1px solid #cccccc;")

        self.retranslateUi(hastanerandevusistemi)
        QtCore.QMetaObject.connectSlotsByName(hastanerandevusistemi)

    def retranslateUi(self, hastanerandevusistemi):
        _translate = QtCore.QCoreApplication.translate
        hastanerandevusistemi.setWindowTitle(_translate("hastanerandevusistemi", "Form"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    hastanerandevusistemi = QtWidgets.QWidget()
    ui = Ui_hastanerandevusistemi()
    ui.setupUi(hastanerandevusistemi)
    hastanerandevusistemi.show()
    sys.exit(app.exec_())