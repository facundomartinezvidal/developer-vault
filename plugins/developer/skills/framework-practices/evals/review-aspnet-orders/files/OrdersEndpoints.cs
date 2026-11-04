public class AuditService(AppDbContext db)
{
    public Task Write(string message) => db.SaveChangesAsync();
}

public static class OrdersEndpoints
{
    public static void Map(WebApplication app)
    {
        app.MapGet("/orders/{id}", (int id, AppDbContext db) =>
        {
            return db.Orders.FindAsync(id).AsTask().Result;
        }).RequireAuthorization();

        app.MapPost("/orders/{id}/notify", (int id, HttpContext ctx, AppDbContext db) =>
        {
            _ = Task.Run(async () =>
            {
                var order = await db.Orders.FindAsync(id);
                var client = new HttpClient();
                await client.PostAsJsonAsync("https://mail.internal/send",
                    new { order!.Email, Path = ctx.Request.Path.Value });
            });
            return Results.Accepted();
        }).RequireAuthorization();
    }
}
