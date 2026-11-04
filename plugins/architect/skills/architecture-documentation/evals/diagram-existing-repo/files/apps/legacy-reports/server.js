// Nightly report endpoint. Nothing in this repo calls it.
app.get("/reports/daily", async (_req, res) => {
  res.json(await db.query("select date(created_at), sum(total) from orders group by 1"));
});
