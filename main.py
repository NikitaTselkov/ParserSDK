from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, RootModel
from camoufox.async_api import AsyncCamoufox
from browserforge.fingerprints import Screen
from browserforge.fingerprints import FingerprintGenerator
from typing import Union, Dict, Any, List, Optional

import utils

app = FastAPI()

# Хранилище браузеров и страниц
browsers: Dict[str, Dict[str, object]] = {}

class ScenarioStep(RootModel):
    root: Dict[str, Union[Dict[str, Any], int]]

class ScenarioRequest(BaseModel):
    browser_key: str  # Ключ браузера
    page_index: Optional[int] = 0  # Индекс страницы (по умолчанию первая страница)
    js_scenario: List[ScenarioStep]  # Список шагов сценария

class BrowserRequest(BaseModel):
    browser_key: str  # Уникальный ключ для идентификации браузера
    fingerprint: Optional[Dict[str, Any]] = None  # Переданный fingerprint в JSON-формате
    browser: Optional[str] = "firefox"  # Тип браузера (если fingerprint отсутствует)
    os: Optional[str] = "linux"  # ОС (если fingerprint отсутствует)
    humanize: Optional[bool] = True  # Человекообразное поведение
    block_images: Optional[bool] = False  # Блокировать изображения
    block_webgl: Optional[bool] = False  # Блокировать WebGL
    geoip: Optional[bool] = True  # Использовать GeoIP
    proxy: Optional[Dict[str, str]] = None  # Настройки прокси



@app.post("/start", summary="Запуск браузера Camoufox")
async def start_browser(request: BrowserRequest):
    # Проверка, запущен ли уже браузер с данным ключом
    if request.browser_key in browsers:
        raise HTTPException(status_code=400, detail="Браузер с данным ключом уже запущен")

    # Генерация fingerprint, если он не был передан
    fingerprint = request.fingerprint
    constrains = Screen(max_width=1920, max_height=1080)

    if not fingerprint:
        fg = FingerprintGenerator(browser=request.browser, os=request.os, screen=constrains)
        fingerprint = fg.generate()

    try:
        camoufox = AsyncCamoufox(
            fingerprint=request.fingerprint,
            humanize=request.humanize,
            block_images=request.block_images,
            block_webgl=request.block_webgl,
            geoip=request.geoip,
            proxy=request.proxy,
            i_know_what_im_doing=True,
            screen=constrains
        )

        # Запуск браузера
        browser_instance = await camoufox.start()

        # Инициализация браузера и списка страниц в хранилище
        browsers[request.browser_key] = {
            "browser": browser_instance,
            "pages": []  # Список страниц, связанных с этим браузером
        }

        return {"message": f"Браузер с ключом {request.browser_key} запущен"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка запуска браузера: {str(e)}")



@app.post("/execute_scenario", summary="Выполнение сценария действий")
async def execute_scenario(request: ScenarioRequest):
    # Проверяем, существует ли браузер с переданным ключом
    if request.browser_key not in browsers:
        raise HTTPException(status_code=400, detail="Браузер с данным ключом не запущен")
    
    browser_data = browsers[request.browser_key]
    browser = browser_data.get("browser")
    if browser is None:
        raise HTTPException(status_code=400, detail="Браузер не найден")
    
    try:
        # Получение страницы по индексу или создание новой
        pages = browser_data.setdefault("pages", [])
        if request.page_index >= len(pages):
            # Создаем новую страницу
            page = await browser.new_page()
            pages.append(page)
        else:
            # Используем существующую страницу
            page = pages[request.page_index]

        result = ''

        # Выполняем сценарий шагов
        for step in request.js_scenario:
            for command, params in step.root.items():
                if command == "navigate":
                    result += await utils.goto(page=page, url=params.get("url"))
                elif command == "click":
                    result += await utils.find_and_click(page=page, selector=params.get("selector"), delay=params.get("delay", 500), timeout=params.get("timeout", 3000))
                elif command == "select_radio":
                    result += await utils.select_radio(page=page, selector=params.get("selector"), value=params.get("value"))
                elif command == "select_option":
                    result += await utils.select_option(page=page, selector=params.get("selector"), value=params.get("value"))
                elif command == "scroll":
                    result += await utils.scroll_into_view(page=page, selector=params.get("selector"), retry_count=params.get("retry_count", 10), delay=params.get("delay", 500))
                elif command == "fill":
                    result += await utils.fill(page=page, selector=params.get("selector"), data=params.get("value"))
                elif command == "wait_for_navigation":
                    result += await utils.wait_navigation(page=page, timeout=params.get("timeout"), url_parts=params.get("url_parts"))
                elif command == "wait_for_selector":
                    result += await utils.wait_for_selector(page=page, selector=params.get("selector"), timeout=params.get("timeout"))
                elif command == "evaluate_script":
                    result += await utils.evaluate_script(page=page, script=params.get("script"))
                elif command == "evaluate_script_on_elements":
                    result += await utils.evaluate_script_on_elements(page=page, selector=params.get("selector"), js_command=params.get("js_command"))
                elif command == "get_screenshot_base64":
                    result += await utils.get_screenshot_base64(page=page, timeout=params.get("timeout", 3000))
                elif command == "is_element_on_page":
                    result += await utils.is_element_on_page(page=page, selector=params.get("selector"))
                elif command == "get_captcha_base64":
                    result += await utils.get_captcha_base64(page=page, selector=params.get("selector"))
                elif command == "wait":
                    if isinstance(params, int):  # Убедимся, что параметр - это число 
                        await page.wait_for_timeout(params)
                else:
                    raise HTTPException(status_code=400, detail=f"Неизвестная команда: {command}")
                
                if "error" in result:
                    await stop_browser(request.browser_key)
                    raise ValueError()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка выполнения сценария ({result}): {str(e)}")

    return result

@app.post("/stop_browser", summary="Остановка браузера")
async def stop_browser(browser_key: str):
    if browser_key not in browsers:
        raise HTTPException(status_code=400, detail="Браузер с данным ключом не найден")

    # Закрытие всех страниц и браузера
    browser_data = browsers.pop(browser_key)
    browser = browser_data.get("browser")
    if browser is not None:
        await browser.close()

    return {"message": f"Браузер с ключом {browser_key} остановлен"}