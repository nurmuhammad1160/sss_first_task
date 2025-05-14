# MQTT Sensor Ma'lumotlarini MongoDB ga Yig'uvchi Dastur

Ushbu loyiha ikki xil MQTT brokeridan ma'lum bir sensorlar ro'yxatiga tegishli ma'lumotlarni qabul qilib, ularni MongoDB ma'lumotlar bazasiga saqlash uchun mo'ljallangan. Ma'lumotlar ikki xil kolleksiyada saqlanadi: barcha qabul qilingan xabarlar uchun tarixiy kolleksiya va har bir sensorning eng so'nggi ma'lumotlari uchun alohida kolleksiya.

## Asosiy Xususiyatlar

* Bir vaqtning o'zida ikkita MQTT brokeriga ulanish (har biri alohida skript orqali).
* Oldindan belgilangan sensorlar ro'yxati (`sensors.json`) bo'yicha xabarlarni filtrlash.
* Ma'lumotlarni MongoDB da ikki xil ko'rinishda saqlash:
    * Barcha qabul qilingan xabarlar (`sensor_readings_historical`).
    * Har bir sensor uchun eng so'nggi ma'lumot (`sensor_last_readings`).
* Konfiguratsiya sozlamalari uchun `.env` faylidan foydalanish.
* MongoDB ga yozish operatsiyalarini alohida potoklarda (threads) bajarish orqali MQTT xabar qabul qilish oqimining bloklanishini oldini olish.
* Dastur ishlashi haqida loglar yuritish.

## Loyihani Sozlash va O'rnatish

1.  **Repozitoriyni klonlash:**
    ```bash
    git clone [https://github.com/nurmuhammad1160/sss_first_task.git](https://github.com/nurmuhammad1160/sss_first_task.git)
    ```

2.  **Loyiha papkasiga o'tish:**
    ```bash
    cd sss_first_task
    ```

3.  **Virtual muhit yaratish:**
    ```bash
    python3 -m venv env 
    ```
    (yoki `python -m venv env`)

4.  **Virtual muhitni aktivlashtirish:**
    * Linux/macOS uchun:
        ```bash
        source env/bin/activate
        ```
    * Windows uchun (Command Prompt):
        ```bash
        env\Scripts\activate.bat
        ```
    * Windows uchun (PowerShell):
        ```bash
        env\Scripts\Activate.ps1
        ```

5.  **Kerakli kutubxonalarni o'rnatish:**
    ```bash
    pip install -r requirements.txt
    ```

6.  **Konfiguratsiya Fayllarini Yaratish:**
    Loyiha to'g'ri ishlashi uchun uning asosiy papkasida (`sss_first_task` ichida) quyidagi ikkita fayl mavjud bo'lishi kerak:

    * **`.env` fayli:** Bu fayl dasturning ishlashi uchun zarur bo'lgan maxfiy sozlamalarni (masalan, brokerlarga ulanish ma'lumotlari, MongoDB ulanish satri va boshqa konfiguratsiyalar) o'z ichiga oladi.
    * **`sensors.json` fayli:** Bu faylda dastur tomonidan kuzatilishi va ma'lumotlari yig'ilishi kerak bo'lgan sensorlarning ro'yxati JSON formatida saqlanadi.

    **DIQQAT:** `.env` va `sensors.json` fayllari maxfiy yoki loyihaga xos ma'lumotlarni o'z ichiga olgani uchun ular odatda Git repozitoriyga qo'shilmaydi (`.gitignore` fayliga kiritilishi kerak). **Bu fayllarning ichidagi ma'lumotlarni ommaviy repozitoriyga yuklamang!** Ularni loyihani ishga tushirmoqchi bo'lgan shaxs o'zi yaratishi va kerakli ma'lumotlar bilan to'ldirishi zarur.

7.  **MongoDB ni O'rnatish va Ishga Tushirish:**
    MongoDB serveri kompyuteringizda o'rnatilgan va ishlab turgan bo'lishi kerak.

## Dasturni Ishga Tushirish

Dastur ikkita broker uchun alohida skriptlar orqali ishga tushiriladi. Buning uchun ikkita alohida terminal oynasidan foydalaning (har birida virtual muhit aktivlashtirilgan bo'lishi kerak):

1.  **Birinchi broker uchun skriptni ishga tushirish:**
    Terminal 1 da:
    ```bash
    python broker1_app.py
    ```

2.  **Ikkinchi broker uchun skriptni ishga tushirish:**
    Terminal 2 da:
    ```bash
    python broker2_app.py
    ```

Dastur ishga tushgach, loglar terminalda ko'rinadi. Ma'lumotlar MongoDB dagi tegishli kolleksiyalarga yozila boshlaydi.

## Loglar
Dastur ishlashi haqidagi ma'lumotlar (ulanishlar, xatolar, qabul qilingan maqsadli xabarlar) terminalga chiqariladi. Log darajasini `.env` faylidagi `LOG_LEVEL` o'zgaruvchisi orqali sozlash mumkin.

---