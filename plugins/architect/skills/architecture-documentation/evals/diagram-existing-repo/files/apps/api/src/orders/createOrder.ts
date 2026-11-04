import Stripe from "stripe";
import { publish } from "../messaging/rabbit";
import { cache } from "../cache/redis";
import { db } from "../db";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function createOrder(req, res) {
  const cart = await cache.get(`cart:${req.user.id}`);
  const intent = await stripe.paymentIntents.create({ amount: cart.total, currency: "usd" });
  const order = await db.orders.insert({ userId: req.user.id, paymentIntent: intent.id });
  await publish("orders.created", { orderId: order.id });
  res.status(201).json(order);
}
