namespace ParserSDK;

public class ParserResponse
{
    public ParserData Data { get; set; }
    public bool Success { get; set; }
    public string ErrorMessage { get; set; }

    public ParserResponse()
    {
        Success = true;
    }
    
    public ParserResponse(ParserData data)
    {
        Success = true;
        Data = data;
    }
    
    public ParserResponse(string errorMessage)
    {
        ErrorMessage = errorMessage;
        Success = false;
    }
}