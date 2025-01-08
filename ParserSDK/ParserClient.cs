using System.Text.Json;
using Flurl;
using Flurl.Http;
using Flurl.Http.Configuration;
using Newtonsoft.Json.Linq;

namespace ParserSDK;

public class ParserClient : IDisposable, IAsyncDisposable
{
    private ParserConfig _config;
    private string _serverUrl;

    public ParserClient(string serverUrl, ParserConfig? parserConfig = null)
    {
        _config = parserConfig ?? new ParserConfig();
        _serverUrl = serverUrl.TrimEnd('/');
        
        CreateSessionAsync().GetAwaiter().GetResult();
    }
    
    public async Task<ParserResponse> ExecuteScenario(ParserScenario scenario, int page = 0)
    {
        try
        {
            var url = _serverUrl + "/execute_scenario";
            
            var request = $$"""
              {
                "browser_key": "{{_config.BrowserKey}}",
                "page_index": {{page}},
                "js_scenario": [
                  {{scenario.ToString()}}
                ]
              }
              """;
           
            var response = await url.WithHeader("Content-Type", "application/json").PostStringAsync(request).ReceiveString();

            if (response.Contains("error"))
                return new ParserResponse(response);

            var str = response.Trim('\"').Replace("\\\"", "\"").Replace("\\\\", "\\");
            var parts = str.Split("}{");
            var parserData = new ParserData();
            
            for (int i = 0; i < parts.Length; i++)
            {
                if (i > 0) parts[i] = "{" + parts[i];
                if (i < parts.Length - 1) parts[i] = parts[i] + "}";
                
                var json = JObject.Parse(parts[i]);

                if (json.TryGetValue("value", out var value))
                    parserData.Add(value);
            }
            
            return new ParserResponse(parserData);
        }
        catch (Exception e)
        {
            if (e is FlurlHttpException flurlEx)
                return new ParserResponse(await flurlEx.GetResponseStringAsync());
            
            return new ParserResponse(e.Message);
        }
    }

    public async Task StopSession()
    {
        try
        {
            var url = _serverUrl + "/stop_browser";
            var response = await url.SetQueryParam("browser_key", _config.BrowserKey).PostAsync();
        }
        catch (Exception e) {}
    }
    
    private async Task CreateSessionAsync()
    {
        try
        {
            if (string.IsNullOrWhiteSpace(_config.BrowserKey))
                _config.BrowserKey = Guid.NewGuid().ToString();

            var url = _serverUrl + "/start";

            var flurlClient = new FlurlClient(url);
            flurlClient.Settings.JsonSerializer = new DefaultJsonSerializer(new JsonSerializerOptions {
                PropertyNameCaseInsensitive = true,
                IgnoreReadOnlyProperties = true,
                IgnoreNullValues = true
            });
            
            var response = await flurlClient.Request().PostJsonAsync(_config);
        }
        catch (Exception e) {}
    }
    
    public void Dispose()
    {
        StopSession().GetAwaiter().GetResult();
    }

    public async ValueTask DisposeAsync()
    {
        await StopSession();
    }
}