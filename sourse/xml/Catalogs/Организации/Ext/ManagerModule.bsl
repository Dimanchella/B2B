﻿Функция ОтправитьНаСайт(СсылкаНаОбъект, ПолнаяВыгрузка) Экспорт
	Возврат web_Справочники.ОтправитьОрганизацию(СсылкаНаОбъект, ПолнаяВыгрузка);
КонецФункции

Функция ПолучитьСвязанныеСсылки(СсылкаНаОбъект) Экспорт
	СписокСсылок = Новый Соответствие;
	СписокСсылок.Вставить(СсылкаНаОбъект, 0);	
	Возврат СписокСсылок;
КонецФункции