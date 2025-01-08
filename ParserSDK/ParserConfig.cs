using System.Text.Json.Serialization;

namespace ParserSDK;

public class ParserConfig
{
    [JsonPropertyName("browser_key")]
    public string? BrowserKey { get; set; }
    
    [JsonPropertyName("fingerprint")]
    public string? Fingerprint { get; set; } // Переданный fingerprint в JSON-формате
    
    [JsonPropertyName("browser")]
    public string Browser { get; set; } = "firefox"; // Тип браузера (если fingerprint отсутствует)
    
    [JsonPropertyName("os")]
    public string OS { get; set; } = "windows"; // ОС (если fingerprint отсутствует)
    
    [JsonPropertyName("humanize")]
    public bool Humanize { get; set; } = true; // Человекообразное поведение
    
    [JsonPropertyName("block_images")]
    public bool BlockImages { get; set; } = false; // Блокировать изображения
    
    [JsonPropertyName("block_webgl")]
    public bool BlockWebGL { get; set; } = false; // Блокировать WebGL
    
    [JsonPropertyName("geoip")]
    public bool GeoIP { get; set; } = false; // Использовать GeoIP
    
    [JsonPropertyName("proxy")]
    public ParserProxyConfig? Proxy { get; set; } = null; // Настройки прокси
}