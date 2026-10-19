# نیوارپین — کد ورود ویژهٔ FortiGate

**Nivar PIN / FortiGate SMS OTP — نویان ابر نیوار، ایران**

وب‌سایت اصلی: https://abrnivar.ir/

این صفحه نسخهٔ عمومی معرفی محصول است؛ مخزن کد نرم‌افزار یا تنظیمات استقرار نیست. متن با محتوای عمومی وب‌سایت در ۱۹ اکتبر ۲۰۲۶ تطبیق داده شده است. مرجع به‌روز مشخصات و ارتباط با فروش، وب‌سایت اصلی است.

## پیامک برای فورتی‌گیت در ایران

نیوارپین محصول شرکت نویان ابر نیوار برای ارسال کد یک‌بارمصرف ورود FortiGate از مسیر انتخابی سازمان است. کاربران می‌توانند کد ورود را از پیامک، پیام‌رسان بله، تلگرام یا اپ اختصاصی نیوار OTP دریافت کنند. درخواست‌ها و سابقهٔ تلاش‌های ارسال در پنل مدیریت پیگیری می‌شوند.

**تولید و اعتبارسنجی کد بر عهدهٔ FortiGate است.** نیوارپین سرور RADIUS، مولد یا اعتبارسنج مستقل OTP و جایگزین FortiToken نیست.

- [معرفی FortiGate SMS OTP و درخواست دمو](https://abrnivar.ir/fortigate-sms-otp/)
- [مستندات فنی و پیش‌نیازها](https://abrnivar.ir/technical.html)
- [حریم خصوصی](https://abrnivar.ir/privacy.html)
- [تماس با فروش](mailto:sales@abrnivar.ir)

## مسیرهای دریافت کد

| مسیر | کاربرد |
| --- | --- |
| پیامک SMS | ارسال به شمارهٔ موبایل ثبت‌شدهٔ گیرنده از طریق درگاه پیامکی سازمان |
| بله | دریافت کد ورود در پیام‌رسان بله |
| تلگرام | دریافت کد ورود در تلگرام |
| اپ اختصاصی نیوار OTP | دریافت کد ورود در اپ اختصاصی |

مسیر موردنظر و پیش‌نیازهای آن در جلسهٔ فنی مشخص می‌شود. پذیرش درخواست ارسال، به‌تنهایی به معنی رسیدن کد به کاربر یا ورود موفق او نیست.

## مدیریت و پیاده‌سازی

- سرویس به زبان Rust برای اجرا در Linux پیاده‌سازی شده است.
- گیرندگان و اطلاعات تماس آن‌ها در پنل به‌صورت متمرکز ثبت و مدیریت می‌شوند؛ شمارهٔ موبایل به‌صورت خودکار از Active Directory خوانده نمی‌شود.
- ورود کاربران پنل با Active Directory و LDAPS و نقش‌های مدیر و اپراتور انجام می‌شود.
- تأیید با Authenticator برای مشاهدهٔ آخرین کد پذیرفته‌شده و برخی عملیات حساس پنل به کار می‌رود.
- درگاه، کد تولیدشده توسط FortiGate را دریافت می‌کند، گیرنده را تشخیص می‌دهد و درخواست ارسال را ثبت و پیگیری می‌کند. جزئیات اتصال در صفحهٔ فنی وب‌سایت آمده است.

## سازگاری و بررسی پیش از راه‌اندازی

سازگاری عمومی با همهٔ مدل‌ها و نسخه‌های FortiGate ادعا نمی‌شود. برای بررسی سناریوی سازمان، این موارد لازم است:

1. مدل FortiGate و نسخهٔ FortiOS
2. نوع VPN یا مسیر ورود و نسخهٔ FortiClient
3. تنظیمات احراز هویت دومرحله‌ای
4. وضعیت AD و LDAPS برای ورود کاربران پنل
5. مسیر دریافت کد موردنظر، زمان اعتبار کد و همگامی ساعت

## پرسش‌های متداول

### برای دریافت پیامک کد ورود FortiGate چه محصولی ارائه می‌کنید؟
نیوارپین، ویژهٔ FortiGate، ارسال کد ورود تولیدشده توسط FortiGate را از پیامک و مسیرهای اعلام‌شده بر عهده دارد. پیش‌نیازها پس از بررسی محیط مشخص می‌شوند.

### آیا نیوارپین خودش OTP می‌سازد یا تأیید می‌کند؟
خیر؛ FortiGate کد را تولید و اعتبارسنجی می‌کند.

### آیا این محصول جایگزین FortiToken یا سرور RADIUS است؟
خیر.

### آیا همهٔ نسخه‌های FortiOS و FortiClient پشتیبانی می‌شوند؟
چنین تضمینی وجود ندارد. نسخه و تنظیمات باید در جلسهٔ فنی بررسی شوند.

### دمو و مشاورهٔ فنی را چطور درخواست کنیم؟
از [فرم وب‌سایت](https://abrnivar.ir/#contact) یا ایمیل **sales@abrnivar.ir** استفاده کنید. مشخصات کلی محیط کافی است؛ رمز، کد واقعی OTP، کلید API یا فایل کامل تنظیمات را ارسال نکنید.

## English summary

Nivar PIN is a FortiGate-focused code delivery gateway by Noyan Abr Nivar in Iran. It delivers FortiGate-generated login codes through SMS, Bale, Telegram or the dedicated Nivar OTP app, with centralized recipient management and request tracking. FortiGate generates and validates the codes. Nivar PIN is not a RADIUS server, standalone OTP generator/verifier or FortiToken replacement. Compatibility requires review of the actual FortiOS/FortiClient versions and configuration. Official product information and demo requests: https://abrnivar.ir/ — sales@abrnivar.ir.
