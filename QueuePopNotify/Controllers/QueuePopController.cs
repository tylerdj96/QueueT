using Microsoft.AspNetCore.Mvc;
using QueuePopNotify.Models;
using QueuePopNotify.Services;

namespace QueuePopNotify.Controllers;

[ApiController]
[Route("[controller]")]
public class QueuePopController : ControllerBase
{
    private ITwilioApiService _twilioService;

    public QueuePopController(ITwilioApiService twilioService)
    {
        _twilioService = twilioService;
    }

    [HttpPost(Name = "QueuePop")]
    public IActionResult Post(QueuePopDTO dto)
    {
        try
        {
            var queuePopText = "Your Queue Popped!";
            _twilioService.SendSMS(queuePopText, dto.PhoneNumber);
        }
        catch (Exception e)
        {
            return BadRequest();
        }
        return NoContent();
    }
}
