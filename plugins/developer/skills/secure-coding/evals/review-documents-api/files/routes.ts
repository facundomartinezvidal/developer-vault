import express from "express";
import { exec } from "child_process";
import jwt from "jsonwebtoken";
import { db } from "./db";

const SECRET = "supersecret123";
export const router = express.Router();

router.use((req: any, _res, next) => {
  req.user = jwt.decode(req.headers.authorization ?? "");
  next();
});

router.get("/documents/:id", async (req: any, res) => {
  const doc = await db.documents.findById(req.params.id);
  res.json(doc);
});

router.post("/convert", (req: any, res) => {
  exec(`convert uploads/${req.query.name} out/${req.query.name}.pdf`, (err) => {
    if (err) return res.status(500).send(err.message);
    res.send("ok");
  });
});

export function signToken(userId: string) {
  return jwt.sign({ userId }, SECRET);
}
