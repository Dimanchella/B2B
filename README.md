# Личный Кабинет Контрагента
--------------------------
## Personal Market Place (B2B)

1C <-> Django

https://nizamov.school/courses/integration1s/django-1c/
```
	frontend - nuxt
	backend - django
	source - код 1С:
	#backup - cfe-выгрузка расширения
		0 - исходное состояние на начало работы
		atomatix - тексты модулей
		b2b - код низамова
		xml - xml выгрузка расширения
```
Функции трассировки запросов:

1С:

web_ОбщегоНазначенияПовтИсп.Трассировка()

backend:

config.py:

ПРИМЕР (catalogs.serializer):
```
from config import IsDebug, IsPrintExceptions, print_exception, print_to

class ImagesSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4)

    ...

    def save(self, **kwargs):
        response = None
        try:
            request = self.context.get('request', None)
            #if self.instance and self.instance.image:
            #    self.instance.image.delete()
            if self.is_valid(raise_exception=True):
                response = super().save(**kwargs)
        except Exception as err:
            if IsPrintExceptions:
                print_exception(stack=True, request=request)
        return response
```
source\\#backup - выгрузка конфигурации расширения 1С (cfe)

Changes list:

### 20240315

Images backend loader:

- 1C common extended modules, source/atomatix: 
	- web_Обмен
	- web_Справочники
	- web_ОбщегоНазначенияПовтИсп
	- web_СписокОбменаССайтомМодульФормыСписка
	- НоменклатураПрисоединенныеФайлыМодульМенеджера
	- СправочникНоменклатураМодульМенеджера

- 1C tracing function routine 
- multipartform action request content structure

- backend:
	- config.py: IsDebug, IsPrintExceptions, print_exception, print_to
	- catalogs.serializers.ImagesSerializer.save()
	- localhost.settings, django_extensions: python manage.py show_urls

### 20240321

Input cart count value type for product item: 

https://github.com/ichar/localhost.1c/blob/main/screenshots/Screenshot_20240321_111751.png
https://github.com/ichar/localhost.1c/blob/main/screenshots/Screenshot_20240321_111840.png
https://github.com/ichar/localhost.1c/blob/main/screenshots/Screenshot_20240321_112005.png

- frontend:

	- components.Order.CartSwitch.vue, input class="product-count"
	- style scoped.product-count
	- stores.cart.js.ChangeFromCart


### 20240325

selected group click (include nested catalog items):

	- price.vue.groupClick
	- price.js.getPriceList
	- app.vue, theme.global.IsDebug = 1; // XXX flag to project debug option

### 20240324-20240325

merge localhost

source:
	- web_Price
	- web_Документы
	- web_Обмен
	- web_ОбщегоНазначенияПовтИсп
	- web_Справочники

backend.debug

### 20240326

backend:

	- documents_exchangenode: добавить заказ в выгрузки

frontend:

	- stores.orders.js updateOrder:
```
      order.value.from_frontend = true
```
1С:

	- общий модуль web_Обмен.ОтправитьОбъектНаСайт:
```
      АдресРесурса = ПолучитьАдресРесурса(URL); // ??? , СсылкаНаОбъект
```     

### 20240327

backend:

	- documents.view.NewOrderView:
```        
        order.contractor = request.user.contractor
        order.partner = request.user.contractor.partner
        
        ...
        
        order.save()
``` 
 frontend:
 
	- Core.AppBarVue:  current username info
```
        <div name="username" class="username">{{ data.user.username }}</div>
        <script>

          ...
          const {data, token} = useAuthState()

        </script>
``` 

### 20240328

Отображение полей карточки заказа: Организация, Контрагент, Соглашение, Договор
Ошибки в определении идентификаторов: organizations, agreements, contracts, counterparty (contractors).

backend:
- catalogs
	- urls.py
	- views.py

frontend:
- stores/catalogs.js:
	- export const useCatalogsStore = defineStore('catalogsStore', () => { ... }
- server/api/v1:
	- counterparty.get.js
	- agreement.get.js
	- contract.js или contract.get.js ?
	- organization.get.js

Input product count value for order's product item: 

pages/order/[uuid].vue:
```
	<!-- <span>{{ item.quantity }} шт.</span>-->
	<input
		class="product-count"
		type="text"
		v-bind:value="productCount(item.quantity)"
		v-on:change="changeProductCount(item, $event.target.value)"
		:disabled="disabled()"
	/>

const changeProductCount = (product, value) => { ... }
const productCount = (value) => { ... }
<style scoped>
.product-count { ... }
</style>
```

### 20240329

Выполено слияние

frontend:
- stores/price.js:
	- export const useCatalogsStore = defineStore('priceStore', () => { ... }):
        - const getPriceList = async (is_root) => { ... }
```
count.value = data.value?.results.count
numPages.value = data.value?.results.num_pages
perPage.value = data.value?.results.per_page
currentPage.value = data.value?.results.current_page
products.value = data.value?.results.results
```

1C:
- Документы/ЗаказКлиента/Реквизиты:
    - web_ЗагруженССайта
- Общие модули/web_Документы:
    - ДобавитьОбновитьЗаказ
```
ДокументОбъект.web_ЗагруженССайта = Истина;
```
- Общие модули/web_Обмен:
    - web_РегистрацияДокументовПриЗаписи
```
Если Источник.ПометкаУдаления ИЛИ Источник.web_ЗагруженССайта Тогда
	Возврат;
КонецЕсли;
```

### 20240330

Сверка и тестирование (validate)

backend/documents/views.py NewOrderView.post:
```
        if request.user.contractor is not None:
            order.contractor = request.user.contractor
            order.partner = request.user.contractor.partner
```
Скрипты:

- frontend/setup.sh - установка frontend
- frontend/run.sh - запуск frontend
- backend/run.sh - запуск backend
- show.sh - запуск проекта

Документация:

- Deploy B2B.txt
- README.md
- Шпаргалка.txt

### 20240405-20240408

backend:

	- модель базы данных (оптимизация, имена таблиц)
	
	- параметризуемый shell-скрипт запуска backend: run.sh

	- python manage.py collectstatic

### 20240409

frontend:

	- авторизация: server/api/auth/[...].ts:	
```
async function refreshAccessToken(token: JWT) {
  try:

  ... (общий try блок)

  } catch (error) {
  ...
  }
}

callbacks: {

  async jwt({ token, user, account }) {

    ... (перегруппировка условий)

    else if (!isNaN(token.accessTokenExpires) && Date.now() > token.accessTokenExpires) {
    ...
    }
    else if (token && user) {
    ...
    }
    return { ...token, ...user }
  }
```

### 20240410

1С:
	- ОбщийМодуль.web_ОбщегоНазначенияПовтИсп: переименован общий модуль (web_ОбщегоНазначения) и все ссылки в коде

	- Перечисления.web_ВидыНастроек: изменен тип параметра настройки соединения Порт (введена Строка вместо Числа)

	- ОбщийМодуль.web_Обмен.СформироватьНастройкиСоединения: добавлен контроль типов параметров соединения


