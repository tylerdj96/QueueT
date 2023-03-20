using QueuePopNotify.Services;

namespace QueuePopNotify;

public class Startup
{
    public IWebHostEnvironment Env { get; }
    public IConfiguration Configuration { get; }

    public Startup(IWebHostEnvironment env, IConfiguration configuration)
    {
        Env = env;
        Configuration = configuration;
    }

    // This method gets called by the runtime. Use this method to add services to the container.
    public void ConfigureServices(IServiceCollection services)
    {
        // Add services to the container.
        services.AddHttpContextAccessor();
        services.AddControllers();
        services.AddHealthChecks();

        ConfigureDependencies(services);
    }

    // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
    public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
    {
        app.UseHttpsRedirection();


        app.UseRouting();
        app.UseEndpoints(endpoints => { 
            endpoints.MapHealthChecks("/health");
            endpoints.MapControllers(); 
        });
    }

    private void ConfigureDependencies(IServiceCollection services)
    {
        services.Configure<TwilioSettings>(Configuration.GetSection("Twilio"));

        services.AddTransient<ITwilioApiService, TwilioApiService>();

        var accountSID = Configuration.GetSection("Twilio")["AccountSID"];
    }

}

