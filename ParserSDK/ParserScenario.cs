namespace ParserSDK;

public class ParserScenario
{
    private List<string>? _commands;

    public ParserScenario()
    {
        _commands ??= new List<string>();
    }

    public void Navigate(string url, int retryCount = 3, NavigateWaitUntil waitUntil = NavigateWaitUntil.NetworkIdle) 
    {
        _commands.Add($$"""{ "navigate": { "url": "{{url}}", "retryCount": {{retryCount}}, "waitUntil": "{{waitUntil}}" } }""");
    }
    
    public void Fill(string selector, string value)
    {
        _commands.Add($$"""{ "fill": { "selector": "{{EscapeQuotes(selector)}}", "value": "{{value}}" } }""");
    }
    
    public void Scroll(string selector, int maxRetryCount = 10, int delay = 500)
    {
        _commands.Add($$"""{ "scroll": { "selector": "{{EscapeQuotes(selector)}}", "retry_count": {{maxRetryCount}}, "delay": {{delay}} } }""");
    }
    
    public void Click(string selector, int timeout = 3000, int delay = 500)
    {
        _commands.Add($$"""{ "click": { "selector": "{{EscapeQuotes(selector)}}", "timeout": {{timeout}}, "delay": {{delay}} } }""");
    }
    
    public void EvaluateScript(string script)
    {
        _commands.Add($$"""{ "evaluate_script": { "script": "{{EscapeQuotes(script)}}" } }""");
    }
    
    public void EvaluateScriptOnElements(string selector, string script)
    {
        _commands.Add($$"""{ "evaluate_script_on_elements": { "selector": "{{EscapeQuotes(selector)}}", "js_command": "{{EscapeQuotes(script)}}" } }""");
    }
    
    public void ScreenshotBase64(int timeout = 3000)
    {
        _commands.Add($$"""{ "get_screenshot_base64": { "timeout": {{timeout}} } }""");
    }
    
    public void SelectOption(string selector, string value)
    {
        _commands.Add($$"""{ "select_option": { "selector": "{{EscapeQuotes(selector)}}", "value": "{{value}}" }""");
    }
    
    public void SelectRadio(string selector, string value)
    {
        _commands.Add($$"""{ "select_radio": { "selector": "{{EscapeQuotes(selector)}}", "value": "{{value}}" }""");
    }
    
    public void GetCaptchaBase64(string selector)
    {
        _commands.Add($$"""{ "get_captcha_base64": { "selector": "{{EscapeQuotes(selector)}}" }""");
    }
    
    public void IsElementOnPage(string selector)
    {
        _commands.Add($$"""{ "is_element_on_page": { "selector": "{{EscapeQuotes(selector)}}" } }""");
    }
    
    public void Wait(int timeout)
    {
        _commands.Add($$"""{ "wait": {{timeout}} }""");
    }
    
    public void WaitForSelector(string selector, int timeout = 30000)
    {
        _commands.Add($$"""{ "wait_for_selector": { "selector": "{{EscapeQuotes(selector)}}", "timeout": {{timeout}} } }""");
    }
    
    public void WaitForNavigation(int timeout, params string[] urlParts)
    {
        _commands.Add($$"""{ "wait_for_navigation": { "timeout": {{timeout}}, "url_parts": [ {{string.Join(", ", urlParts.Select(part => "\"" + part + "\""))}} ] } }""");
    }
    
    public override string ToString()
    {
        return string.Join(",\r\n\t", _commands);
    }
    
    private string EscapeQuotes(string input)
    {
        if (string.IsNullOrEmpty(input))
            return input;

        return input.Replace("\"", "\\\"");
    }
}