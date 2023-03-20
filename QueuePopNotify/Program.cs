using Azure.Identity;
using QueuePopNotify;


Host.CreateDefaultBuilder(args)
.ConfigureWebHostDefaults(webBuilder =>
{
    webBuilder.UseStartup<Startup>();
}).ConfigureAppConfiguration((hostContext, configurationBuilder) =>
{
    configurationBuilder.AddEnvironmentVariables();    

        var config = configurationBuilder.Build();
        configurationBuilder.AddAzureKeyVault(
            new Uri($"{config.GetConnectionString("KeyVault")}"),
            new DefaultAzureCredential()
        );
    if (args != null) configurationBuilder.AddCommandLine(args);
}).Build().Run();
