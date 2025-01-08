using Newtonsoft.Json.Linq;

namespace ParserSDK;

public class ParserData
{
    private readonly List<JToken> _items = new List<JToken>();

    public void Add(JToken item)
    {
        _items.Add(item);
    }

    public T Get<T>(int index)
    {
        var value = _items[index];

        if (value is JArray array)
            return array.ToObject<T>();
        
        return (T)Convert.ChangeType(value.Value<object>(), typeof(T));
    }
}