using System.Text.Json.Serialization;

namespace QueuePopNotify.Models;


public class QueuePopDTO {

        [JsonPropertyName("phoneNumber")]
        public string PhoneNumber { get; set; }
};

