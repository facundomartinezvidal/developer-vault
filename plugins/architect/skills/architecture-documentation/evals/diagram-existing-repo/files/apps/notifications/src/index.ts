import sgMail from "@sendgrid/mail";
import { consume } from "./rabbit";
import { db } from "./db";

consume("orders.created", async ({ orderId }) => {
  const order = await db.query("select o.*, u.email from orders o join users u on u.id = o.user_id where o.id = $1", [orderId]);
  await sgMail.send({ to: order.email, from: "shop@example.com", subject: "Order confirmed", text: `Order ${order.id}` });
  await db.query("update orders set notified_at = now() where id = $1", [orderId]);
});
