async function applyCoupon(db, payments, orderId, code) {
  const coupon = await db.coupons.find(code);
  if (coupon.used) throw new Error("already used");
  await db.coupons.markUsed(code);
  const order = await db.orders.find(orderId);
  await payments.charge(order.customerId, order.total - coupon.amount);
}
module.exports = { applyCoupon };
