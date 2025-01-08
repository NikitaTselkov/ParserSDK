
using ParserSDK;

using (var client = new ParserClient("http://localhost:8000", 
       new ParserConfig
       {
           BlockWebGL = true,
           GeoIP = true,
           Proxy = new ParserProxyConfig("85.142.143.50:64890", "2DY3DUWG", "iLgHe791")
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


