﻿
&НаКлиенте
Процедура ОбработкаКоманды(ПараметрКоманды, ПараметрыВыполненияКоманды)
	ЗагрузитьЗаказыССайта();	
КонецПроцедуры

&НаСервере
Процедура ЗагрузитьЗаказыССайта()
	web_Обмен.ЗагрузитьЗаказыССайта();	
КонецПроцедуры