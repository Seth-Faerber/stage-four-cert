import { Router, Request, Response } from "express";

const router = Router();

// Simulated user store
const users = [
  { id: 1, name: "Alice", email: "alice@example.com" },
  { id: 2, name: "Bob", email: "bob@example.com" },
];

router.get("/", (req: Request, res: Response) => {
  res.json({ users });
});

router.get("/:id", (req: Request, res: Response) => {
  const user = users.find((u) => u.id === Number(req.params.id));
  if (!user) return res.status(404).json({ error: "User not found" });
  res.json({ user });
});

export default router;
