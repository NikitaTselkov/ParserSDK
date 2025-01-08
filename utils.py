from playwright.async_api import Page
import random
import json
import base64

async def scroll_into_view(page: Page, selector, retry_count=10, delay=500):
    try:
        # Выполняем JavaScript для прокрутки элемента в область видимости
        await page.evaluate("document.querySelector('" + selector.replace('\'', '\"') + "').scrollIntoView({ behavior: 'smooth', block: 'center' });")
        
        # Ожидаем появления элемента
        element = await page.wait_for_selector(selector, state="visible")
        
        # Проверяем, находится ли элемент в области видимости, с попытками
        for _ in range(retry_count):
            if await element.is_visible():
                break
            await page.wait_for_timeout(delay)

    except Exception as e:
        return json.dumps({ "error": f"scroll_into_view: {e}" }, ensure_ascii=False)
    
    return ""


async def find_and_click(page: Page, selector, delay=500, timeout=3000):
    try:
        # Ждем появления элемента
        button_element = await page.wait_for_selector(selector, state="visible", timeout=timeout)

        await button_element.click()
        await page.wait_for_timeout(delay)

    except Exception as e:
        return json.dumps({ "error": f"find_and_click: {e}" }, ensure_ascii=False)

    return ""


async def get_screenshot_base64(page: Page, timeout: int = 3000):
    try:
        screenshot_bytes = await page.screenshot(timeout=timeout, type='jpeg', full_page=True)
        screenshot_base64 = base64.b64encode(screenshot_bytes).decode('utf-8')

        return json.dumps({ "value": screenshot_base64 }, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"error": f"get_screenshot_base64: {e}"}, ensure_ascii=False)


async def evaluate_script(page: Page, script):
    try:
       return json.dumps({ "value": await page.evaluate(script) }, ensure_ascii=False)

    except Exception as e:
        return json.dumps({ "error": f"evaluate_script: {e}" }, ensure_ascii=False)
    

async def select_radio(page: Page, selector, value):
    try:
        elements = await page.query_selector_all(selector)

        for element in elements:
            value_tmp = await element.evaluate("e => e.value")

            if value_tmp == value:
                await element.click()
                return ""

        return ""

    except Exception as e:
        return json.dumps({"error": f"select_radio: {e}"}, ensure_ascii=False)


async def select_option(page: Page, selector, value):
    try:
        dropdown = await page.wait_for_selector(selector)

        await dropdown.click()
        await dropdown.select_option(value=value)

        return ""

    except Exception as e:
        return json.dumps({"error": f"select_option: {e}"}, ensure_ascii=False)


async def evaluate_script_on_elements(page: Page, selector, js_command):
    try:
        elements = await page.query_selector_all(selector)

        results = []
        for element in elements:
            result = await element.evaluate(f"(e) => {{ {js_command} }}")

            if (result is not None):
                results.append(result)
        
        if (len(results) == 0):
            return ""
        
        return json.dumps({"value": results}, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"error": f"evaluate_script_on_elements: {e}"}, ensure_ascii=False)


async def goto(page: Page, url: str, retry_count: int = 3, wait_until: str = "networkidle"):
    for _ in range(retry_count):
        try:
            await page.goto(url, wait_until=wait_until)
            return ""
        except Exception as e:
            continue

    return json.dumps({ "error": f"navigate: {e}" }, ensure_ascii=False)


async def is_element_on_page(page: Page, selector):
    try:
        await page.wait_for_timeout(timeout=1000)
        await page.wait_for_selector(selector, state="visible", timeout=2000)

        return json.dumps({ "value": True }, ensure_ascii=False)

    except Exception as e:
        return json.dumps({ "value": False }, ensure_ascii=False)


async def get_captcha_base64(page: Page, selector):
    try:
        img_element = await page.wait_for_selector(selector)

        await img_element.hover()

        js_clip = await img_element.evaluate("""
            e => {
                const rect = e.getBoundingClientRect();
                return {
                    x: rect.x,
                    y: rect.y,
                    width: rect.width,
                    height: rect.height
                };
            }
        """)

        screenshot_bytes = await page.screenshot(
            type='jpeg',
            clip={
                "x": js_clip["x"],
                "y": js_clip["y"],
                "width": js_clip["width"],
                "height": js_clip["height"]
            }
        )

        screenshot_base64 = base64.b64encode(screenshot_bytes).decode('utf-8')
        return json.dumps({ "value": screenshot_base64 }, ensure_ascii=False)
    
    except Exception as e:
        return json.dumps({ "error": f"get_captcha_base64: {e}" }, ensure_ascii=False)


async def wait_for_selector(page: Page, selector, timeout=3000):
    try:
        # Ждем появления элемента
        await page.wait_for_selector(selector, state="visible", timeout=timeout)

    except Exception as e:
        return json.dumps({ "error": f"wait_for_selector: {e}" }, ensure_ascii=False)

    return ""


async def wait_navigation(page: Page, timeout: int, url_parts: list[str]):
    try:
        script = " || ".join(f"window.location.href.indexOf('{url_part}') > -1" for url_part in url_parts if url_part.strip())

        if not script:
            raise ValueError("At least one valid url_part must be provided.")

        await page.wait_for_function(script, timeout=timeout)

    except Exception as e:
        return json.dumps({ "error": f"wait_navigation: {e}" }, ensure_ascii=False)

    return ""


async def fill(page: Page, selector, data):
    try:
        # Ждем появления элемента
        element = await page.wait_for_selector(selector)
        await element.click()
        
        # Очищаем значение в элементе через JavaScript
        await element.evaluate("e => e.value = ''")
        
        # Вводим строку по символам с задержкой
        for char in data:
            await page.wait_for_timeout(random.uniform(90, 200))  # Случайная задержка от 90 до 200 мс
            await element.type(char)

    except Exception as e:
        return json.dumps({ "error": f"set_data: {e}" }, ensure_ascii=False)

    return ""