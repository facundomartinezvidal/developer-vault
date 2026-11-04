var builder = WebApplication.CreateBuilder(args);
builder.Services.AddDbContext<AppDbContext>();
builder.Services.AddSingleton<AuditService>();
builder.Services.AddAuthorization();
var app = builder.Build();
app.UseAuthorization();
OrdersEndpoints.Map(app);
app.Run();
