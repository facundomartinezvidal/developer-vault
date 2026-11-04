var builder = WebApplication.CreateBuilder(args);
builder.Services.AddDbContext<AppDbContext>();
var app = builder.Build();

app.MapPost("/orders/{id}/cancel", async (int id, AppDbContext db) =>
{
    var order = await db.Orders.FindAsync(id);
    if (order is null) return Results.NotFound();
    if (order.Status == "Shipped") return Results.Conflict();
    order.Status = "Cancelled";
    await db.SaveChangesAsync();
    return Results.NoContent();
});

app.Run();
