using Microsoft.Extensions.Options;
using Twilio;
using Twilio.Rest.Api.V2010.Account;

namespace QueuePopNotify.Services;

public interface ITwilioApiService {
    public void SendSMS(string text, string toPhoneNumber);
}

public class TwilioApiService : ITwilioApiService
{
    private readonly TwilioSettings _twilioSettings;

    public TwilioApiService(
        IOptions<TwilioSettings> twilioSettings
    )
    {
        _twilioSettings = twilioSettings.Value;
    }
    public void SendSMS(string text, string toPhoneNumber)
    {
        var accountSID = _twilioSettings.AccountSID;
        var authToken = _twilioSettings.AuthToken;
        TwilioClient.Init(accountSID, authToken);

        var message = MessageResource.Create(
            body: text,
            from: _twilioSettings.PhoneNumber,
            to: toPhoneNumber
        );
    }
}