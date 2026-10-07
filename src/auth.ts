import { Request, Response, NextFunction } from "express";
import jwt from "jsonwebtoken";

const PUBLIC_PATHS = ["/health"];

export function authMiddleware(req: Request, res: Response, next: NextFunction) {
  if (PUBLIC_PATHS.includes(req.path)) {
    return next();
  }

  const token = req.headers.authorization?.split(" ")[1];
  if (!token) {
    return res.status(401).json({ error: "Missing token" });
  }

  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET || "");
    (req as any).user = payload;
    next();
  } catch {
    res.status(401).json({ error: "Invalid token" });
  }
}
