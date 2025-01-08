# Документация для класса `ParserScenario`

`ParserScenario` — это класс для создания сценариев автоматизированного взаимодействия с веб-страницами. Сценарий формируется из последовательности команд, которые затем конвертируются в JSON-формат для отправки и выполнения.

## Методы

| Метод                       | Описание                                                   | Параметры                                                                                                                                                                                                 |
|-----------------------------|-----------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Navigate`                  | Переходит по указанному URL.                              | `url` (string): URL для перехода.<br>`retryCount` (int): Количество попыток (по умолчанию 3).<br>`waitUntil` (NavigateWaitUntil): Условие завершения загрузки (по умолчанию `NetworkIdle`).               |
| `Fill`                      | Заполняет текстовое поле указанным значением.             | `selector` (string): CSS-селектор элемента.<br>`value` (string): Значение для ввода.                                                                                                                     |
| `Scroll`                    | Прокручивает страницу к указанному элементу.              | `selector` (string): CSS-селектор элемента.<br>`maxRetryCount` (int): Максимальное количество попыток (по умолчанию 10).<br>`delay` (int): Задержка в миллисекундах (по умолчанию 500).                  |
| `Click`                     | Нажимает на элемент.                                      | `selector` (string): CSS-селектор элемента.<br>`timeout` (int): Таймаут в миллисекундах (по умолчанию 3000).<br>`delay` (int): Задержка перед нажатием (по умолчанию 500).                                |
| `EvaluateScript`            | Выполняет JavaScript-код.                                 | `script` (string): JavaScript-код для выполнения.                                                                                                                 |
| `EvaluateScriptOnElements`  | Выполняет JavaScript-код для множества элементов.         | `selector` (string): CSS-селектор элементов.<br>`script` (string): JavaScript-код.                                                                                                                      |
| `ScreenshotBase64`          | Создаёт скриншот страницы в формате Base64.               | `timeout` (int): Таймаут в миллисекундах (по умолчанию 3000).                                                                                                     |
| `SelectOption`              | Выбирает опцию в выпадающем списке.                       | `selector` (string): CSS-селектор элемента.<br>`value` (string): Значение опции.                                                                                                                        |
| `SelectRadio`               | Устанавливает радиокнопку.                                | `selector` (string): CSS-селектор радиокнопки.<br>`value` (string): Значение радиокнопки.                                                                                                                |
| `GetCaptchaBase64`          | Получает изображение капчи в формате Base64.              | `selector` (string): CSS-селектор элемента капчи.                                                                                                                 |
| `IsElementOnPage`           | Проверяет наличие элемента на странице.                  | `selector` (string): CSS-селектор элемента.                                                                                                                       |
| `Wait`                      | Выполняет паузу на указанное время.                       | `timeout` (int): Продолжительность ожидания в миллисекундах.                                                                                                     |
| `WaitForSelector`           | Ожидает появления элемента.                               | `selector` (string): CSS-селектор элемента.<br>`timeout` (int): Таймаут в миллисекундах (по умолчанию 30000).                                                                                           |
| `WaitForNavigation`         | Ожидает завершения навигации.                             | `timeout` (int): Таймаут в миллисекундах.<br>`urlParts` (string[]): Части URL для проверки загрузки.                                                                                                    |

## Пример использования

```csharp
using ParserSDK;

using (var client = new ParserClient("http://localhost:8000", 
       new ParserConfig
       {
           BlockWebGL = true,
           GeoIP = true,
           Proxy = new ParserProxyConfig("ip:port", "login", "password")
       }))
{
    var scenario = new ParserScenario();

    scenario.Navigate("https://kad.arbitr.ru/");
    scenario.WaitForNavigation(10000, "test", "kad.arbitr");
    scenario.IsElementOnPage("[type='submit']");
    scenario.EvaluateScriptOnElements("div input[placeholder]", "return e.outerHTML");

    var result = await client.ExecuteScenario(scenario);
    var t = result.Data.Get<bool>(0);
    var t2 = result.Data.Get<List<string>>(1);
    Console.WriteLine(result);
}
