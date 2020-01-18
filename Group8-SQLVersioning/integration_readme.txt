Q1. Bizden script istediklerinde scripti nasıl döneceğiz?

A1. op=get_script yok. Bizden script istemeyecekler. Operate ile konuştum. Söyledikleri üzere; Operasyonlar arasında bu yok. Aşağıda paylaştığım çalışma akışı dışında proje ile kesiştiğimiz yer yok(muş):



Q2. Script yoksa nasıl hata vereceğiz?

A2. op=get_script yok.


Q3. Yeni script geldiğinde scripti versiyonladıysak ne döneceğiz?

A3. Versiyonladığımız zaman Plan grubuna json dosyasını ('result'=true) göndereceğiz. Trello'da gösterecekler.

Q4. Versiyonlanmadıysa ne döneceğiz?

A3. Versiyonlamadığımız zaman Plan grubuna json dosyasını ('result') göndereceğiz. Trello'da gösterecekler.


Plan grubu bizim json formatına uyacak. Bunu baz aldım:

# {"origin": 8, "destination": 4, "name": "b", "result": false}   


Plan grubuna key 'result' olarak -kesin- belirlendi.
Bize json gönderecek olan tek grup Plan grubu. Diğer key'leri de biliyor.

Python 2.7'de çalışacakmış, onu da test edelim lütfen. 
