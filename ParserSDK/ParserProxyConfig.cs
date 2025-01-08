using System.Text.Json.Serialization;

namespace ParserSDK;

public class ParserProxyConfig
{
    [JsonPropertyName("server")]
    public string Server { get; set; }
    
    [JsonPropertyName("username")]
    public string Login { get; set; }
    
    [JsonPropertyName("password")]
    public string Password { get; set; }

    public ParserProxyConfig() {}
    
    public ParserProxyConfig(string server, string login, string password)
    {
        Server = server;
        Login = login;
        Password = password;
    }
}